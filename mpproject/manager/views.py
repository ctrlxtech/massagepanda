from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import serializers

from django.http import HttpResponse
from manager.models import Staff, InSMS, OutSMS
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

def logs(request):
    inSMS_list = InSMS.objects.order_by('id')
    outSMS_list = OutSMS.objects.order_by('id')
    context = {'inSMS_list': inSMS_list, 'outSMS_list': outSMS_list}
    return render(request, 'manager/logs.html', context)

   
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
    return HttpResponse(r)

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
    for num in settings.FOR_NUMBERS:
        payload = {'api_key': api_key, 'api_secret': api_secret, 'from': "12069396577", 'to': num, 'type': 'unicode', 'text': message_body} 
        requests.get("https://rest.nexmo.com/sms/json", params=payload).text
        time.sleep(1)

    return HttpResponse()

def configurations(request):
    staff_list = Staff.objects.order_by('first_name')
    context = {'staff_list': staff_list}
    return render(request, 'manager/configurations.html', context)

def applyConfig(request):
    settings.FOR_NUMBERS = request.POST.getlist('needToForward')
    message = "Forward numbers set successfully [" + str(settings.FOR_NUMBERS).strip('[]') + "]"
    context = {'message': message}
    return render(request, 'manager/done.html', context)

def utc_to_local(t):
    utc = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
    UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
    local_datetime = utc - UTC_OFFSET_TIMEDELTA
    return local_datetime.strftime("%Y-%m-%d %H:%M:%S")

def getInLogs(request):
    index = request.GET.get('index')
    data = serializers.serialize("json", InSMS.objects.all()[index:])
    return HttpResponse(data)

def getOutLogs(request):
    index = request.GET.get('index')
    data = serializers.serialize("json", OutSMS.objects.all()[index:])
    return HttpResponse(data)
