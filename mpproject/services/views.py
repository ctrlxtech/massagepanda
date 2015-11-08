from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import redirect, render_to_response
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.template.defaulttags import register
from django.views.generic import View

from customers.models import Address
from feedback.models import Feedback
from payment.models import Order, Coupon, GENDER_PREFERENCES
from referral.models import CustomerReferralHistory
from services.models import Service

from manager.views import sendSMS

import hashlib
import re
import stripe
import time
from datetime import datetime
from django.utils import timezone

# Create your views here.
@register.filter
def stripZero(value):
    return ('%f' % value).rstrip(".0")

def services(request):
    service_list = Service.objects.order_by('popularity')
    context = {'service_list': service_list}
    return render_to_response('services/store.html', context, context_instance=RequestContext(request))

def details(request):
    context = {}
    try:
      service = Service.objects.get(id=request.POST.get('serviceId'))
      context['service'] = service
    except:
      return JsonResponse("Service not found", safe=False)
    return render_to_response('services/details.html', context, context_instance=RequestContext(request))

class DetailsView(View):
    context = {}
    def get(self, request):
      return render_to_response('services/details.html', self.context, context_instance=RequestContext(request))

def taxService(service):
    if service.service_sale:
      total = service.service_sale
    else:
      total = service.service_fee

    tax = total * settings.TAX
    return total + tax, tax

def taxAdditional(data):
    needTable = data.get("needTable")
    additional = 0
    if not needTable or needTable == "None":
      return 0, 0

    zipcode = data.get('zipcode')
    if isInSF(zipcode):
      additional += 10
    tax = additional * settings.TAX
    return additional + tax, tax

def checkout(request):
    context = {}
    try:
      zipcode = request.POST.get('zipcode')
      serviceDate = request.POST.get("massageDetailsDate")
      serviceTime = request.POST.get("massageDetailsTime")
      genderPreferred = request.POST.get("genderPreferred")

      try:
        service = Service.objects.get(pk=request.POST.get("serviceId"))
      except:
        raise Exception("Service not found")

      total, tax = taxService(service)

      additional, aTax = taxAdditional(request.POST)
      tax += aTax
      total += additional

      needTable = request.POST.get("needTable")
      parkingInfo = request.POST.get("parkingInfo")
      massage1 = request.POST.get("massage1")
      if massage1:
        parkingInfo += " |massage1: " + massage1
      massage2 = request.POST.get("massage2")
      if massage2:
        parkingInfo += " |massage2: " + massage2
      b2b = request.POST.get("backToBack")
      if b2b:
        parkingInfo += " |Accept back-to-back"

      if additional != 0:
        context['additionalCharge'] = True
    except Exception as e:
      return HttpResponse(e)
   
    stripeCustomer = ""
    try:
      stripe.api_key = settings.STRIPE_KEY
      stripeCustomer = stripe.Customer.retrieve(request.user.customer.stripe_customer_id)
    except:
      pass

    state_list = Address.STATE_CHOICES
    context.update({'stripePublishKey': settings.STRIPE_PUBLISH_KEY, 'state_list': state_list, 'service': service, 'serviceDate': serviceDate,
        'serviceTime': serviceTime, 'gender': genderPreferred, 'needTable': needTable, 'parkingInfo': parkingInfo,
        'zipcode': zipcode, 'tax': '%.2f' % tax, 'subtotal': '%.2f' % (total - tax), 'total': '%.2f' % total, 'stripeCustomer': stripeCustomer})
    return render_to_response('services/checkout.html', context, context_instance=RequestContext(request))

def stringToDatetime(data):
    service_datetime_string = data.get('serviceDate')
    service_datetime_string += " " + data.get('serviceTime')
    date_format = '%m/%d/%Y %I:%M%p'
    return datetime.strptime(service_datetime_string, date_format)

def getPhone(data):
    phone = data.get('phone')
    phone = re.sub("[^0-9]", "", phone)
    if len(phone) == 10:
        phone = "1" + phone
    return phone

def sendOrderNotificationToManager(order):
    subject, from_email, to = 'New Order!', settings.SERVER_EMAIL, settings.ORDER_NOTIFICATION_EMAIL
    try:
      text_content = "address: " + order.shipping_address + " ,customer: " + order.recipient \
        + " ,gender: " + order.get_preferred_gender_display() + " ,time: " + order.service_datetime.ctime() + " ,service: " \
        + order.service.service_type + " for " + str(order.service.service_time) + " hour(s) ,table: " \
        + str(order.need_table) + " ,parking: " + order.parking_info
    except:
      text_content = "Check admin page for new order!"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
    return HttpResponse("Email sent!")

def sendNewOrderEmailToCustomer(order):
    stripe.api_key = settings.STRIPE_KEY
    stripeCharge = stripe.Charge.retrieve(order.stripe_token)
    subject, from_email, to = 'Thank you for your order! - MassagePanda', settings.SERVER_EMAIL, order.email
    text_content = 'This is an email containing your order.'
    html_content = get_template('payment/order_confirmation_email.html').render(Context({'order': order, 'stripeCharge': stripeCharge}))
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def createUncapturedCharge(amount, stripeToken, stripeCustomerId):
    ch = {'status': 'failure'}
    try:
      ch = stripe.Charge.create(
        amount=amount, # amount in cents, again
        currency="usd",
        customer=stripeCustomerId,
        source=stripeToken,
        capture=False,
        description="Uncaptured charge"
      )
    except stripe.error.StripeError, e:
      ch['error'] = str(e)
      return ch

    return ch

def uncaptureCharge(request):
    try:
        amount, markDown, coupon, isSuccess = markDownPrice(request.POST)
    except Exception as e:
        return JsonResponse(e, safe=False)
    amount = amount * 100

    stripe.api_key = settings.STRIPE_KEY
    stripeToken = request.POST.get('stripeToken')
    try:
      stripeCustomerId = request.user.customer.stripe_customer_id
    except:
      stripeCustomerId = None

    ch = createUncapturedCharge(amount, stripeToken, stripeCustomerId)
    if ch['status'] == 'succeeded':
        request.session['succeeded'] = True
    return JsonResponse(ch)

def insertReferCode(order, customer=None):
    if customer is None:
        return

    try: 
        crh = CustomerReferralHistory(order=order, code=customer.referredcustomer.code, referred_customer=customer)
        crh.save()
    except:
        pass
    return

def redeemRefer(order=None):
    if order is None:
        return

    try:
        rc = order.customerreferralhistory.referred_customer.referredcustomer
        if rc.redeemed is False:
            rc.redeemed = True
            rc.save()
    except:
        pass
    return

def getAddressDetail(customer, data):
    phone = getPhone(data)
    email = data.get('email')

    sName = data.get('first-name')
    sName += " " + data.get('last-name')
    sAL1 = data.get('al1').strip()
    sAL2 = data.get('al2')
    address = sAL1
    if sAL2 is not None and sAL2:
        address = address + " " + sAL2.strip()
    sCity = data.get('city').strip()
    sCountry = data.get('country').strip()
    sState = data.get('state').strip()
    sZipcode = data.get('zipcode').strip()
    address = address + ", " + sCity + ", " + sState + ", " +\
        sCountry + " " + sZipcode

    if customer is not None:
        # add shipping address for the customer
        a = Address(customer=customer, name=sName, phone=phone, email=email, address_line1=sAL1, address_line2=sAL2, 
            zipcode=sZipcode, city=sCity, state=sState, country=sCountry)
        a.save()
    return address

def addPaymentForCustomer(customer, stripeToken):
    newPayment = "error"
    if customer is not None:
        stripe.api_key = settings.STRIPE_KEY
        cu = stripe.Customer.retrieve(customer.stripe_customer_id)
        newPayment = cu.sources.create(source=stripeToken)
    return newPayment

def isCurrent(coupon):
    now = timezone.now()
    return coupon.start_date <= now and coupon.end_date >= now

def markDownPrice(data):
    isSuccess = False

    try:
        service = Service.objects.get(pk=data.get("serviceId"))
        total, tax = taxService(service)
    except:
        return 0, 0, None, isSuccess

    additional, aTax = taxAdditional(data)
    couponCode = data.get('couponCode').upper()
    coupon = None
    newPrice = total
    try:
        coupon = Coupon.objects.get(code=couponCode)

        if (not coupon.servicecoupon_set.all() or service in [sc.service for sc in coupon.servicecoupon_set.all()]) \
            and coupon.quantity != 0 and isCurrent(coupon):
          if coupon.is_flat:
            newPrice -= coupon.discount * ( 1 + settings.TAX)
          else:
            newPrice *= coupon.discount
          isSuccess = True
    except:
        pass
    markDown = total - newPrice
    newPrice += additional
    return int(newPrice), markDown, coupon, isSuccess
   
def applyCoupon(request):
    newPrice, markDown, coupon, isSuccess = markDownPrice(request.POST)
    if isSuccess:
        context = {'status': 'success', 'newPrice': '%.2f' % newPrice, 'markDown': '%.2f' % markDown, 'couponCode': coupon.code}
    else:
        context = {'status': 'failure', 'error': 'Invalid coupon'}
    return JsonResponse(context)

def deleteCoupon(request):
    try:
        service = Service.objects.get(pk=request.POST.get("serviceId"))
        total, tax = taxService(service)
    except:
        return JsonResponse({'status': 'failure', 'error': 'Error occurred'})

    additional, aTax = taxAdditional(request.POST)
    total += additional
    context = {'status': 'success', 'serviceFee': '%.2f' % total}
    return JsonResponse(context)

def createFeedbackForOrder(order):
    f = Feedback(order=order, code=getFeedbackCode(order.id), rated=False)
    f.save()
    return

def getFeedbackCode(value):
    m = hashlib.md5()
    m.update(str(time.time()))
    m.update(str(value))
    return m.hexdigest()

def isInSF(zipcode):
    try:
      if int(zipcode) in settings.SF_ZIPCODES:
        return True
      else:
        return False
    except:
        return False

@register.filter
def gender_display(q):
    for choice in GENDER_PREFERENCES:
        if choice[0] == q:
            return choice[1]
    return ''

def placeOrderFromJson(request):
    data = json.loads(request.body)
    return placeOrder(request, data);

def placeOrderFromPost(request):
    try:
      if request.session['complete']:
        request.session['complete'] = False
        return redirect('index')
    except:
      pass

    try:
      if request.session['succeeded']:
        request.session['succeeded'] = False
    except:
        raise Http404("Invalid card!")
      
    data = request.POST;
    return placeOrder(request, data);

@transaction.atomic
def placeOrder(request, data):
    customer = None
    stripeCustomerId = None
    if request.user.is_authenticated():
        try:
            customer = request.user.customer
        except:
            pass

    savedAddress = data.get("savedAddress")
    savedPayment = data.get("savedPayment")

    if savedPayment:
        stripeToken = savedPayment
        stripe.api_key = settings.STRIPE_KEY
        stripeCustomer = stripe.Customer.retrieve(customer.stripe_customer_id)
        name = stripeCustomer.sources.retrieve(savedPayment).name
        stripeCustomerId = customer.stripe_customer_id
    else:
        stripeToken = data.get('stripeToken')
        name = data.get('name')
        if customer is not None and stripeToken:
            addPaymentForCustomer(customer, stripeToken)

    try:
        amount, markDown, coupon, isSuccess = markDownPrice(data)
        serviceId = data.get('serviceId')
    except Exception as e:
        return JsonResponse(e, safe=False)
    amount = amount * 100

    if savedAddress:
        addressObj = Address.objects.get(pk=savedAddress)
        address = addressObj.detail()
        sName = addressObj.name
        phone = addressObj.phone
        email = addressObj.email
    else:
        address = getAddressDetail(customer, data)
        sName = data.get('first-name')
        sName += " " + data.get('last-name')
        phone = getPhone(data)
        email = data.get('email')

    service_datetime = stringToDatetime(data)
    preferredGender = data.get('serviceGenderPreferred')
    needTable = request.POST.get("needTable")
    if needTable != "None":
        needTable = True
    else:
        needTable = False
    parkingInfo = request.POST.get("parkingInfo")
   
    o = Order(stripe_token=stripeToken, service_id=serviceId, service_datetime=service_datetime, coupon=coupon,
        preferred_gender=preferredGender, need_table=needTable, parking_info=parkingInfo, customer=customer,
        amount=amount, shipping_address=address, recipient=sName, billing_name=name, phone=phone, email=email)
    o.save()
    
    if isSuccess:
        if coupon.quantity > 0:
          coupon.quantity -= 1
        coupon.used += 1
        coupon.save()

    insertReferCode(o, customer)
    createFeedbackForOrder(o)

    message_body = "Thank you for booking with MassagePanda! We are reaching out to our therapists now, and we'll let you know once anyone responds!"
    nums = [phone]
    sendSMS(nums, message_body, False)
    sendNewOrderEmailToCustomer(o)

    sendOrderNotificationToManager(o)

    request.session['complete'] = True
    context = {'status': 'success', 'total': o.amount, 'txid': o.id}
    return render_to_response('services/success.html', context, context_instance=RequestContext(request))

