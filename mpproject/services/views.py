from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.defaulttags import register

from customers.models import Address
from feedback.models import Feedback
from payment.models import Order, OrderTherapist
from services.models import Service

import hashlib
import stripe
import time

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

def checkout(request):
    context = {}
    try:
      needTable = request.POST.get("needTable")
      service = Service.objects.get(pk=request.POST.get("serviceId"))
    except:
      return HttpResponse("Service not found")
    if needTable:
      total = 10.0;
    else:
      total = 0.0;
    if service.service_sale:
      total += service.service_sale
    else:
      total += service.service_fee
    zipcode = request.POST.get('zipcode')
    if isInSF(zipcode):
      context['inSF'] = True
      total += 10
    tax = total * settings.TAX
    total += tax
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
        'zipcode': zipcode, 'tax': tax, 'total': total, 'stripeCustomer': stripeCustomer})
    return render(request, 'services/checkout.html', context)

def placeOrderFromJson(request):
    data = json.loads(request.body)
    return placeOrder(request, data);

def placeOrderFromPost(request):
    data = request.POST;
    return placeOrder(request, data);

@transaction.atomic
def placeOrder(request, data):
    customer = None;
    if request.user.is_authenticated():
        try:
            customer = request.user.customer
        except:
            pass

    serviceId = data.get('serviceId')
    if serviceId is None or not serviceId:
        context = {'status': 'failure', 'error': 'serviceId is not available'}
        return JsonResponse(context)
    mamount = Service.objects.get(pk=serviceId).service_fee * 100
    service_datetime_string = data.get('serviceDate')
    service_datetime_string += " " + data.get('serviceTime')
    date_format1 = '%m/%d/%Y %I:%M%p'
    date_format2 = '%Y-%m-%d %I:%M%p'
    service_datetime = None
    try:
        service_datetime = datetime.strptime(service_datetime_string, date_format1)
    except:
        service_datetime = datetime.strptime(service_datetime_string, date_format2)

    preferred_gender = data.get('serviceGenderPreferred')
    token = data.get('stripeToken')
    name = data.get('name')
    sName = data.get('first-name')
    sName += " " + data.get('last-name')
    phone = data.get('phone')
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

    o = Order(token=token, service_id=serviceId, service_datetime=service_datetime,
        preferred_gender=preferred_gender, customer=customer, amount=mamount,
        shipping_address=address, recipient=sName, name=name, phone=phone, email=email)
    o.save()
    
    f = Feedback(order=o, code=getFeedbackCode(o.id), rated=False)
    f.save()

    if customer is not None:
        # update customer's stripe default card
        stripe.api_key = settings.STRIPE_KEY
        cu = stripe.Customer.retrieve(customer.stripe_customer_id)
        cu.source = token
        cu.save()

        # add shipping address for the customer
        a = Address(customer=customer, name=sName, address_line1=sAL1, address_line2=sAL2, zipcode=sZipcode, city=sCity, state=sState, country=sCountry)
        a.save()
    message_body = "Thank you for booking with MassagePanda! We are reaching out to our therapists now, and we'll let you know once anyone responds!"
    nums = [phone]
    sendSMS(nums, message_body, False)

    context = {'status': 'success'}
    return render(request, 'services/success.html', context)
    return JsonResponse(context)

def applyCoupon(request):
    couponCode = request.POST.get('couponCode').upper()
    if couponCode == 'TWENTYOFF':
        context = {'status': 'success', 'newPrice': 60, 'discount': 20, 'couponCode': couponCode.upper()}
    else:
        context = {'error': 'Invalid coupon code!'}
    return JsonResponse(context)

def deleteCoupon(request):
    serviceId = request.POST.get('serviceId')
    try:
        service = Service.objects.get(pk=serviceId)
        if service.service_sale:
            serviceFee = Service.objects.get(pk=serviceId).service_sale
        else:
            serviceFee = Service.objects.get(pk=serviceId).service_fee
        context = {'status': 'success', 'serviceFee': serviceFee}
    except:
        context = {'error': 'Invalid service!'}
    return JsonResponse(context)

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
