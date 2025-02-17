"""
View definitions for the Polls App
"""

from django.shortcuts import render, get_object_or_404
from django.db.models import F, Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Topic, Question, Choice
# Create your views here.

class IndexView(generic.ListView):
    """This View is for the main page"""
    template_name = "polls/index.html"
    context_object_name = "topic_list"

    def get_queryset(self):
        """Return a list of all topics"""
        return Topic.objects.all()


def topic_view(request, pk):
    """This View lists all questions for a particular topic"""
    # Get the Topic object by its primary key (pk)
    topic = get_object_or_404(Topic, pk=pk)

    # Get all Questions related to this Topic
    questions = Question.objects.filter(topic=topic)

    # Return the context to the template
    return render(request, 'polls/topic.html', {
        'topic': topic,  # Pass the Topic object
        'question_by_topic_list': questions  # Pass the filtered Questions
    })


class DetailView(generic.DetailView):
    """This View displays details of a question with voting choices"""
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    """This View displays all voting results for a question"""
    model = Question
    template_name = "polls/results.html"


def question_view(request):
    """This View displays lists questions based on various parameters"""
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    earliest_question_list = Question.objects.order_by("pub_date")[:5]
    questions = Question.objects.annotate(total_votes=Sum('choice__votes'))
    most_popular_question_list = questions.order_by('-total_votes')[:5]
    context = {
        "latest_question_list": latest_question_list,
        "earliest_question_list": earliest_question_list,
        "most_popular_question_list": most_popular_question_list
    }
    return render(request, "polls/questions.html", context)


def vote(request, question_id):
    """This View allows users to submit a vote on a question"""
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


def add_question(request):
    """This View allows users to submit a new question"""
    if request.method == "POST":
        question_text = request.POST.get("question_text")
        topic_ids = request.POST.getlist("topic") #getlist() for multiple topics
        choice_texts = request.POST.getlist("choice") #getlist() for multiple choices

        # Check if all required fields are filled
        if not question_text or not topic_ids or not choice_texts:
            return render(
                request,
                "polls/add_question.html",
                {
                    "error_message": "You didn't select all required fields.",
                },
            )

        # Create the Question instance
        question = Question.objects.create(
            question_text=question_text,
            pub_date=timezone.now()
        )

        # Add topics to the Question
        topics = Topic.objects.filter(id__in=topic_ids)
        question.topic.set(topics)

        # Create Choice instances
        for choice_text in choice_texts:
            Choice.objects.create(
                question=question,
                choice_text=choice_text,
                votes=0
            )

        # Redirect to index page after successful submission
        return redirect(reverse("polls:index"))

    # If request method is GET, render the form
    return render(request, "polls/add_question.html")




#class QuestionsView(generic.ListView):
    #"""This is an alternate view for displaying a list of questions"""
#    template_name = "polls/questions.html"
#    context_object_name = "latest_question_list"

#    def get_queryset(self):
#        """Return the last five published questions."""
#        return Question.objects.order_by("-pub_date")[:5]


    #def detail(request, question_id):
    #"""This is an alternate view for displaying question details"""
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, "polls/detail.html", {"question": question})


#def results(request, question_id):
    #"""This is an alternate view for displaying voting results"""
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, "polls/results.html", {"question": question})
