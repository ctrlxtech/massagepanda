from django.shortcuts import render_to_response

from django.http import HttpResponse, JsonResponse
from django.template import Context, RequestContext
from django.contrib.auth.tokens import default_token_generator
from feedback.models import Feedback

from django.db import transaction

# Create your views here.
def feedbackEmail(request):
    try:
      staff = Staff.objects.get(pk=request.GET.get('id'))
    except:
      pass
    context = {'message': 'Thanks'}
    return render_to_response('feedback/feedbackEmail.html', context, context_instance=RequestContext(request))

def feedbackSurvey(request, code=None, rating=None):
    assert code is not None and rating is not None
    try:
      feedback = Feedback.objects.get(code=code)
      if feedback.rated:
          validlink = False
      else:
          validlink = True
    except:
      validlink = False
    context = {'message': 'Thanks', 'validlink': validlink, 'code': code, 'rating': rating}
    return render_to_response('feedback/feedbackSurvey.html', context, context_instance=RequestContext(request))

@transaction.atomic
def feedbackConfirm(request):
    code = request.POST.get('code')
    rating = request.POST.get('rating')
    whereYouLearn = request.POST.get('whereYouLearn')
    comment = request.POST.get('comment')
    rating = int(rating)
    assert code and rating and rating >= 1 and rating <= 5
    feedback = Feedback.objects.get(code=code)
    if feedback.rated is True:
        context = {'validlink': False}
        return render_to_response('feedback/feedbackSurvey.html', context, context_instance=RequestContext(request))
    feedback.rated = True
    feedback.rating = rating
    ots = feedback.order.ordertherapist_set.all()
    for ot in ots:
      if ot.therapist.rating:
        ot.therapist.rating += rating
      else:
        ot.therapist.rating = rating
    
      if ot.therapist.rate_count:
        ot.therapist.rate_count += 1
      else:
        ot.therapist.rate_count = 1

      ot.therapist.save()

    feedback.comment = whereYouLearn + "|comment: " + comment
    feedback.save()
    return render_to_response('index/index.html', {}, context_instance=RequestContext(request))
