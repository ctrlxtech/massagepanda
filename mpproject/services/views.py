from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import stripe

from services.models import Service

# Create your views here.
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
    try:
      needTable = request.POST.get("needTable")
      service = Service.objects.get(pk=request.POST.get("serviceId"))
      tax = service.service_fee * 0.1
      serviceDate = request.POST.get("massageDetailsDate")
      serviceTime = request.POST.get("massageDetailsTime")
      genderPrefer = request.POST.get("genderPreferred")
    except:
      return render(request, 'services/checkout.html')
    
    stripeCustomer = ""
    try:
      stripe.api_key = settings.STRIPE_KEY
      stripeCustomer = stripe.Customer.retrieve(request.user.customer.stripe_customer_id)
    except:
      pass

    context = {'service': service, 'serviceDate': serviceDate, 'serviceTime': serviceTime,
        'gender': genderPrefer, 'needTable': needTable, 'tax': tax, 'stripeCustomer': stripeCustomer}
    return render(request, 'services/checkout.html', context)
