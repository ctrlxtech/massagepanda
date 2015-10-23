from django.shortcuts import render_to_response

from django.template import RequestContext
from django.template.defaulttags import register
from django.http import HttpResponse, JsonResponse
from services.models import Service
from services.views import stripZero # used by order_confirmation_email
from payment.models import Order
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings

import decimal
import stripe

# Create your views here.
# Set your secret key: remember to change this to your live secret key in production
# See your keys here https://dashboard.stripe.com/account/apikeys

def test(request):
    return render_to_response('payment/test.html', {}, context_instance=RequestContext(request))

def index(request):
    service_list = Service.objects.order_by('service_type')
    context = {"id": request.GET.get("id"), "service_list": service_list}
    return render_to_response('payment/index.html', context, context_instance=RequestContext(request))

def buy(request):
    serviceId = request.POST.get("serviceId")
    ser = Service.objects.get(pk=serviceId)
    service_fee = 0
    if ser.service_sale:
        service_fee = ser.service_sale
    else:
      service_fee = ser.service_fee
    tax = service_fee * settings.TAX
    total = service_fee + tax
    context = {"date": request.POST.get("Date"), "time": request.POST.get("Time"),
        "gender": request.POST.get("Gender"), "quantity": request.POST.get("Quantity"),
        "service": ser.service_type, "serviceFee": service_fee, "tax": tax, "total": total}
    return render_to_response('payment/charge.html', context, context_instance=RequestContext(request))

def charge(request):
    serviceId = request.POST.get("serviceId")
    service = Service.objects.get(pk=serviceId)
    fee = int(float(service.service_fee) * 100)
    stripe.api_key = settings.STRIPE_KEY
    # Get the credit card details submitted by the form
    token = request.POST.get('stripeToken', False)
    try:
        charge = stripe.Charge.create(
        amount=fee, # amount in cents, again
        currency="usd",
        source=token,
        description="Example charge"
    )
    except stripe.CardError, e:
    # The card has been declined
      pass

    return HttpResponse(charge.status)

@user_passes_test(lambda u: u.is_superuser)
def processOrder(request):
    orderId = request.POST.get("orderId")
    statusToUpdate = request.POST.get("statusToUpdate")
    order = Order.objects.get(pk=orderId)
    context = {'status': 'error', 'statusToUpdate': statusToUpdate, 'orderId': orderId}
    if order is not None and order:
        order.status = statusToUpdate
        order.save()
        context['status'] = 'success'
    return JsonResponse(context)

@register.filter
def get_service(dictionary, key):
    return dictionary.get(pk=key)

@register.filter
def centsToDollars(cents):
    cents_to_dollars_format_string = '{:,.2f}'
    return cents_to_dollars_format_string.format(cents/100.0)

@register.filter
def getFirstFromAddress(address):
    return address.split(',', 1)[0]

@register.filter
def getSecondFromAddress(address):
    return address.split(',', 1)[1]
