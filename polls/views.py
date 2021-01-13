from django.shortcuts import render , get_object_or_404
from django.http import HttpResponseRedirect
from .models import Question , Choice
from django.urls import reverse, timezone
from django.views import generic
# Create your views here.
#used render instead of Httpresponse
class IndexView(generic.ListView):
    context_object_name = 'latest_question_list'
    template_name='polls/index.html'

    def get_queryset(self):
        """
        Return the last 5 published Question ( not including those set to be published in the future)
        """
        return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name='polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name='polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question ,pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #Redisplay Question Voting form
        return render(request, 'polls/detail.html',{
            'question':question,
            'error_messeage' : "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #Always return an HttpResponseRedirect after successfully dealing
        #with POST data. This prevents data from being posted twice if a user hits the Back button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
