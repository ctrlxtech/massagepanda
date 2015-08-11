from django.shortcuts import render
from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import stripe

from customers.models import Address

# Create your views here.
@login_required(login_url="/customers/login")
def index(request):
    state_list = Address.STATE_CHOICES
    context = {'state_list': state_list}
    return render(request, 'customers/profile.html', context)

@login_required(login_url="/customers/login")
def referPage(request):
    context = {"customer": "Kevin"}
    return render(request, 'customers/refer.html', context)

@register.filter
def div(value, arg):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        value = int(value)
        arg = int(arg)
        if arg:
                
            return '{0:.02f}'.format(float(value) / arg)
    except: pass
    return ''

@register.filter
def addCardImageSrc(value, arg):
    try:
        arg = str(arg)
        arg = arg.replace(" ", "").lower()
        return str(value) + arg
    except:
        pass
    return ""

@login_required(login_url="/customers/login")
def historyPage(request):
    context = {"customer": "Kevin"}
    return render(request, 'customers/history.html', context)

@login_required(login_url="/customers/login")
def paymentPage(request):
    checkAdmin(request)
    stripe.api_key = settings.STRIPE_KEY
    stripeCustomer = ""
    try:
        stripeCustomer = stripe.Customer.retrieve(request.user.customer.stripe_customer_id)
    except:
        pass
    context = {'stripeCustomer': stripeCustomer}
    return render(request, 'customers/payment.html', context)
    
def checkAdmin(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
    except:
        return HttpResponse("No valid customer found(probably you are an admin?)")

