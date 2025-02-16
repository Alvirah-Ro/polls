"""
View definitions for the Polls App
"""

from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Topic, Question, Choice
# Create your views here.

class IndexView(generic.ListView):
    """View for main page"""
    template_name = "polls/index.html"
    context_object_name = "topic_list"

    def get_queryset(self):
        """Return a list of all topics"""
        return Topic.objects.all()

def topic_view(request, pk):
    """View for all questions of a particular topic"""
    # Get the Topic object by its primary key (pk)
    topic = get_object_or_404(Topic, pk=pk)

    # Get all Questions related to this Topic
    questions = Question.objects.filter(topic=topic)

    # Return the context to the template
    return render(request, 'polls/topic.html', {
        'topic': topic,  # Pass the Topic object
        'question_by_topic_list': questions  # Pass the filtered Questions
    })


#class QuestionsView(generic.ListView):
#    template_name = "polls/questions.html"
#    context_object_name = "latest_question_list"

#    def get_queryset(self):
#        """Return the last five published questions."""
#        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    """View for details of a question with voting choices"""
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    """View that displays all voting results for a question"""
    model = Question
    template_name = "polls/results.html"


def question_view(request):
    """View that lists questions based on date published"""
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    earliest_question_list = Question.objects.order_by("pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list,
        "earliest_question_list": earliest_question_list,
    }
    return render(request, "polls/questions.html", context)


#def detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, "polls/detail.html", {"question": question})


#def results(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    """View for users to submit a vote on a question"""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
