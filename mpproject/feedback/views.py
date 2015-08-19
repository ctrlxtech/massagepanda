from django.shortcuts import render

# Create your views here.
def feedbackEmail(request):
    try:
      staff = Staff.objects.get(pk=request.GET.get('id'))
    except:
      pass
    context = {'message': 'Thanks'}
    return render(request, 'feedback/feedbackEmail.html', context)

def feedbackSurvey(request):
    try:
      staff = Staff.objects.get(pk=request.GET.get('id'))
    except:
      pass
    context = {'message': 'Thanks'}
    return render(request, 'feedback/feedbackSurvey.html', context)
