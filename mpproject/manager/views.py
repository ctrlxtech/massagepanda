from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.db import connection
from django.contrib.auth.decorators import user_passes_test

from django.template.defaulttags import register

from django.http import HttpResponse, JsonResponse
from manager.models import Staff, Area, Therapist, InSMS, OutSMS, ForwardSMS, ForwardNumber, SMSTemplate
from payment.models import Order, OrderTherapist
from services.models import Service
from referral.models import CustomerReferralCode, CustomerReferralHistory
from django.contrib.auth.models import User
from customers.models import Customer, Address
from django.db import transaction
import requests
import json
import time
from datetime import datetime
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives

from referral.views import referralCodeGenerator

from django.template.loader import get_template

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

def referralTest(request):
    code = request.GET.get("referCode")
    if code:
        try:
            referralObj = CustomerReferralCode.objects.get(code=code)
        except:
            return HttpResponse("Invalid code")
        return HttpResponse("Looks like you're referred by " + referralObj.customer.user.first_name)
    else:
        return HttpResponse("No code found")

@login_required
def sendMyEmail(request):
    subject, from_email, to = 'Your Coupon!', 'support@massagepanda.com', 'yuechen1989@gmail.com'
    text_content = 'This is an email containing your coupon.'
    html_content = get_template('manager/hello.html').render()
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse("Email sent!") 

@login_required
def test(request):
    plaintext = get_template('manager/hello.html')
    return HttpResponse(plaintext.render())


    user = User.objects.get(pk=11)
    user = authenticate(username=user.username, password=user.password)
    if user is not None:
        return HttpResponse(user.user)
    else:
        return HttpResponse("Can't")

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

@login_required(login_url="/manager/login")
def customerProfile(request):
    customerId = request.GET.get('id')
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
    except:
        return HttpResponse("No valid customer found(probably you are an admin?)")
    shippingAddress_list = None
    referralCode = None 
    stripe.api_key = settings.STRIPE_KEY
    stripeCustomer = ""
    try:
        referralCode = CustomerReferralCode.objects.get(customer=customer)
        referralHistory = CustomerReferralHistory.objects.filter(code_id=referralCode.id)
        shippingAddress_list = Address.objects.filter(customer=customer)
        stripeCustomer = stripe.Customer.retrieve(customer.stripe_customer_id)
    except:
        pass
    context = {'customer': customer, 'shippingAddress_list': shippingAddress_list,
        'stripeCustomer': stripeCustomer, 'referralCode': referralCode, 'referralHistory': referralHistory}
    return render(request, 'manager/profile.html', context) 

def buildAddress(request):
    address = request.POST.get('al1')
    address = address.strip()
    sAL2 = request.POST.get('al2')
    sAL2 = sAL2.strip()
    if sAL2 is not None and sAL2:
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

    service_list = Service.objects.all()
    context = {'customer': customer, 'stripeCustomer': stripeCustomer, 'service_list': service_list}

    return render(request, 'manager/payment.html', context)

def placeOrderFromJson(request):
    data = json.loads(request.body)
    return placeOrder(request, data);

def placeOrderFromPost(request):
    data = request.POST;
    return placeOrder(request, data);

def placeOrder(request, data):
    customer = None;
    if request.user.is_authenticated():
        try:
            customer = request.user.customer
        except:
            pass

    serviceId = data.get('service_id')
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
    return JsonResponse(context)

@user_passes_test(lambda u: u.is_superuser)
def assignTherapist(request):
    orderId = request.POST.get('pk')
    staffId = request.POST.get('value')
    orderTherapist = None
    orderTherapistList = OrderTherapist.objects.filter(order_id=orderId)
    if orderTherapistList is not None and orderTherapistList:
        for orderTherapist in orderTherapistList:
            if orderTherapist.staff_id != staffId:
                orderTherapist.staff_id = staffId
    else:
        orderTherapist = OrderTherapist(order_id=orderId, staff_id=staffId)
    if orderTherapist is not None:
        orderTherapist.save()
    staff = Staff.objects.get(pk=staffId)
    return HttpResponse(staff.id)

@user_passes_test(lambda u: u.is_superuser)
def orders(request):
    order_list = Order.objects.all()
    service_list = Service.objects.all()
    therapist_list = Staff.objects.filter(title=2)
    order_tl = []
    charge_tl = []
    stripe.api_key = settings.STRIPE_KEY
    for order in order_list:
        order_tl.append(stripe.Token.retrieve(order.token))
    '''
    for charge in charge_list:
        charge_tl.append(stripe.Charge.retrieve(charge.charge_token))
    '''
    context = {'order_list': order_list, 'order_tl': order_tl, 
        'therapist_list': therapist_list, 'service_list': service_list}
    return render(request, 'manager/orders.html', context)

@user_passes_test(lambda u: u.is_superuser)
def getOrders(request):
    index = request.GET.get('index')
    data = serializers.serialize("json", Order.objects.filter(charged=False)[index:])
    return HttpResponse(data)

@register.filter
def lookup(d, key):
    try:
        result = d[key]
        return result
    except:
        return

@register.filter
def lookupServiceType(d, key):
    try:
        for service in d:
            if service.id == key:
                return service.service_type
    except:
        return

@register.filter
def lookupOrderTherapist(d, key):
    orderTherapistList = OrderTherapist.objects.filter(order_id=key)
    return orderTherapistList

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
    if number is not None and number:
        nums.append(number)
    message_body = request.POST.get('message')
    r = sendSMS(nums, message_body, False)
    return HttpResponse(r)

@user_passes_test(lambda u: u.is_superuser)
def sendWithNum(request):
    number = request.POST.get('num')
    message_body = request.POST.get('message')
    nums = [number]
    r = sendSMS(nums, message_body, False)
    return HttpResponse(r)

def sendSMS(nums, message_body, isForward):
    api_key = settings.NEXMO_KEY
    api_secret = settings.NEXMO_SECRET
    r = []
    for n in nums:
        payload = {'api_key': api_key, 'api_secret': api_secret, 'from': "12069396577", 'to': n, 'type': 'unicode', 'text': message_body} 
        r.append(requests.get("https://rest.nexmo.com/sms/json", params=payload).text)
        staff = None
        try:
            staff = Staff.objects.get(phone_number=n)
        except:
            pass
        if isForward:
            f = ForwardSMS(staff=staff, receiver=n, messageBody=message_body, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            f.save()
        else:
            o = OutSMS(staff=staff, receiver=n, messageBody=message_body, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            o.save()

        time.sleep(1)

    return r

def receiveSMS(request):
    msisdn = request.GET.get('msisdn')
    message_body = request.GET.get('text')
    time_stamp = request.GET.get('message-timestamp')
    messageId = request.GET.get('messageId')

    if (time_stamp is None or msisdn is None or message_body is None):
        return HttpResponse("***Error request")
    
    time_stamp = utc_to_local(time_stamp)
    staff = None
    try:
        staff = Staff.objects.get(phone_number=msisdn)
    except:
        pass
    i = InSMS(staff=staff, messageId=messageId, sender=msisdn, messageBody=message_body, timestamp=time_stamp)
    i.save()

    message_body += "[sent by " + msisdn + " at " + time_stamp + "]"
    for_numbers = ForwardNumber.objects.all()
    nums = []
    for num in for_numbers:
        nums.append(Staff.objects.get(pk=num.number_id).phone_number)
    sendSMS(nums, message_body, True);

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
    utc = datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
    UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()
    local_datetime = utc - UTC_OFFSET_TIMEDELTA
    return local_datetime.strftime("%Y-%m-%d %H:%M:%S")

@user_passes_test(lambda u: u.is_superuser)
def logs(request):
    '''
    cursor = connection.cursor()
    cursor.execute("select manager_insms.id, manager_insms.sender, manager_insms.timestamp," \
        " manager_staff.first_name, manager_staff.last_name," \
        " manager_insms.messageBody from manager_insms left join manager_staff" \
        " on manager_insms.sender = manager_staff.phone_number ORDER BY manager_insms.id DESC")
    inSMS_list = dictfetchall(cursor)

    cursor.execute("select manager_outsms.id, manager_outsms.receiver, manager_outsms.timestamp," \
        " manager_staff.first_name, manager_staff.last_name," \
        " manager_outsms.messageBody from manager_outsms left join manager_staff" \
        " on manager_outsms.receiver = manager_staff.phone_number ORDER BY manager_outsms.id DESC")

    outSMS_list = dictfetchall(cursor)
    context = {'inSMS_list': inSMS_list, 'outSMS_list': outSMS_list}
    '''
    return render(request, 'manager/logs.html')

@user_passes_test(lambda u: u.is_superuser)
def forwardLogs(request):
    forwardSMS_list = ForwardSMS.objects.all().order_by('-timestamp');
    context = {'forwardSMS_list': forwardSMS_list}
    return render(request, 'manager/forwardLogs.html', context)

@user_passes_test(lambda u: u.is_superuser)
def getForwardLogs(request):
    index = request.GET.get('index')
    cursor = connection.cursor()
    cursor.execute("select manager_forwardsms.id, manager_forwardsms.receiver, manager_forwardsms.timestamp," \
        " manager_staff.first_name, manager_staff.last_name," \
        " manager_forwardsms.messageBody from manager_forwardsms left join manager_staff" \
        " on manager_forwardsms.receiver = manager_staff.phone_number where manager_forwardsms.id > " + index + " ORDER BY manager_forwardsms.id ASC")
    data = dictfetchall(cursor)
    return JsonResponse(data, safe=False)

@user_passes_test(lambda u: u.is_superuser)
def getOldInLogs(request):
    oldTimestamp = request.POST.get('oldTimestamp')
    newTimestamp = request.POST.get('newTimestamp')
    cursor = connection.cursor()
    cursor.execute("select manager_insms.id, manager_insms.sender, manager_insms.timestamp," \
        " manager_staff.first_name, manager_staff.last_name," \
        " manager_insms.messageBody from manager_insms left join manager_staff" \
        " on manager_insms.sender = manager_staff.phone_number where timestamp <= \"" + oldTimestamp + "\" and timestamp > \"" + newTimestamp + "\" ORDER BY manager_insms.id DESC")
    data = dictfetchall(cursor)
    return JsonResponse(data, safe=False)

@user_passes_test(lambda u: u.is_superuser)
def getNewInLogs(request):
    index = request.POST.get('index')
    timestamp = request.POST.get('timestamp')
    cursor = connection.cursor()
    cursor.execute("select manager_insms.id, manager_insms.sender, manager_insms.timestamp," \
        " manager_staff.first_name, manager_staff.last_name," \
        " manager_insms.messageBody from manager_insms left join manager_staff" \
        " on manager_insms.sender = manager_staff.phone_number where manager_insms.id > " + index + " and timestamp > \"" + timestamp + "\" ORDER BY manager_insms.id DESC")
    data = dictfetchall(cursor)
    return JsonResponse(data, safe=False)

@user_passes_test(lambda u: u.is_superuser)
def getOldOutLogs(request):
    oldTimestamp = request.POST.get('oldTimestamp')
    newTimestamp = request.POST.get('newTimestamp')
    cursor = connection.cursor()
    cursor.execute("select manager_outsms.id, manager_outsms.receiver, manager_outsms.timestamp," \
        " manager_staff.first_name, manager_staff.last_name," \
        " manager_outsms.messageBody from manager_outsms left join manager_staff" \
        " on manager_outsms.receiver = manager_staff.phone_number where timestamp <= \"" + oldTimestamp + "\" and timestamp > \"" + newTimestamp + "\" ORDER BY manager_outsms.id DESC")
    data = dictfetchall(cursor)
    return JsonResponse(data, safe=False)

@user_passes_test(lambda u: u.is_superuser)
def getNewOutLogs(request):
    index = request.POST.get('index')
    timestamp = request.POST.get('timestamp')
    cursor = connection.cursor()
    cursor.execute("select manager_outsms.id, manager_outsms.receiver, manager_outsms.timestamp," \
        " manager_staff.first_name, manager_staff.last_name," \
        " manager_outsms.messageBody from manager_outsms left join manager_staff" \
        " on manager_outsms.receiver = manager_staff.phone_number where manager_outsms.id > " + index + " and timestamp > \"" + timestamp + "\" ORDER BY manager_outsms.id DESC")
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
        context['error'] = "can't found user"
    return JsonResponse(context)


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
def createCustomer(data):
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    gender = data.get('gender')
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

    code = referralCodeGenerator()
    customerReferralCode = CustomerReferralCode(customer=customer, code=code)
    customerReferralCode.save()

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
