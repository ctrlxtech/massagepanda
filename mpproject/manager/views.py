import base64
import pytz
import csv
import json
import re
import time
import urllib2
import datetime

import requests
import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.mail import EmailMultiAlternatives
from django.db import connection, transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import Context
from django.template.defaulttags import register
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt

import therapist_pb2
from customers.models import Address, Customer
from feedback.models import Feedback
from manager.models import (Area, ForwardNumber, ForwardSMS, InSMS, Interval, OutSMS,
                            Schedule, SMSTemplate, Staff, Therapist)
from payment.models import Coupon, Order, OrderTherapist, ServiceCoupon
from referral.models import CustomerReferralCode, CustomerReferralHistory
from services.models import Group, Service

# Create your views here.
def applyHeaders(res):
    res['Access-Control-Allow-Origin'] = "*"
    res['Access-Control-Allow-Methods'] = "GET,POST"
    res['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
    return res

def getTherapist(request):
    try:
      jsonRequest = json.loads(request.body)
      return getTherapistFromJson(jsonRequest)
    except:
      return None

def getTherapistFromJson(data):
    try:
        uidb64 = data['uid']
        uid = force_text(urlsafe_base64_decode(uidb64))
        UserModel = get_user_model()
        return UserModel._default_manager.get(pk=uid).therapist
    except:
        return None

@csrf_exempt
def getRequestlist(request):
    therapist = getTherapist(request)
    if therapist:
      orders = Order.objects.filter(ordertherapist__id__isnull=True).order_by('created_at')
      order_list = buildOrderListProto(orders)
      jsonRes = HttpResponse(order_list.SerializeToString(), content_type="application/octet-stream")
    else:
      jsonRes = HttpResponse("Invalid request")
 
    return applyHeaders(jsonRes)

@csrf_exempt
def getOrderlist(request):
    therapist = getTherapist(request)

    if therapist:
      orders = Order.objects.filter(ordertherapist__therapist=therapist).order_by('service_datetime')

      order_list = buildOrderListProto(orders)

      jsonRes = HttpResponse(order_list.SerializeToString(), content_type="application/octet-stream")
    else:
      jsonRes = HttpResponse("Invalid request")
      
    return applyHeaders(jsonRes)

def buildOrderListProto(orders):
    order_list = therapist_pb2.OrderList()
    for data in orders:
      order = order_list.order.add()

      order.id = data.id.hex
      order.external_id = str(data.external_id)
      order.service_time = datetimeToEpoch(data.service_datetime)
      order.service_duration = int(data.service.service_time * 60)
      order.service_type = str(data.service.service_type)
      order.order_status = int(data.status)
      order.earn = data.service.labor_cost

      stubs = data.shipping_address.split(', ')
      order.address.address_line = str(stubs[0])
      order.address.city = str(stubs[1])
      order.address.state = str(stubs[2])
      country_and_zipcode = stubs[3].split(' ')
      order.address.country = str(country_and_zipcode[0])
      order.address.zipcode = str(country_and_zipcode[1])
      recipient = data.recipient.split(' ')
      order.customer_name = str(recipient[0] + ' ' + recipient[-1][0])
      order.creation_time = datetimeToEpoch(data.created_at)
    return order_list

@csrf_exempt
def getSchedule(request):
    therapist = getTherapist(request)

    if therapist:
      schedule = therapist.schedule_set.all()
      schedule_list = buildScheduleProto(schedule)
      jsonRes = HttpResponse(schedule_list.SerializeToString(), content_type="application/octet-stream")
    else:
      jsonRes = JsonResponse({'error': "Invalid request"})
 
    return applyHeaders(jsonRes)

def buildScheduleProto(data):
    schedule_list = therapist_pb2.Schedule()
    for item in data:
        slot = schedule_list.slot.add()
        slot.status = int(item.active)
        slot.day = int(item.day)
        intervals = item.interval_set.all()
        for intvl in intervals:
            interval = slot.interval.add()
            interval.start_time = timeToSeconds(intvl.starttime)
            interval.end_time = timeToSeconds(intvl.endtime)
    return schedule_list

@csrf_exempt
@transaction.atomic
def updateSchedule(request):
    try:
      jsonRequest = json.loads(request.body)
    except:
      jsonRes = JsonResponse({'status': 'error'})
      return applyHeaders(jsonRes)

    therapist = getTherapistFromJson(jsonRequest)
    schedule_list = jsonRequest["schedule_list"]
    for slot in schedule_list["slot"]:
      schedule = therapist.schedule_set.filter(day=slot["day"])
      if not schedule:
        schedule = Schedule(day=slot["day"], therapist=therapist, active=False)
        schedule.save()
      else:
        schedule[0].interval_set.all().delete()
        schedule = schedule[0]
      for interval in slot["interval"]:
        intvl = Interval(schedule=schedule, starttime=secondsToTime(interval["start_time"]),
                         endtime=secondsToTime(interval["end_time"]))
        intvl.save()
    jsonRes = JsonResponse({'status': 'success'})
    return applyHeaders(jsonRes)

@csrf_exempt
@transaction.atomic
def processAction(request):
    try:
      jsonRequest = json.loads(request.body)
      therapist = getTherapistFromJson(jsonRequest)
      order = Order.objects.get(id=jsonRequest["order_id"])
      action = jsonRequest["action"]
      if action == 0: # Accept order
        ot = OrderTherapist(order=order, therapist=therapist)
        ot.save()
        pass
      elif action == 1: # Check in
        pass
      elif action == 2: # Check out
        pass
      elif action == 3: # Emergency
        pass
      
      jsonRes = JsonResponse({'status': 'success'})
    except:
      jsonRes = JsonResponse({'status': 'failure', 'error': "Invalid request"})
 
    return applyHeaders(jsonRes)


def timeToSeconds(daytime):
    return daytime.hour * 3600 + daytime.minute * 60 + daytime.second

def secondsToTime(seconds):
    seconds = int(seconds)
    hours = seconds/3600
    secondsRemain = seconds%3600
    minutes = secondsRemain/60
    secondsRemain = minutes%60
    return datetime.time(hours, minutes, secondsRemain)

def datetimeToEpoch(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    naive = dt.replace(tzinfo=None)
    return int((naive - epoch).total_seconds() * 1000)

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

@user_passes_test(lambda u: u.is_superuser)
def sendEmail(request):
    order_list = Order.objects.filter(ordertherapist__id__isnull=False)
    context = {'order_list': order_list}
    return render(request, 'manager/email.html', context)

@login_required
def sendMyEmail(request):
    stripe.api_key = settings.STRIPE_KEY
    order = Order.objects.get(pk='2d5b4b009046465aa04d48849fde2a89')
    stripeToken = stripe.Token.retrieve(order.stripe_token)
    subject, from_email, to = 'Your Coupon!', settings.SERVER_EMAIL, 'yuechen1989@gmail.com'
    text_content = 'This is an email containing your coupon.'
    html_content = get_template('payment/order_shipped_email.html').render(Context({'order': order, 'stripeToken': stripeToken}))
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse("Email sent!") 

@user_passes_test(lambda u: u.is_superuser)
def sendFeedbackEmails(request):
    orderIds = request.POST.getlist('orderIds')
    for orderId in orderIds:
        sendFeedbackEmail(request, orderId)
    return HttpResponse("Email sent!") 

def sendFeedbackEmail(request, orderId):
    order = Order.objects.get(pk=orderId)
    f = order.feedback

    ot = order.ordertherapist_set.all()
    from_email = settings.SERVER_EMAIL
    subject = 'How do you like ' + ot[0].therapist.user.first_name 
    if len(ot) > 1:
        subject += ' and ' + ot[1].therapist.user.first_name
    subject += ' - Your Feedback is Important to Us'
    text_content = 'We really appreciate your feedback!'
    current_site = get_current_site(request)
    host = "http://" + current_site.domain
    html_content = get_template('feedback/feedbackEmail.html').render(Context({'order': order, 'host': host, 'code': f.code.hex}))
    msg = EmailMultiAlternatives(subject, text_content, from_email, [Order.objects.get(pk=orderId).email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    f.request_count += 1
    f.save()

    return

def test(request):
    name = "Mr. unknown"
    if request.POST.get('name'):
      name = request.POST.get('name')
    return pushIO()
    context = {'status': 'success', 'message': "Hello, " + name}
        
    json = JsonResponse(context)
    json['Access-Control-Allow-Origin'] = "*"
    return json

def pushIO():
    payload = {'user_ids': ['fe3b6ed1-330e-4a0e-a05d-916e6357b8fb'], 'production': False, 'notification': { 'alert': 'MassagaPanda'}}
    private_key = "d03a2dc3aa95b5884312c4102b731f54fc70a9d2a8479fd9"
    b64 = base64.encodestring('%s:' % private_key).replace('\n', '')
    auth = "Basic %s" % b64
    headers = {'Content-type': 'application/json', 'X-Ionic-Application-Id': 'ce70fa55', 'Authorization': auth}
    url = 'https://push.ionic.io/api/v1/push'
    return HttpResponse(requests.post(url, data=json.dumps(payload), headers=headers))

@login_required(login_url="/manager/login")
def customerProfile(request):
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
        order_tl.append(stripe.Token.retrieve(order.stripe_token))
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

    o = Order.objects.get(stripeToken=mtoken)
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
    staff_list = Staff.objects.filter(suspended=False).exclude(area__areacode=10).order_by('first_name')
    template_list = SMSTemplate.objects.all()
    area_list = Area.AREA_CHOICES[:4]
    context = {'staff_list': staff_list, 'template_list': template_list, 'area_list': area_list}
    return render(request, 'manager/sms.html', context)

@user_passes_test(lambda u: u.is_superuser)
def chicago(request):
    staff_list = Staff.objects.filter(suspended=False, area__areacode=10).order_by('first_name')
    template_list = SMSTemplate.objects.all()
    area_list = Area.AREA_CHOICES[4:]
    context = {'staff_list': staff_list, 'template_list': template_list, 'area_list': area_list, 'is_chicago': True}
    return render(request, 'manager/sms.html', context)

@user_passes_test(lambda u: u.is_superuser)
def getContactList(request):
    genderList = request.POST.getlist("gender")

    area = request.POST.get("areacode")
    contact_list = []
    for gender in genderList:
        contact_list += Staff.objects.filter(area__areacode=area, gender=gender, suspended=False)
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
            f = ForwardSMS(staff=staff, receiver=n, messageBody=message_body, timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            f.save()
        else:
            o = OutSMS(staff=staff, receiver=n, messageBody=message_body, timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
    
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
    utc = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
    UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
    local_datetime = utc - UTC_OFFSET_TIMEDELTA
    return local_datetime.strftime("%Y-%m-%d %H:%M:%S")

@user_passes_test(lambda u: u.is_superuser)
def logs(request):
    return render(request, 'manager/logs.html')

@user_passes_test(lambda u: u.is_superuser)
def allLogs(request):
    return render(request, 'manager/allLogs.html')

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
        " on manager_forwardsms.receiver = manager_staff.phone_number where manager_forwardsms.id > %s ORDER BY manager_forwardsms.id ASC", (index))
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
        " on manager_insms.sender = manager_staff.phone_number where timestamp <= %s and timestamp > %s ORDER BY manager_insms.timestamp DESC", (oldTimestamp, newTimestamp))
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
        " on manager_insms.sender = manager_staff.phone_number where manager_insms.id > %s and timestamp > %s ORDER BY manager_insms.timestamp DESC", (index, timestamp))
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
        " on manager_outsms.receiver = manager_staff.phone_number where timestamp <= %s and timestamp > %s ORDER BY manager_outsms.id DESC", (oldTimestamp, newTimestamp))
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
        " on manager_outsms.receiver = manager_staff.phone_number where manager_outsms.id > %s and timestamp > %s ORDER BY manager_outsms.id DESC", (index, timestamp))
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
def logsByNum(request):
    context = {'number': request.POST.get('number'), 'byNum': True}
    return render(request, 'manager/logs.html', context)

@user_passes_test(lambda u: u.is_superuser)
def getInLogsByNum(request):
    number = request.POST.get('number')
    cursor = connection.cursor()
    cursor.execute("select manager_insms.id, manager_insms.sender, manager_insms.timestamp," \
        " manager_staff.first_name, manager_staff.last_name," \
        " manager_insms.messageBody from manager_insms left join manager_staff" \
        " on manager_insms.sender = manager_staff.phone_number where manager_insms.sender = %s ORDER BY manager_insms.id DESC", (number))
    data = dictfetchall(cursor)
    return JsonResponse(data, safe=False)

@user_passes_test(lambda u: u.is_superuser)
def getOutLogsByNum(request):
    number = request.POST.get('number')
    cursor = connection.cursor()
    cursor.execute("select manager_outsms.id, manager_outsms.receiver, manager_outsms.timestamp," \
        " manager_staff.first_name, manager_staff.last_name," \
        " manager_outsms.messageBody from manager_outsms left join manager_staff" \
        " on manager_outsms.receiver = manager_staff.phone_number where manager_outsms.receiver = %s ORDER BY manager_outsms.id DESC", (number))
    data = dictfetchall(cursor)
    return JsonResponse(data, safe=False)

def register_view(request):
    return render(request, 'manager/register.html')

def tregister_view(request):
    return render(request, 'manager/tregister.html')

def getPhone(data):
    phone = str(data.get('phone'))
    phone = filter(str.isdigit, phone)
    phone = re.sub("[^0-9]", "", phone)
    if len(phone) == 10:
        phone = "1" + phone
    return phone

@transaction.atomic
def createTherapist(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    user = User.objects.create_user(email, email, password,
        first_name=first_name, last_name=last_name)
    phone = getPhone(request.POST)
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
    routing_number = request.POST.get('routing_number')
    account_number = request.POST.get('account_number')
    supplementary = request.POST.get('supplementary')
    therapist = Therapist(user=user, phone=phone, gender=gender, home_address=home_address,
        availability=availability, working_area=working_area, experience=experience, specialty=specialty,
        emergency_contact_name=emergency_contact_name, emergency_contact_phone=emergency_contact_phone,
        account_number=account_number, routing_number=routing_number, supplementary=supplementary,
        massage_license=request.FILES['massage_license'], driver_license=request.FILES['driver_license'])
    therapist.save()
    return HttpResponse("Thank you for registering MassagePanda, " + therapist.user.first_name)

@user_passes_test(lambda u: u.is_superuser)
def addCoupons_view(request):
    serviceGroups = Group.objects.all()
    context = {'service_groups': serviceGroups}
    return render(request, 'manager/addCoupons.html', context)

@transaction.atomic
def addCoupon(request):
    couponCode = request.POST.get('couponCode')
    groupId = request.POST.get('serviceGroup')
    group = Group.objects.get(pk=groupId)
    isFlat = request.POST.get('isFlat')
    startDate = request.POST.get('start_date')
    endDate = request.POST.get('end_date')
    startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    if not isFlat:
        isFlat = False
    discount = request.POST.get('discount')
    quantity = request.POST.get('quantity')

    coupon = Coupon(code=couponCode, discount=discount, quantity=quantity, used=0, start_date=startDate, end_date=endDate, is_flat=isFlat)
    coupon.save()

    sgs = group.servicegroup_set.all()
    for sg in sgs:
        sc = ServiceCoupon(service=sg.service, coupon=coupon)
        sc.save()

    return HttpResponse("Coupon added")

def toCSV(rows):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    for row in rows:
      writer.writerow(row)
    return response

@login_required(login_url="/customer/login")
def paystub(request):
    context = {}
    return render(request, 'manager/stub.html', context)

def isInSF(order):
    stubs = order.shipping_address.split(', ')
    country_and_zipcode = stubs[-1].split(' ')
    zipcode = str(country_and_zipcode[1])

    try:
      if int(zipcode) in settings.SF_ZIPCODES:
        return True
      else:
        return False
    except:
        return False

def getTherapistWage(therapist, startDate, endDate):
    tz = pytz.timezone('US/Pacific')
    wages = []
    wages.append(therapist.user.first_name)
    for ot in therapist.ordertherapist_set.filter(order__service_datetime__range=(startDate, endDate)).order_by('order__service_datetime'):
      wages.append(ot.order.service_datetime.astimezone(tz=tz).strftime('%b-%d-%y %H:%M:%S'))
      if ot.order.status == 3 or ot.order.status == 6:
        laborCost = ot.order.labor_adjustment
      else:  
        laborCost = ot.order.service.labor_cost + ot.order.labor_adjustment
        if isInSF(ot.order) and ot.order.need_table:
          laborCost += 10

      if ot.order.coupon and ot.order.coupon.is_gilt:
        wages.append(True)
        laborCost -= 5
      else:
        wages.append(False)
      wages.append(laborCost)
    return wages

def wageListToJson(wages):
    result = wages[0]
    result += "<br>"
    result += "Service time, is gilt city, you earn<br>"
    count = 0;
    for wage in wages[1:]:
        result += str(wage)
        if count == 2:
            result += "<br>"
            count = 0
        else:
            result += ", "
            count += 1
    return result

@login_required(login_url="/customer/login")
def getWage(request):
    startDate = datetime.datetime.strptime(request.POST.get("startDate"), "%Y-%m-%d")
    endDate = datetime.datetime.strptime(request.POST.get("endDate"), "%Y-%m-%d")
    if request.user.is_superuser:
      therapistWage = []
      for therapist in Therapist.objects.all():
        therapistWage.append(getTherapistWage(therapist, startDate, endDate))
      return toCSV(therapistWage)
    else:
      return HttpResponse(wageListToJson(getTherapistWage(request.user.therapist, startDate, endDate)))
