from django.shortcuts import render

from services.models import Service

# Create your views here.
def services(request):
    service_list = Service.objects.order_by('service_type')
    context = {'service_list': service_list}
    return render(request, 'services/store.html', context)
