from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import redirect, render_to_response
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.template.defaulttags import register
from django.views.generic import View

from customers.models import Address
from feedback.models import Feedback
from payment.models import Order, Coupon, GENDER_PREFERENCES
from referral.models import CustomerReferralCode, CustomerReferralHistory, ReferralCredit
from services.models import Service
from django.contrib import messages

from manager.views import sendSMS

import hashlib
import requests
import json
import re
import stripe
import time
from datetime import datetime
from django.utils import timezone

# Create your views here.
@register.filter
def stripZero(value):
    return ('%f' % value).rstrip(".0")

@register.filter
def sum(creditSet):
    try:
      credit_sum = creditSet.aggregate(Sum('credit'))

      value = credit_sum.get('credit__sum', 0)
      if value:
        return '%.2f' % value
      else:
        return '0.00'
    except:
      return '0.00'

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
    if re.match("couple", Service.objects.get(pk=data.get("serviceId")).service_type, re.I):
      additional *= 2
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
        'serviceTime': serviceTime, 'gender': genderPreferred, 'needTable': needTable, 'parkingInfo': parkingInfo, 'zipcode': zipcode,
        'additional': '%.2f' % additional, 'tax': '%.2f' % tax, 'subtotal': '%.2f' % (total - tax), 'total': '%.2f' % total, 'stripeCustomer': stripeCustomer})
    return render_to_response('services/checkout.html', context, context_instance=RequestContext(request))

def stringToDatetime(data):
    service_datetime_string = data.get('serviceDate')
    service_datetime_string += " " + data.get('serviceTime')
    date_format = '%m/%d/%Y %I:%M%p'
    return datetime.strptime(service_datetime_string, date_format)

def getPhone(data):
    phone = str(data.get('phone'))
    phone = filter(str.isdigit, phone)
    phone = re.sub("[^0-9]", "", phone)
    if len(phone) == 10:
        phone = "1" + phone
    return phone

def sendOrderNotificationToManager(order):
    subject, from_email, to = 'New Order! - ' + str(order.id.int >> 96), settings.SERVER_EMAIL, settings.ORDER_NOTIFICATION_EMAIL
    try:
      charge = order.amount / 100.0
      text_content = order.recipient + ", " + order.shipping_address + ", " + order.service.service_type \
        + " for " + str(order.service.service_time) + " hour(s), " + order.service_datetime.ctime() \
        + ". Customer Phone: " + order.phone + ", Customer email: " + order.email + ". " + order.get_preferred_gender_display() \
        + ", table: " + str(order.need_table) + ", parking: " + order.parking_info + ", charge: $" + str(charge) + ", coupon: " + str(order.coupon)
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

def isSavedPaymentSeleted(request):
    savedPayment = request.POST.get("savedPayment")
    return savedPayment and savedPayment != "new-payment-selector"

def isAccountBalanceSeleted(request):
    paymentType = request.POST.get("payment-type")
    return paymentType and paymentType == "account-balance"

def isSavedAddressSeleted(request):
    savedAddress = request.POST.get("savedAddress")
    return savedAddress and savedAddress != "new-address-selector"

def createUncapturedCharge(amount, stripeToken, stripeCustomerId):
    ch = {'status': 'failure'}
    if amount == 0: # create place holder amount
        amount = 100
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
    request.session['complete'] = False
    try:
        amount, markDown, coupon, isSuccess = markDownPrice(request.POST)
        if isAccountBalanceSeleted(request):
            amount = max(amount - request.user.customer.referralcredit_set.all().latest('id').accumulative_credit, 0)
    except Exception as e:
        return JsonResponse(e, safe=False)

    amount = amount * 100

    customer = None
    stripeCustomerId = None
    if request.user.is_authenticated():
        try:
            customer = request.user.customer
            stripeCustomerId = customer.stripe_customer_id
        except:
            pass

    stripe.api_key = settings.STRIPE_KEY

    if isSavedPaymentSeleted(request):
        stripeToken = request.POST.get("savedPayment")
    else:
        stripeToken = request.POST.get('stripeToken')
        if customer is not None and stripeToken:
            stripeToken = addPaymentForCustomer(customer, stripeToken).id

    ch = createUncapturedCharge(int(amount), stripeToken, stripeCustomerId)

    if ch['status'] == 'succeeded':
        request.session['succeeded'] = True
    return JsonResponse(ch)

def insertReferOrder(order, customer=None):
    if customer is None:
        return

    try: 
        crh = customer.customerreferralhistory
        if not crh.order:
          crh.order = order
          crh.save()
    except:
        pass
    return

def rewardCredit(customer, crh, credit=float(settings.REFER_BONUS)):
    accumulativeCredit = 0
    try:
        accumulativeCredit = customer.referralcredit_set.all().latest('id').accumulative_credit
    except:
        pass
    accumulativeCredit += credit
    rCredit = ReferralCredit(customer=customer, customer_referral_history=crh, credit=credit, accumulative_credit=accumulativeCredit)
    rCredit.save()

@transaction.atomic
def redeemRefer(order=None):
    if order is None:
        return

    try:
      crh = order.customerreferralhistory
      if crh.status == 'P' and crh.order:
        referredCustomer = crh.referred_customer
        referrer = crh.code.customer

        rewardCredit(referrer, crh)

        crh.status = 'S'
        crh.save()
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
    return newPrice, markDown, coupon, isSuccess
   
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
    f = Feedback(order=order, rated=False)
    f.save()
    return f

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

def subscribeCustomer(request, order, list_id):
    url = "https://us10.api.mailchimp.com/3.0/lists/" + list_id + "/members"
    fname_lname = order.recipient.split(' ', 1)
    payload = {'apikey': settings.MAILCHIMP_KEY, 'status': 'subscribed', 'email_address': order.email, 'merge_fields': {'FNAME': fname_lname[0], 'LNAME':fname_lname[1]}}
    headers = {'Content-type': 'application/json', 'Authorization': 'apikey fe35e80bca4df4928991af8f0e3092be-us10'}
    return requests.post(url, data=json.dumps(payload), headers=headers)
      
class PlaceOrderView(View):
    def get(self, request):
        return redirect('index')
    def post(self, request):
        return placeOrderFromPost(request);

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

def placeOrder(request, data):
    customer = None
    stripeCustomerId = None
    rCredit = None
    credit_used = 0
    if request.user.is_authenticated():
        try:
            customer = request.user.customer
        except:
            pass

    if isSavedPaymentSeleted(request):
        stripe.api_key = settings.STRIPE_KEY
        stripeCustomer = stripe.Customer.retrieve(customer.stripe_customer_id)
        name = stripeCustomer.sources.retrieve(data.get("savedPayment")).name
        stripeCustomerId = customer.stripe_customer_id
    else:
        name = data.get('name')

    stripeToken = data.get('stripeToken')

    try:
        amount, markDown, coupon, isSuccess = markDownPrice(data)
        if isAccountBalanceSeleted(request):
            accumulative_credit = request.user.customer.referralcredit_set.all().latest('id').accumulative_credit
            credit_used = min(amount, accumulative_credit)
            remain_credit = accumulative_credit-credit_used
            rCredit = ReferralCredit(customer=customer, credit=-credit_used, accumulative_credit=remain_credit)

        serviceId = data.get('serviceId')
    except Exception as e:
        return JsonResponse(e, safe=False)
    amount = amount * 100

    if isSavedAddressSeleted(request):
        addressObj = Address.objects.get(pk=data.get("savedAddress"))
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
   
    if amount == 0:
        amount = 100 # create place holder amount
    o = Order(stripe_token=stripeToken, service_id=serviceId, service_datetime=service_datetime, coupon=coupon,
        preferred_gender=preferredGender, need_table=needTable, parking_info=parkingInfo, customer=customer,
        amount=amount, credit_used=credit_used, shipping_address=address, recipient=sName, billing_name=name, phone=phone, email=email)
    o.save()
    
    if rCredit and isinstance(rCredit, ReferralCredit):
        rCredit.order = o
        rCredit.save()

    if isSuccess:
        if coupon.quantity > 0:
          coupon.quantity -= 1
        coupon.used += 1
        coupon.save()

    insertReferOrder(o, customer)
    f = createFeedbackForOrder(o)

    message_body = "Thank you for booking with MassagePanda! We are reaching out to our therapists now, and we'll let you know once anyone responds!"
    nums = [phone]
    sendSMS(nums, message_body, False)
    sendNewOrderEmailToCustomer(o)

    subscribeCustomer(request, o, "e77933f373")

    sendOrderNotificationToManager(o)

    request.session['complete'] = True
    context = {'status': 'success', 'total': o.amount, 'txid': o.id}
    return render_to_response('services/success.html', context, context_instance=RequestContext(request))

