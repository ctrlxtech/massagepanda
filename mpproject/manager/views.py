from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import connection

from django.http import HttpResponse
from manager.models import Staff, InSMS, OutSMS, ForwardNumber
import requests
import json
import time
import datetime
# Create your views here.
@login_required
def index(request):
    staff_list = Staff.objects.order_by('first_name')
    context = {'staff_list': staff_list}
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
    ppl = request.POST.getlist('needToSend')
    message_body = request.POST.get('message')
    number = ""
    api_key = "412847f0"
    api_secret = "55f41401"
    r = ""
    for p in ppl:
        number = str(Staff.objects.get(pk=p).phone_number)
        payload = {'api_key': api_key, 'api_secret': api_secret, 'from': "12069396577", 'to': number, 'type': 'unicode', 'text': message_body} 
        r += requests.get("https://rest.nexmo.com/sms/json", params=payload).text
        r += "<br>"
        o = OutSMS(receiver=number, messageBody=message_body, timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        o.save()
        time.sleep(1)
    return redirect('manager')

@login_required
def sendWithNum(request):
    number = request.POST.get('num')
    message_body = request.POST.get('messageWithNum')
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
