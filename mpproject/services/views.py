from django.shortcuts import render
from django.conf import settings
import stripe

from services.models import Service

# Create your views here.
def services(request):
    service_list = Service.objects.order_by('service_type')
    context = {'service_list': service_list}
    return render(request, 'services/store.html', context)

def details(request):
    service_list = Service.objects.order_by('service_type')
    context = {'service_list': service_list}
    return render(request, 'services/details.html', context)

def checkout(request):
    massageType = request.POST.get("massageType")
    massageFee = request.POST.get("massageFee")
    serviceDate = request.POST.get("massageDetailsDate")
    serviceTime = request.POST.get("massageDetailsTime")
    genderPrefer = request.POST.get("genderPreferred")

    stripe.api_key = settings.STRIPE_KEY
    stripeCustomer = ""
    try:
        stripeCustomer = stripe.Customer.retrieve(request.user.customer.stripe_customer_id)
    except:
        pass

    context = {'massageType': massageType, 'massageFee': massageFee,
        'serviceDate': serviceDate, 'serviceTime': serviceTime, 
        'gender': genderPrefer, 'stripeCustomer': stripeCustomer}
    return render(request, 'services/checkout.html', context)
