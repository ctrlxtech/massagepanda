from django.shortcuts import render

from django.template.defaulttags import register
from django.http import HttpResponse
from services.models import Service
import stripe
# Create your views here.
# Set your secret key: remember to change this to your live secret key in production
# See your keys here https://dashboard.stripe.com/account/apikeys

def test(request):
    return render(request, 'payment/test.html')


def index(request):
    service_list = Service.objects.order_by('service_type')
    context = {"id": request.GET.get("id"), "service_list": service_list}
    return render(request, 'payment/index.html', context)

def buy(request):

    serviceId = request.POST.get("serviceId")
    context = {"Date": request.POST.get("Date"), "Time": request.POST.get("Time"),
        "Gender": request.POST.get("Gender"), "Quantity": request.POST.get("Quantity"),
        "serviceId": serviceId}
    return render(request, 'payment/charge.html', context)

def charge(request):
    serviceId = request.POST.get("serviceId")
    service = Service.objects.get(pk=serviceId)
    fee = int(float(service.service_fee) * 100)
    stripe.api_key = "sk_test_aibfico1Lcf9qydk9snpXVrI"
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

@register.filter
def get_service(dictionary, key):
    return dictionary.get(pk=key)
