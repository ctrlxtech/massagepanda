from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.defaulttags import register
from django.views.generic import View

from customers.models import Address
from feedback.models import Feedback
from payment.models import Order, OrderTherapist, Coupon
from services.models import Service

from manager.views import sendSMS

import hashlib
import stripe
import time
from datetime import datetime

# Create your views here.
@register.filter
def stripZero(value):
    return ('%f' % value).rstrip(".0")

def services(request):
    service_list = Service.objects.order_by('popularity')
    context = {'service_list': service_list}
    return render(request, 'services/store.html', context)

def details(request):
    context = {}
    try:
      service = Service.objects.get(id=request.POST.get('serviceId'))
      context['service'] = service
    except:
      return JsonResponse("Service not found", safe=False)
    return render(request, 'services/details.html', context)

class DetailsView(View):
    context = {}
    def get(self, request):
      return render(request, 'services/details.html', self.context)

def taxService(data):
    try:
      service = Service.objects.get(pk=data.get("serviceId"))
    except:
      raise Exception("Service not found")

    if service.service_sale:
      total = service.service_sale
    else:
      total = service.service_fee

    tax = total * settings.TAX
    return total + tax, tax

def taxAdditional(data):
    needTable = data.get("needTable")
    if needTable:
      additional = 10.0;
    else:
      additional = 0.0;
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
 
      service = Service.objects.get(pk=request.POST.get("serviceId"))
      total, tax = taxService(request.POST)

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

      if isInSF(zipcode):
        context['inSF'] = True
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
        'zipcode': zipcode, 'tax': '%.2f' % tax, 'total': '%.2f' % total, 'stripeCustomer': stripeCustomer})
    return render(request, 'services/checkout.html', context)

def placeOrderFromJson(request):
    data = json.loads(request.body)
    return placeOrder(request, data);

def placeOrderFromPost(request):
    data = request.POST;
    return placeOrder(request, data);

def stringToDatetime(data):
    service_datetime_string = data.get('serviceDate')
    service_datetime_string += " " + data.get('serviceTime')
    date_format = '%m/%d/%Y %I:%M%p'
    return datetime.strptime(service_datetime_string, date_format)

def getPhone(data):
    phone = data.get('phone')
    if len(phone) == 10:
        phone = "1" + phone
    return phone

@transaction.atomic
def placeOrder(request, data):
    customer = None;
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
    else:
        stripeToken = data.get('stripeToken')
        name = data.get('name')
        if customer is not None and stripeToken:
            addPaymentForCustomer(customer, stripeToken)

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

    try:
        amount, markDown = markDownPrice(data)
        serviceId = data.get('serviceId')
    except Exception as e:
        return JsonResponse(e, safe=False)
    amount = amount * 100

    service_datetime = stringToDatetime(data)
    preferredGender = data.get('serviceGenderPreferred')
    needTable = request.POST.get("needTable")
    if needTable != "None":
        needTable = True
    else:
        needTable = False
    parkingInfo = request.POST.get("parkingInfo")
   
    o = Order(stripe_token=stripeToken, service_id=serviceId, service_datetime=service_datetime,
        preferred_gender=preferredGender, need_table=needTable, parking_info=parkingInfo, customer=customer,
        amount=amount, shipping_address=address, recipient=sName, billing_name=name, phone=phone, email=email)
    o.save()
    
    createFeedbackForOrder(o)

    message_body = "Thank you for booking with MassagePanda! We are reaching out to our therapists now, and we'll let you know once anyone responds!"
    nums = [phone]
    sendSMS(nums, message_body, False)

    context = {'status': 'success', 'total': o.amount, 'txid': o.id}
    return render(request, 'services/success.html', context)

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

def addPaymentForCustomer(customer, stripeToken):
    newPayment = "error"
    if customer is not None:
        stripe.api_key = settings.STRIPE_KEY
        cu = stripe.Customer.retrieve(customer.stripe_customer_id)
        newPayment = cu.sources.create(source=stripeToken)
    return newPayment

def markDownPrice(data):
    try:
        total, tax = taxService(data)
    except Exception as e :
        return JsonResponse(e, safe=False)

    additional, aTax = taxAdditional(data)
    couponCode = data.get('couponCode').upper()
    try:
        discount = Coupon.objects.get(code=couponCode).discount
    except:
        discount = 1
    newPrice = total * discount
    markDown = total - newPrice
    newPrice += additional
    return newPrice, markDown
   
def applyCoupon(request):
    newPrice, markDown = markDownPrice(request.POST)
    couponCode = request.POST.get('couponCode').upper()
    context = {'status': 'success', 'newPrice': '%.2f' % newPrice, 'markDown': '%.2f' % markDown, 'couponCode': couponCode.upper()}
    return JsonResponse(context)

def deleteCoupon(request):
    try:
        total, tax = taxService(request.POST)
    except Exception as e :
        return JsonResponse(e, safe=False)

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
