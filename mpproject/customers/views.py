from django.db import transaction, IntegrityError
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render_to_response
from django.template import loader, RequestContext
from django.template.defaulttags import register
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt

import json
import re
import requests
import stripe

from customers.models import Customer, Address
from referral.models import CustomerReferralCode
from referral.views import referralCodeGenerator
from services.views import addPaymentForCustomer, getPhone

# Create your views here.
@login_required(login_url="/customer/login")
def index(request):
    state_list = Address.STATE_CHOICES
    context = {'state_list': state_list}
    return render_to_response('customers/profile.html', context, context_instance=RequestContext(request))

def createCustomerFromForm(request):
    return createCustomer(request.POST, request)

def createCustomerFromJson(request):
    try:
        data = json.loads(request.body)
    except:
        data = None
    return createCustomer(data)

@transaction.atomic
def createCustomer(data, request=None):
    if data is None:
      return JsonResponse({"message": "check your inputs"})

    referCode = None
    if request is not None:
        referCode = request.session['code']

    email = data.get('email')
    phone = getPhone(data)
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    gender = data.get('gender')
    try:
      user = User.objects.create_user(email, email, password,
        first_name=first_name, last_name=last_name)
      user.is_active = False
      user.save()

      stripe.api_key = settings.STRIPE_KEY

      stripe_cus = stripe.Customer.create(
        description=user.get_full_name(),
        email=user.email
      )
      customer = Customer(user=user, stripe_customer_id=stripe_cus['id'], gender=gender, phone=phone)
      customer.save()

      if referCode is not None:
          crh = CustomerReferralHistory(referred_customer=customer, code=CustomerReferralCode.objects.get(code=referCode))
          crh.save()

      code = referralCodeGenerator()
      customerReferralCode = CustomerReferralCode(customer=customer, code=code)
      customerReferralCode.save()
    except IntegrityError as e:
      return JsonResponse({"message": e.message})

    sendValidationEmail(request, user)
    return redirect('index')

@transaction.atomic
def verifyCustomer(request, uidb64=None, token=None, token_generator=default_token_generator):
    assert uidb64 is not None and token is not None  # checked by URLconf
    UserModel = get_user_model()
    try:
      # urlsafe_base64_decode() decodes to bytestring on Python 3
      uid = force_text(urlsafe_base64_decode(uidb64))
      user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
      user = None

    if user is not None and token_generator.check_token(user, token):
      if user.is_active:
        login(request, user)
        return redirect('index')

      user.is_active = True
      user.save()

      user.backend = 'django.contrib.auth.backends.ModelBackend'
      login(request, user)

      sendWelcomeEmail(user.email, user.first_name)
      context = {'status': 'success', 'firstName': user.first_name}
    else:
      context = {'status': 'failure'}

    return render_to_response('customers/verify.html', context, context_instance=RequestContext(request))

def sendWelcomeEmail(to, first_name):
    subject = "Welcome!"
    text_content = "Thanks for signing up on MassagePanda! Hope you enjoy our services."
    msg = EmailMultiAlternatives(subject, text_content, settings.SERVER_EMAIL, [to])
    msg.send()
    return HttpResponse("Email sent!")

def sendValidationEmail(request, user, use_https=False):
    email_template_name='customers/signup_validation_email.html'
    subject='MassagePanda: Verify your email to complete your account signup'
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain
    token_generator=default_token_generator
    context = {
        'email': user.email,
        'domain': domain,
        'site_name': site_name,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
        'protocol': 'https' if use_https else 'http',
    }
    body = loader.render_to_string(email_template_name, context)
    email_message = EmailMultiAlternatives(subject, body, settings.SERVER_EMAIL, [user.email])
    email_message.send()
    context = {'status': 'success', 'message': 'Email sent!'}
    return JsonResponse(context)

def loginFromForm(request):
    payload = {"response": request.POST.get('g-recaptcha-response'), "secret": settings.GOOGLE_RECAPTCHA}
    resp = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload).json()
    if resp['success']:
        return userLogin(request, request.POST)
    else:
        context = {'status': 'failure', 'error': 'Are you a bot?'}
        return render_to_response('customers/login.html', context, context_instance=RequestContext(request))

@csrf_exempt
def loginFromJson(request):
    try:
        data = json.loads(request.body)
    except:
        data = None
    return userLogin(request, data, True)

def userLogin(request, data, fromJson=False):
    context = {'status': 'failure'}
    userID = request.POST.get('userID')
    fbToken = request.POST.get('fbToken')
    if fbToken and userID:
        request.session['login'] = True
        return HttpResponse("token: " + fbToken + " userID: " + userID)
    if data is None:
      json = JsonResponse({"error": "check your inputs"}, safe=False)
      json['Access-Control-Allow-Origin'] = "*"
      json['Access-Control-Allow-Methods'] = "GET,POST"
      json['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
      return json

    username = data.get('username')
    password = data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            request.session['login'] = True
            context['status'] = 'success'
            context['firstName'] = user.first_name
            context['lastName'] = user.last_name
            try:
                context['rating'] = float(user.therapist.rating) / user.therapist.rate_count
            except:
                pass
            context['uid'] = urlsafe_base64_encode(force_bytes(user.pk))
        else:
            context['error'] = "user is inactive!"
    else:
        context['error'] = "username and password do not match!"
    if fromJson:
        json = JsonResponse(context, safe=False)
        json['Access-Control-Allow-Origin'] = "*"
        json['Access-Control-Allow-Methods'] = "GET,POST"
        json['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
        return json
    elif 'error' in context:
        return render_to_response('customers/login.html', context, context_instance=RequestContext(request))
    else:
        return redirect('index')

def registerView(request):
    if request.user.is_authenticated():
        return redirect('index')

    if request.GET.get('code'):
        request.session['code'] = request.GET.get('code')
    return render_to_response('customers/register.html', {}, context_instance=RequestContext(request))

def loginView(request):
    if request.user.is_authenticated():
        return redirect('index')
    return render_to_response('customers/login.html', {}, context_instance=RequestContext(request))

def logoutView(request):
    logout(request)
    try:
        del request.session['login']
    except KeyError:
        pass
    return redirect('index')

@login_required(login_url="/customer/login")
def changePassword(request):
    oldPassword = request.POST.get('oldPassword')    
    newPassword = request.POST.get('newPassword')    
    user = authenticate(username=request.user.username, password=oldPassword)
    if user is not None:
      if user.is_active:
        user.set_password(newPassword)
        user.save()
        update_session_auth_hash(request, user)
        context = {'status': 'success'}
      else:
        context = {'status': 'failure', 'error': 'wrong password'}
    else:
        context = {'status': 'failure', 'error': 'wrong password'}
    return JsonResponse(context)

def resetPassword(request):
    email_template_name='registration/password_reset_email.html'
    subject_template_name='registration/password_reset_subject.txt'
    token_generator=default_token_generator
    email = request.POST.get('email')
    form = PasswordResetForm({'email': email})
    if form.is_valid():
        opts = {
            'use_https': request.is_secure(),
            'token_generator': token_generator,
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'email_template_name': email_template_name,
            'subject_template_name': subject_template_name,
            'request': request,
            'html_email_template_name': None,
        }
        form.save(**opts)
        context = {'status': 'success', 'message': 'Email sent!'}
    else:
        context = {'status': 'failure', 'error': 'We did not find the email in our system!'}
    return JsonResponse(context)

@login_required(login_url="/customer/login")
def addNewAddress(request):
    firstName = request.POST.get('firstName')
    lastName = request.POST.get('lastName')
    name = firstName.strip() + " " + lastName.strip()
    email = request.POST.get('email')
    phone = getPhone(request.POST)
    address = request.POST.get('address')
    zipcode = request.POST.get('zipcode')
    city = request.POST.get('city')
    state = request.POST.get('state')
    country = request.POST.get('country')
    try:
        a = Address(customer=request.user.customer, name=name, email=email, phone=phone, address_line1=address, city=city, state=state, country=country, zipcode=zipcode)
        a.save()
        context = {'status': 'success', 'addressId': a.id, 'name': name, 'address_line1': address, 'zipcode': zipcode, 'city': city, 'state': state}
    except:
        context = {'status': 'failure', 'error': 'Check your inputs please'}
    return JsonResponse(context)

@login_required(login_url="/customer/login")
def deleteAddress(request):
    try:
        addressId = force_text(urlsafe_base64_decode(request.POST.get('addressId')))
        a = request.user.customer.address_set.get(pk=addressId)
        a.delete()
        context = {'status': 'success'}
    except:
        context = {'status': 'failure', 'error': 'Check your inputs please: ' + addressId}
    return JsonResponse(context)

@login_required(login_url="/customer/login")
@transaction.atomic
def setDefaultAddress(request):
    try:
        addressId = force_text(urlsafe_base64_decode(request.POST.get('addressId')))
        addresses = request.user.customer.address_set.all()
        addresses.update(default=False)
        addresses.filter(id=addressId).update(default=True)
        context = {'status': 'success'}
    except:
        context = {'status': 'failure', 'error': 'Check your inputs please: ' + str(addressId)}
    return JsonResponse(context)

@login_required(login_url="/customer/login")
def addNewPayment(request):
    stripeToken = request.POST.get('stripeToken')
    newPayment = addPaymentForCustomer(request.user.customer, stripeToken)
    context = {'newPayment': newPayment}
    return JsonResponse(context)

@login_required(login_url="/customer/login")
def deletePayment(request):
    try:
        cardId = request.POST.get('cardId')
        customer = stripe.Customer.retrieve(request.user.customer.stripe_customer_id)
        customer.sources.retrieve(cardId).delete()
        context = {'status': 'success'}
    except:
        context = {'status': 'failure'}
    return JsonResponse(context)

@login_required(login_url="/customer/login")
def referPage(request):
    context = {"customer": "Kevin"}
    return render_to_response('customers/refer.html', context_instance=RequestContext(request, context))

@register.filter
def encodeId(value):
    return urlsafe_base64_encode(force_bytes(value))

@register.filter
def div(value, arg):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        value = float(value)
        arg = float(arg)
        if arg:
            return '{0:.02f}'.format(value / arg)
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

@login_required(login_url="/customer/login")
def historyPage(request):
    context = {"customer": "Kevin"}
    return render_to_response('customers/history.html', context, context_instance=RequestContext(request))

@login_required(login_url="/customer/login")
def paymentPage(request):
    checkAdmin(request)
    stripe.api_key = settings.STRIPE_KEY
    stripeCustomer = ""
    try:
        stripeCustomer = stripe.Customer.retrieve(request.user.customer.stripe_customer_id)
    except:
        pass
    context = {'stripeCustomer': stripeCustomer, 'stripePublishKey': settings.STRIPE_PUBLISH_KEY}
    return render_to_response('customers/payment.html', context, context_instance=RequestContext(request))
    
def checkAdmin(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
    except:
        return HttpResponse("No valid customer found(probably you are an admin?)")

