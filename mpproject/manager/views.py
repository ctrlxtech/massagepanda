from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.db import connection
from django.contrib.auth.decorators import user_passes_test

from django.template.defaulttags import register

from django.http import HttpResponse, JsonResponse
from manager.models import Staff, Therapist, InSMS, OutSMS, ForwardNumber, SMSTemplate
from payment.models import Order, Charge
from django.contrib.auth.models import User
from customers.models import Customer
from django.db import transaction
import requests
import json
import time
import datetime
import stripe
# Create your views here.

def test(request):
    address = buildAddress(request)
    return HttpResponse("I got address: " + address)

def buildAddress(request):
    address = request.POST.get('al1')
    address = address.strip()
    sAL2 = request.POST.get('al2')
    sAL2 = sAL2.strip()
    if sAL2 is not None and not sAL2:
        address = address + " " + sAL2
    sCity = request.POST.get('city')
    sCountry = request.POST.get('country')
    sState = request.POST.get('state')
    sZipcode = request.POST.get('zipcode')
    address = address + ", " + sCity.strip() + ", " + sState.strip() + ", " +\
        sCountry + " " + sZipcode.strip()
    return address

@user_passes_test(lambda u: u.is_superuser)
def payment(request):
    return render(request, 'manager/payment.html')

def placeOrder(request):
    data = json.loads(request.body)
    mamount = data['amount']
    mamount = float(mamount) * 100
    # Get the credit card details submitted by the form
    token = data['stripeToken']
    bPhone = data['phone']
    bEmail = data['email']
    
    customer = None;
    if request.user.is_authenticated():
        try:
            customer = request.user.customer
        except:
            pass
    name = data['full-name']
    phone = data['phone']
    email = data['email']
    address = data['al1']
    address = address.strip()
    sAL2 = data['al2']
    sAL2 = sAL2.strip()
    if sAL2 is not None and not sAL2:
        address = address + " " + sAL2
    sCity = data['city']
    sCountry = data['country']
    sState = data['state']
    sZipcode = data['zipcode']
    address = address + ", " + sCity.strip() + ", " + sState.strip() + ", " +\
        sCountry + " " + sZipcode.strip()

    o = Order(token=token, customer=customer, amount=mamount, b_phone=bPhone, b_email=bEmail, shipping_address=address, name=name, phone=phone, email=email)
    o.save()
    message_body = "Thank you for booking with MassagePanda! We are reaching out to our therapists now, and we'll let you know once anyone responds!"
    api_key = "412847f0"
    api_secret = "55f41401"
    payload = {'api_key': api_key, 'api_secret': api_secret, 'from': "12069396577", 'to': phone, 'type': 'unicode', 'text': message_body} 
    r = requests.get("https://rest.nexmo.com/sms/json", params=payload).text

    context = {'status': 'success'}
    return JsonResponse(context)

def placeOrderInfo(request):
    mamount = request.POST.get('amount')
    mamount = float(mamount) * 100

    # Get the credit card details submitted by the form
    token = request.POST.get('stripeToken', False)
    bPhone = request.POST.get('phone', "unknown_billing_phone")
    bEmail = request.POST.get('email', "unknown_billing_email")
    
    customer = None;
    if request.user.is_authenticated():
        try:
            customer = request.user.customer
        except:
            pass
    name = request.POST.get('full-name', "unknown_name")
    phone = request.POST.get('phone', "unknown_phone")
    email = request.POST.get('email', "unknown_email")
    sa = buildAddress(request)
    o = Order(token=token, customer=customer, amount=mamount, b_phone=bPhone, b_email=bEmail, shipping_address=sa, name=name, phone=phone, email=email)
    o.save()
    context = {'status': 'success'}
    return JsonResponse(context)

@user_passes_test(lambda u: u.is_superuser)
def orders(request):
    order_list = Order.objects.filter(charged=False)
    charge_list = Charge.objects.all()
    order_tl = []
    charge_tl = []
    #stripe.api_key = "sk_live_4oD38m4mvOMOba8TlT2cqi3A"
    stripe.api_key = "sk_test_jcGeofOhYGQw7BPl3UPGP0lh"
    for order in order_list:
        order_tl.append(stripe.Token.retrieve(order.token))
    for charge in charge_list:
        charge_tl.append(stripe.Charge.retrieve(charge.charge_token))
    #return HttpResponse(token_list)
    context = {'order_list': order_list, 'order_tl': order_tl, 'charge_list': charge_list, 'charge_tl': charge_tl}
    return render(request, 'manager/orders.html', context)

@user_passes_test(lambda u: u.is_superuser)
def getOrders(request):
    index = request.GET.get('index')
    data = serializers.serialize("json", Order.objects.filter(charged=False)[index:])
    return HttpResponse(data)

@register.filter
def lookup(d, key):
    return d[key]

def mcharge(request):
    orderId = request.POST.get('orderId')
    order = Order.objects.get(pk=orderId)
    mtoken = request.POST.get('token')
    mamount = request.POST.get('amount')
    b_phone = request.POST.get('b_phone')
    b_email = request.POST.get('b_email')
    mname = request.POST.get('name')
    mphone = request.POST.get('phone')
    memail = request.POST.get('email')
    sa = request.POST.get('sa')
    #stripe.api_key = "sk_live_4oD38m4mvOMOba8TlT2cqi3A"
    stripe.api_key = "sk_test_jcGeofOhYGQw7BPl3UPGP0lh"
    try:
        chargeObj = stripe.Charge.create(
        amount=mamount, # amount in cents, again
        currency="usd",
        source=mtoken,
        description="Example charge",
        receipt_email=b_email,
    )
    except stripe.CardError, e:
    # The card has been declined
      return HttpResponse(str(e))

    o = Order.objects.get(token=mtoken)
    o.charged = True;
    o.save();

    c = Charge(customer=order.customer, charge_token=chargeObj['id'], shipping_address=sa, name=mname, phone=mphone, email=memail)
    c.save()
    return JsonResponse(chargeObj)
    '''
    r = token + "<br>" + al1 + "<br>" + al2
    return HttpResponse(r)
    '''

@user_passes_test(lambda u: u.is_superuser)
def mrefund(request):
    chargeToken = request.POST.get('chargeToken')
    chargeId = request.POST.get('chargeId')
    ch = stripe.Charge.retrieve(chargeToken)
    try:
        re = ch.refunds.create()
    except e:
        return HttpResponse(str(e))
    c = Charge.objects.get(pk=chargeId)
    c.refunded = True
    c.save()

    return HttpResponse("Refund succeeded<br>" + str(re))

@user_passes_test(lambda u: u.is_superuser)
def index(request):
    staff_list = Staff.objects.order_by('first_name')
    template_list = SMSTemplate.objects.all()
    context = {'staff_list': staff_list, 'template_list': template_list}
    return render(request, 'manager/sms.html', context)

@user_passes_test(lambda u: u.is_superuser)
def logs(request):
    cursor = connection.cursor()
    cursor.execute("select manager_insms.sender, manager_insms.timestamp," \
        " manager_staff.first_name, manager_staff.last_name," \
        " manager_insms.messageBody from manager_insms left join manager_staff" \
        " on manager_insms.sender = manager_staff.phone_number ORDER BY manager_insms.id DESC")
    inSMS_list = dictfetchall(cursor)

    cursor.execute("select manager_outsms.receiver, manager_outsms.timestamp," \
        " manager_staff.first_name, manager_staff.last_name," \
        " manager_outsms.messageBody from manager_outsms left join manager_staff" \
        " on manager_outsms.receiver = manager_staff.phone_number ORDER BY manager_outsms.id DESC")

    outSMS_list = dictfetchall(cursor)
    context = {'inSMS_list': inSMS_list, 'outSMS_list': outSMS_list}
    return render(request, 'manager/logs.html', context)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

@user_passes_test(lambda u: u.is_superuser)
def send(request):
    nums = request.POST.getlist('needToSend')
    number = request.POST.get('num')
    if number is not None and number != '':
        nums.append(number)
    message_body = request.POST.get('message')
    number = ""
    api_key = "412847f0"
    api_secret = "55f41401"
    r = []
    for n in nums:
        payload = {'api_key': api_key, 'api_secret': api_secret, 'from': "12069396577", 'to': n, 'type': 'unicode', 'text': message_body} 
        r.append(requests.get("https://rest.nexmo.com/sms/json", params=payload).text)
        o = OutSMS(receiver=n, messageBody=message_body, timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        o.save()
        time.sleep(1)
    return HttpResponse(r)

def sendWithNum(request):
    number = request.POST.get('num')
    message_body = request.POST.get('message')
    api_key = "412847f0"
    api_secret = "55f41401"
    payload = {'api_key': api_key, 'api_secret': api_secret, 'from': "12069396577", 'to': number, 'type': 'unicode', 'text': message_body} 
    r = requests.get("https://rest.nexmo.com/sms/json", params=payload).text
    o = OutSMS(receiver=number, messageBody=message_body, timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    o.save()

    return HttpResponse(r)

def receiveSMS(request):
    msisdn = request.GET.get('msisdn')
    message_body = request.GET.get('text')
    time_stamp = request.GET.get('message-timestamp')

    if (time_stamp is None or msisdn is None or message_body is None):
        return HttpResponse("***Error request")
    
    time_stamp = utc_to_local(time_stamp)
    i = InSMS(sender=msisdn, messageBody=message_body, timestamp=time_stamp)
    i.save()
    api_key = "412847f0"
    api_secret = "55f41401"
    message_body += "[sent by " + msisdn + " at " + time_stamp + "]"
    for_numbers = ForwardNumber.objects.all()
    for num in for_numbers:
        key = num.number_id
        payload = {'api_key': api_key, 'api_secret': api_secret, 'from': "12069396577",
            'to': Staff.objects.get(pk=key).phone_number, 'type': 'unicode', 'text': message_body} 
        requests.get("https://rest.nexmo.com/sms/json", params=payload).text
        time.sleep(1)

    return HttpResponse()

@user_passes_test(lambda u: u.is_superuser)
def configurations(request):
    staff_list = Staff.objects.order_by('first_name')
    context = {'staff_list': staff_list, 'for_staff': Staff.objects.filter(forwardnumber__number_id__isnull=False)}
    return render(request, 'manager/configurations.html', context)

@user_passes_test(lambda u: u.is_superuser)
def applyConfig(request):
    for_numbers = request.POST.getlist('needToForward')
    ForwardNumber.objects.all().delete()
    message = "Forward numbers set successfully ["
    for num in for_numbers:
        n = ForwardNumber(number_id=num)
        n.save()
        message += Staff.objects.get(pk=num).phone_number + ", "
    message += "]"
    context = {'message': message}
    return render(request, 'manager/done.html', context)

def utc_to_local(t):
    utc = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
    UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
    local_datetime = utc - UTC_OFFSET_TIMEDELTA
    return local_datetime.strftime("%Y-%m-%d %H:%M:%S")

@user_passes_test(lambda u: u.is_superuser)
def getInLogs(request):
    index = request.GET.get('index')
    data = serializers.serialize("json", InSMS.objects.all()[index:])
    return HttpResponse(data)

@user_passes_test(lambda u: u.is_superuser)
def getOutLogs(request):
    index = request.GET.get('index')
    data = serializers.serialize("json", OutSMS.objects.all()[index:])
    return HttpResponse(data)

@user_passes_test(lambda u: u.is_superuser)
def getUserInLogs(request):
    index = request.GET.get('index')
    num = request.GET.get('num')
    data = serializers.serialize("json", InSMS.objects.filter(sender=num)[index:])
    return HttpResponse(data)

@user_passes_test(lambda u: u.is_superuser)
def getUserOutLogs(request):
    index = request.GET.get('index')
    num = request.GET.get('num')
    data = serializers.serialize("json", OutSMS.objects.filter(receiver=num)[index:])
    return HttpResponse(data)

@user_passes_test(lambda u: u.is_superuser)
def getUserLogsByNum(request):
    number = request.GET.get('number')
    inSMS_list = InSMS.objects.filter(sender=number).order_by('-timestamp')
    outSMS_list = OutSMS.objects.filter(receiver=number).order_by('-timestamp')
    context = {'inSMS_list': inSMS_list, 'outSMS_list': outSMS_list, 'num': number}
    return render(request, 'manager/userlogs.html', context)

def login_view(request):
    if request.session.get('login', False) or request.user.is_authenticated():
        return HttpResponse("You have logged in, " + request.user.username)
    return render(request, 'manager/login.html')

def welcome(request):
    userID = request.POST.get('userID')
    fbToken = request.POST.get('fbToken')
    if fbToken is not None and userID is not None:
        request.session['login'] = True
        return HttpResponse("token: " + fbToken + " userID: " + userID)
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            request.session['login'] = True
            return HttpResponse("Nice to see you back, " + user.first_name)
        else:
            return HttpResponse("user is inactive!")
    else:
        return HttpResponse("can't found user")

def logout_view(request):
    logout(request)
    try:
        del request.session['login']
    except KeyError:
        pass 
    return HttpResponse("logout succeccfully")

def register_view(request):
    return render(request, 'manager/register.html')

def tregister_view(request):
    return render(request, 'manager/tregister.html')

def createUser(request):
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    user = User.objects.create_user(email, email, password,
        first_name=first_name, last_name=last_name)
    customer = Customer(user=user, phone=phone)
    customer.save()
    return HttpResponse("Hello, " + customer.user.first_name)

@transaction.atomic
def createTherapist(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    user = User.objects.create_user(email, email, password,
        first_name=first_name, last_name=last_name)
    phone = request.POST.get('phone')
    gender = request.POST.get('gender')
    home_address = request.POST.get('home_address')
    availability = request.POST.get('availability')
    experience = request.POST.get('experience')
    specialty = request.POST.get('specialty')
    emergency_contact_name = request.POST.get('emergency_contact_name')
    emergency_contact_phone = request.POST.get('emergency_contact_phone')
    supplementary = request.POST.get('supplementary')
    therapist = Therapist(user=user, phone=phone, gender=gender, home_address=home_address,
        availability=availability, experience=experience, specialty=specialty, emergency_contact_name=emergency_contact_name,
        emergency_contact_phone=emergency_contact_phone, supplementary=supplementary,
        massage_license=request.FILES['massage_license'], driver_license=request.FILES['driver_license'])
    therapist.save()
    return HttpResponse("Thank you for registering MassagePanda, " + therapist.user.first_name)
