from django.shortcuts import render

# Create your views here.
def index(request):
    context = {"customer": "Kevin"}
    return render(request, 'customers/profile.html', context)

def referPage(request):
    context = {"customer": "Kevin"}
    return render(request, 'customers/refer.html', context)

def paymentPage(request):
    context = {"customer": "Kevin"}
    return render(request, 'customers/payment.html', context)
    
