from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from manager.models import Staff, InSMS
import requests
import json
import time
# Create your views here.
@login_required
def index(request):
    staff_list = Staff.objects.order_by('first_name')
    context = {'staff_list': staff_list}
    return render(request, 'manager/sms.html', context)

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
        time.sleep(1)
    return HttpResponse(r)

def sendWithNum(request):
    number = request.POST.get('num')
    message_body = request.POST.get('messageWithNum')
    api_key = "412847f0"
    api_secret = "55f41401"
    payload = {'api_key': api_key, 'api_secret': api_secret, 'from': "12069396577", 'to': number, 'type': 'unicode', 'text': message_body} 
    r = requests.get("https://rest.nexmo.com/sms/json", params=payload).text
    return HttpResponse(r)

def receiveSMS(request):
    msisdn = request.GET.get('msisdn')
    message_body = request.GET.get('text')
    time_stamp = request.GET.get('message-timestamp')
    if (msisdn is None):
        msisdn = "none"
    if (message_body is None):
        message_body = "no_body"

    if (msisdn is None or message_body is None):
        i = InSMS(sender=msisdn, messageBody=message_body)
        i.save()
        return HttpResponse("***Error request")

    i = InSMS(sender=msisdn, messageBody=message_body, timestamp=time_stamp)
    i.save()
    numbers = [14128889022, 16056596655, 12133790752]
    api_key = "412847f0"
    api_secret = "55f41401"
    message_body += "[sent by " + msisdn + " at " + time_stamp + "]"
    for num in numbers:
        payload = {'api_key': api_key, 'api_secret': api_secret, 'from': "12069396577", 'to': num, 'type': 'unicode', 'text': message_body} 
        requests.get("https://rest.nexmo.com/sms/json", params=payload).text

    return HttpResponse()

