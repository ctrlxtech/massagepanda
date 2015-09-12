from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.defaulttags import register

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
    return ('%f' % value).rstrip('0').rstrip('.')

def services(request):
    service_list = Service.objects.order_by('service_type')
    context = {'service_list': service_list}
    return render(request, 'services/store.html', context)

def details(request):
    context = {}
    try:
      service = Service.objects.get(pk=request.POST.get('serviceId'))
      context['service'] = service
    except:
      pass
    return render(request, 'services/details.html', context)

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
      context['inSF'] = True
      additional += 10
    tax = additional * settings.TAX
    return additional + tax, tax

def checkout(request):
    context = {}
    try:
      service = Service.objects.get(pk=request.POST.get("serviceId"))
      total, tax = taxService(request.POST)
    except Exception as e:
      return HttpResponse(e)

    additional, aTax = taxAdditional(request.POST)
    tax += aTax
    total += additional
    needTable = request.POST.get("needTable")
    zipcode = request.POST.get('zipcode')
    serviceDate = request.POST.get("massageDetailsDate")
    serviceTime = request.POST.get("massageDetailsTime")
    genderPrefer = request.POST.get("genderPreferred")
    
    stripeCustomer = ""
    try:
      stripe.api_key = settings.STRIPE_KEY
      stripeCustomer = stripe.Customer.retrieve(request.user.customer.stripe_customer_id)
    except:
      pass

    state_list = Address.STATE_CHOICES
    context.update({'state_list': state_list, 'service': service, 'serviceDate': serviceDate,
        'serviceTime': serviceTime, 'gender': genderPrefer, 'needTable': needTable,
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

@transaction.atomic
def placeOrder(request, data):
    try:
        amount, markDown = markDownPrice(data)
        serviceId = data.get('serviceId')
    except Exception as e:
        return JsonResponse(e)
    amount = amount * 100

    service_datetime = stringToDatetime(data)
    preferred_gender = data.get('serviceGenderPreferred')
    stripeToken = data.get('stripeToken')
    name = data.get('name')
    sName = data.get('first-name')
    sName += " " + data.get('last-name')
    phone = data.get('phone')
    if len(phone) == 10:
        phone = "1" + phone

    email = data.get('email')
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

    customer = None;
    if request.user.is_authenticated():
        try:
            customer = request.user.customer
        except:
            pass

    o = Order(stripe_token=stripeToken, service_id=serviceId, service_datetime=service_datetime,
        preferred_gender=preferred_gender, customer=customer, amount=amount,
        shipping_address=address, recipient=sName, billing_name=name, phone=phone, email=email)
    o.save()
    
    createFeedbackForOrder(o)

    if customer is not None:
        if stripeToken:
            addPaymentForCustomer(customer, stripeToken)

        # add shipping address for the customer
        a = Address(customer=customer, name=sName, address_line1=sAL1, address_line2=sAL2, zipcode=sZipcode, city=sCity, state=sState, country=sCountry)
        a.save()
    message_body = "Thank you for booking with MassagePanda! We are reaching out to our therapists now, and we'll let you know once anyone responds!"
    nums = [phone]
    sendSMS(nums, message_body, False)

    context = {'status': 'success'}
    return render(request, 'services/success.html', context)

def addPaymentForCustomer(customer, stripeToken):
    newPayment = "error"
    if customer is not None:
        # update customer's stripe default card
        stripe.api_key = settings.STRIPE_KEY
        cu = stripe.Customer.retrieve(customer.stripe_customer_id)
        newPayment = cu.sources.create(source=stripeToken)
    return newPayment

def markDownPrice(data):
    try:
        total, tax = taxService(data)
    except Exception as e :
        return JsonResponse(e)

    additional, aTax = taxAdditional(data)
    couponCode = data.get('couponCode').upper()
    discount = Coupon.objects.get(code=couponCode).discount
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
        return JsonResponse(e)

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
