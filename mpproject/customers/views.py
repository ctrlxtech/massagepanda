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
from django.shortcuts import render, redirect
from django.template import loader
from django.template.defaulttags import register
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

import stripe

from customers.models import Customer, Address
from services.views import addPaymentForCustomer, getPhone

# Create your views here.
@login_required(login_url="/customer/login")
def index(request):
    state_list = Address.STATE_CHOICES
    context = {'state_list': state_list}
    return render(request, 'customers/profile.html', context)

def createCustomerFromForm(request):
    return createCustomer(request.POST, request)

def createCustomerFromJson(request):
    data = json.loads(request.body)
    return createCustomer(data)

@transaction.atomic
def createCustomer(data, request=None):
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

      code = referralCodeGenerator()
      customerReferralCode = CustomerReferralCode(customer=customer, code=code)
      customerReferralCode.save()
    except IntegrityError as e:
      return JsonResponse({"message": e.message})

    return sendValidationEmail(request, user)

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

      login(request, user)

      sendWelcomeEmail(user.email, first_name, code)
      context = {'status': 'success', 'firstName': first_name}
    else:
      context = {'status': 'failure'}

    return redirect('index')

def sendWelcomeEmail(to, first_name, code):
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
    token_generator=default_token_generator
    body = loader.render_to_string(email_template_name, context)
    email_message = EmailMultiAlternatives(subject, body, settings.SERVER_EMAIL, [user.email])
    email_message.send()
    context = {'status': 'success', 'message': 'Email sent!'}
    return JsonResponse(context)

def loginFromForm(request):
    return userLogin(request, request.POST)

def loginFromJson(request):
    data = json.loads(request.body)
    return userLogin(request, data)

def userLogin(request, data):
    context = {'status': 'failure'}
    userID = request.POST.get('userID')
    fbToken = request.POST.get('fbToken')
    if fbToken and userID:
        request.session['login'] = True
        return HttpResponse("token: " + fbToken + " userID: " + userID)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            request.session['login'] = True
            context['status'] = 'success'
            context['firstName'] = user.first_name
        else:
            context['error'] = "user is inactive!"
    else:
        context['error'] = "username and password do not match!"
    if 'error' in context:
        return render(request, 'customers/login.html', context)
    else:
        return redirect('index')
    return JsonResponse(context)

def loginView(request):
    if request.user.is_authenticated():
        return redirect('index')
    return render(request, 'customers/login.html')

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
    return render(request, 'customers/refer.html', context)

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
    return render(request, 'customers/history.html', context)

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
    return render(request, 'customers/payment.html', context)
    
def checkAdmin(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
    except:
        return HttpResponse("No valid customer found(probably you are an admin?)")

