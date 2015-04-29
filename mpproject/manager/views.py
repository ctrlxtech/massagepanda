from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from manager.models import Staff
import requests
# Create your views here.
@login_required
def index(request):
    staff_list = Staff.objects.order_by('name')
    context = {'staff_list': staff_list}
    return render(request, 'manager/sms.html', context)

def send(request):
    ppl = request.POST.getlist('needToSend')
    message_body = request.POST.get('message')
    number = ""
    api_key = "412847f0"
    api_secret = "55f41401"
    for p in ppl:
        number += str(Staff.objects.get(pk=p).phone_number)
#    cmd = "https://rest.nexmo.com/sms/json?api_key=" + api_key + "&api_secret=" +\
#        api_secret + "&from=12069396577&to=" + number + "&text=hello_world"
#    return HttpResponse(cmd)
    payload = {'api_key': api_key, 'api_secret': api_secret, 'from': "12069396577", 'to': number, 'text': message_body} 
    r = requests.get("https://rest.nexmo.com/sms/json", params=payload)
    return HttpResponse(r)
