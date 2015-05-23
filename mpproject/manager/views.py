from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import connection

from django.template.defaulttags import register

from django.http import HttpResponse, JsonResponse
from manager.models import Staff, InSMS, OutSMS, ForwardNumber, SMSTemplate
from payment.models import Order, Charge
import requests
import json
import time
import datetime
import stripe
# Create your views here.
@login_required
def payment(request):
    return render(request, 'manager/payment.html')

def placeOrder(request):
    '''
    serviceId = request.POST.get("serviceId")
    service = Service.objects.get(pk=serviceId)
    fee = int(float(service.service_fee) * 100)
    '''
    livemode = request.POST.get('livemode')
    mamount = request.POST.get('amount')
    if livemode is not None:
        stripe.api_key = "sk_live_4oD38m4mvOMOba8TlT2cqi3A"
    else:
        stripe.api_key = "sk_test_jcGeofOhYGQw7BPl3UPGP0lh"

    # Get the credit card details submitted by the form
    token = request.POST.get('stripeToken', False)
    b_phone = request.POST.get('b_phone', "unknown_billing_phone")
    b_email = request.POST.get('b_email', "unknown_billing_email")

    name = request.POST.get('name', "unknown_name")
    phone = request.POST.get('phone', "unknown_phone")
    email = request.POST.get('email', "unknown_email")
    sa = request.POST.get('al1') 
    o = Order(token=token, amount=mamount, b_phone=b_phone, b_email=b_email, shipping_address=sa, name=name, phone=phone, email=email)
    o.save()
    return HttpResponse("Successfully placed order")

@login_required
def orders(request):
    order_list = Order.objects.filter(charged=False)
    charge_list = Charge.objects.all()
    order_tl = []
    charge_tl = []
    stripe.api_key = "sk_live_4oD38m4mvOMOba8TlT2cqi3A"
    #stripe.api_key = "sk_test_jcGeofOhYGQw7BPl3UPGP0lh"
    for order in order_list:
        order_tl.append(stripe.Token.retrieve(order.token))
    for charge in charge_list:
        charge_tl.append(stripe.Charge.retrieve(charge.token))
    #return HttpResponse(token_list)
    context = {'order_list': order_list, 'order_tl': order_tl, 'charge_list': charge_list, 'charge_tl': charge_tl}
    return render(request, 'manager/orders.html', context)

@login_required
def getOrders(request):
    index = request.GET.get('index')
    data = serializers.serialize("json", Order.objects.filter(charged=False)[index:])
    return HttpResponse(data)

@register.filter
def lookup(d, key):
    return d[key]

def mcharge(request):
    mtoken = request.POST.get('token')
    mamount = request.POST.get('amount')
    b_phone = request.POST.get('b_phone')
    b_email = request.POST.get('b_email')
    mname = request.POST.get('name')
    mphone = request.POST.get('phone')
    memail = request.POST.get('email')
    sa = request.POST.get('sa')
    stripe.api_key = "sk_live_4oD38m4mvOMOba8TlT2cqi3A"
    #stripe.api_key = "sk_test_jcGeofOhYGQw7BPl3UPGP0lh"
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

    c = Charge(token=mtoken, shipping_address=sa, name=mname, phone=mphone, email=memail)
    c.save()
    return JsonResponse(chargeObj)
    '''
    r = token + "<br>" + al1 + "<br>" + al2
    return HttpResponse(r)
    '''

@login_required
def index(request):
    staff_list = Staff.objects.order_by('first_name')
    template_list = SMSTemplate.objects.all()
    context = {'staff_list': staff_list, 'template_list': template_list}
    return render(request, 'manager/sms.html', context)

@login_required
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

@login_required
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
    #numbers = [16056596655, 12133790752, 14128889022]
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

@login_required
def configurations(request):
    staff_list = Staff.objects.order_by('first_name')
    context = {'staff_list': staff_list, 'for_staff': Staff.objects.filter(forwardnumber__number_id__isnull=False)}
    return render(request, 'manager/configurations.html', context)

@login_required
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

@login_required
def getInLogs(request):
    index = request.GET.get('index')
    data = serializers.serialize("json", InSMS.objects.all()[index:])
    return HttpResponse(data)

@login_required
def getOutLogs(request):
    index = request.GET.get('index')
    data = serializers.serialize("json", OutSMS.objects.all()[index:])
    return HttpResponse(data)

@login_required
def getUserInLogs(request):
    index = request.GET.get('index')
    num = request.GET.get('num')
    data = serializers.serialize("json", InSMS.objects.filter(sender=num)[index:])
    return HttpResponse(data)

@login_required
def getUserOutLogs(request):
    index = request.GET.get('index')
    num = request.GET.get('num')
    data = serializers.serialize("json", OutSMS.objects.filter(receiver=num)[index:])
    return HttpResponse(data)

@login_required
def getUserLogsByNum(request):
    number = request.GET.get('number')
    inSMS_list = InSMS.objects.filter(sender=number).order_by('-timestamp')
    outSMS_list = OutSMS.objects.filter(receiver=number).order_by('-timestamp')
    context = {'inSMS_list': inSMS_list, 'outSMS_list': outSMS_list, 'num': number}
    return render(request, 'manager/userlogs.html', context)
