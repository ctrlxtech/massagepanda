from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.db import connection
from django.contrib.auth.decorators import user_passes_test

from django.template.defaulttags import register

from django.http import HttpResponse, JsonResponse
from manager.models import Staff, Area, Therapist, InSMS, OutSMS, ForwardNumber, SMSTemplate
from payment.models import Order, Charge
from django.contrib.auth.models import User
from customers.models import Customer, Address
from django.db import transaction
import requests
import json
import time
import datetime
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
def terms(request):
    return render(request, 'manager/terms.html')

def privacy(request):
    return render(request, 'manager/privacy.html')

def logtest(request):
    index = 105
    data = InSMS.objects.all()[index:]
    data = serializers.serialize("json", data)
    return HttpResponse(data)

@login_required
def test(request):
    index = 105
    data = list(InSMS.objects.all()[index:])
    data[0].first_name = "Kevin"
    d = list(data)
    data = serializers.serialize("json", d)
    return HttpResponse(d[0].first_name)
    context = {"data": data}
    return render(request, 'manager/test.html', context) 
    return HttpResponse(data)
    context = ""

    if request.user.is_authenticated():
        context += "Had been Authenticated: <br>"
    else:
        context += "Had not!<br>"
    '''
    user = authenticate(username="paul@gmail.com", password="1234")
    if user is not None:
        if user.is_active:
            request.user = user
            return login(request, user)
            # Redirect to a success page.
            context += "hello, " + user.username
        else:
            # Return a 'disabled account' error message
            context += "User is not active"
    else:
        # Return an 'invalid login' error message.
        context += "User not found"
    if request.user.is_authenticated():
        context += "<br> Authenticated: " + request.user.username
    else:
        context += "<br>Not"
    '''
    return HttpResponse(context)

def customerProfile(request):
    customerId = request.GET.get('id')
    customer = "Customer not found"
    stripe.api_key = settings.STRIPE_KEY
    stripeCustomer = ""
    try:
        customer = Customer.objects.get(pk=customerId)
        shippingAddress = Address.objects.filter(customer=customer)

        stripeCustomer = stripe.Customer.retrieve(customer.stripe_customer_id)
    except:
        pass
    context = {'customer': customer, 'shippingAddress': shippingAddress, 'stripeCustomer': stripeCustomer}
    return render(request, 'manager/profile.html', context) 

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

def payment(request):
    customer = None
    stripeCustomer = None

    if request.user.is_authenticated():
        if hasattr(request.user, 'customer'):
            customer = request.user.customer
            stripe.api_key = settings.STRIPE_KEY
            try:
                stripeCustomer = stripe.Customer.retrieve(customer.stripe_customer_id)
            except:
                pass

    context = {'customer': customer, 'stripeCustomer': stripeCustomer}

    return render(request, 'manager/payment.html', context)

def placeOrder(request):
    data = json.loads(request.body)
    mamount = data.get('amount')
    mamount = float(mamount) * 100
    # Get the credit card details submitted by the form
    token = data.get('stripeToken')
    bPhone = data.get('phone')
    bEmail = data.get('email')
    
    customer = None;
    if request.user.is_authenticated():
        try:
            customer = request.user.customer
        except:
            pass
    name = data.get('first-name')
    name += " " + data.get('last-name')
    phone = data.get('phone')
    email = data.get('email')
    sAL1 = data.get('al1').strip()
    sAL2 = data.get('al2')
    address = sAL1
    if sAL2 is not None and not sAL2:
        address = address + " " + sAL2.strip()
    sCity = data.get('city').strip()
    sCountry = data.get('country').strip()
    sState = data.get('state').strip()
    sZipcode = data.get('zipcode').strip()
    address = address + ", " + sCity + ", " + sState + ", " +\
        sCountry + " " + sZipcode

    o = Order(token=token, customer=customer, amount=mamount, b_phone=bPhone, b_email=bEmail, shipping_address=address, name=name, phone=phone, email=email)
    o.save()
    if customer is not None:
        # update customer's stripe default card
        stripe.api_key = settings.STRIPE_KEY
        cu = stripe.Customer.retrieve(customer.stripe_customer_id)
        cu.source = token
        cu.save()

        # add shipping address for the customer
        a = Address(customer=customer, address_line1=sAL1, address_line2=sAL2, zipcode=sZipcode, city=sCity, state=sState, country=sCountry)
        a.save()
    message_body = "Thank you for booking with MassagePanda! We are reaching out to our therapists now, and we'll let you know once anyone responds!"
    nums = [phone]
    sendSMS(nums, message_body)


    context = {'status': 'success'}
    return JsonResponse(context)

def placeOrderFromForm(request):
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
    if customer is not None:
        stripe.api_key = settings.STRIPE_KEY
        cu = stripe.Customer.retrieve(customer.stripe_customer_id)
        cu.source = token
        cu.save()
    message_body = "Thank you for booking with MassagePanda! We are reaching out to our therapists now, and we'll let you know once anyone responds!"
    nums = [phone]
    sendSMS(nums, message_body)

    context = {'status': 'success'}
    return JsonResponse(context)

@user_passes_test(lambda u: u.is_superuser)
def orders(request):
    order_list = Order.objects.filter(charged=False)
    charge_list = Charge.objects.all()
    order_tl = []
    charge_tl = []
    stripe.api_key = settings.STRIPE_KEY
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

@register.filter
def staffNumLookup(d, key):
    return Staff.objects.get(pk=key).phone_number


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
    stripe.api_key = settings.STRIPE_KEY
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
    area_list = Area.AREA_CHOICES
    context = {'staff_list': staff_list, 'template_list': template_list, 'area_list': area_list}
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

@user_passes_test(lambda u: u.is_superuser)
def getContactList(request):
    genderList = request.POST.getlist("gender")
    area = request.POST.get("areacode")
    contact_list = []
    for gender in genderList:
        contact_list += Staff.objects.filter(area__areacode=area, gender=gender)
    data = serializers.serialize("json", contact_list)
    return HttpResponse(data)


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
    r = sendSMS(nums, message_body)
    return HttpResponse(r)

@user_passes_test(lambda u: u.is_superuser)
def sendWithNum(request):
    number = request.POST.get('num')
    message_body = request.POST.get('message')
    nums = [number]
    r = sendSMS(nums, message_body)
    return HttpResponse(r)

def sendSMS(nums, message_body):
    api_key = settings.NEXMO_KEY
    api_secret = settings.NEXMO_SECRET
    r = []
    for n in nums:
        payload = {'api_key': api_key, 'api_secret': api_secret, 'from': "12069396577", 'to': n, 'type': 'unicode', 'text': message_body} 
        r.append(requests.get("https://rest.nexmo.com/sms/json", params=payload).text)
        staff = Staff.objects.filter(phone_number=n)
        o = OutSMS(staff=staff[0], receiver=n, messageBody=message_body, timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        o.save()
        time.sleep(1)

    return r

def receiveSMS(request):
    msisdn = request.GET.get('msisdn')
    message_body = request.GET.get('text')
    time_stamp = request.GET.get('message-timestamp')

    if (time_stamp is None or msisdn is None or message_body is None):
        return HttpResponse("***Error request")
    
    time_stamp = utc_to_local(time_stamp)
    staff = Staff.objects.filter(phone_number=msisdn)
    i = InSMS(staff=staff[0], sender=msisdn, messageBody=message_body, timestamp=time_stamp)
    i.save()

    message_body += "[sent by " + msisdn + " at " + time_stamp + "]"
    for_numbers = ForwardNumber.objects.all()
    nums = []
    for num in for_numbers:
        nums.append(Staff.objects.get(pk=num.number_id).phone_number)
    sendSMS(nums, message_body);

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
    cursor = connection.cursor()
    cursor.execute("select manager_insms.sender, manager_insms.timestamp," \
        " manager_staff.first_name, manager_staff.last_name," \
        " manager_insms.messageBody from manager_insms left join manager_staff" \
        " on manager_insms.sender = manager_staff.phone_number where manager_insms.id > " + index + " ORDER BY manager_insms.id DESC")
    data = dictfetchall(cursor)
    return JsonResponse(data, safe=False)

@user_passes_test(lambda u: u.is_superuser)
def getOutLogs(request):
    index = request.GET.get('index')
    cursor = connection.cursor()
    cursor.execute("select manager_outsms.receiver, manager_outsms.timestamp," \
        " manager_staff.first_name, manager_staff.last_name," \
        " manager_outsms.messageBody from manager_outsms left join manager_staff" \
        " on manager_outsms.receiver = manager_staff.phone_number where manager_outsms.id > " + index + " ORDER BY manager_outsms.id DESC")
    data = dictfetchall(cursor)
    return JsonResponse(data, safe=False)

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

@transaction.atomic
def createCustomer(request):
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    gender = request.POST.get('gender')
    user = User.objects.create_user(email, email, password,
        first_name=first_name, last_name=last_name)
    full_name = first_name + " " + last_name
    stripe.api_key = settings.STRIPE_KEY

    stripe_cus = stripe.Customer.create(
        description=full_name,
        email=email
    )
    customer = Customer(user=user, stripe_customer_id=stripe_cus['id'], gender=gender, phone=phone)
    customer.save()

    context = {'customer': customer}
    return render(request, 'manager/welcome.html', context) 

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
    home_address = buildAddress(request)
    availability = request.POST.get('availability')
    working_area = request.POST.get('working_area')
    experience = request.POST.get('experience')
    specialty = request.POST.get('specialty')
    emergency_first_name = request.POST.get('emergency_first_name')
    emergency_last_name = request.POST.get('emergency_last_name')
    emergency_contact_name = emergency_first_name.strip() + "" + emergency_last_name.strip()
    emergency_contact_phone = request.POST.get('emergency_phone')
    supplementary = request.POST.get('supplementary')
    therapist = Therapist(user=user, phone=phone, gender=gender, home_address=home_address,
        availability=availability, working_area=working_area, experience=experience, specialty=specialty,
        emergency_contact_name=emergency_contact_name, emergency_contact_phone=emergency_contact_phone, supplementary=supplementary,
        massage_license=request.FILES['massage_license'], driver_license=request.FILES['driver_license'])
    therapist.save()
    return HttpResponse("Thank you for registering MassagePanda, " + therapist.user.first_name)
