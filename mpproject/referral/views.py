from django.shortcuts import render
import hashlib, time
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
import string
import random

# Create your views here.
@login_required(login_url="/manager/login")
def index(request):
    user = request.user;
    return HttpResponse("Welcome to referral system, " + user.first_name)

def referralCode(request):
    return HttpResponse(referralCodeGenerator())

def referralCodeGenerator(size=5, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

@login_required(login_url="/manager/login")
def referralCodeGenerator1(request):
    user = request.user;
    md5 = hashlib.md5(user.username)
    md5.update(str(time.time()))
    return md5.hexdigest()
