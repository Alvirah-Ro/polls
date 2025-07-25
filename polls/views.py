"""
View definitions for the Polls App
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from polls.context_processors import get_question_lists  # Import function

from .models import Topic, Question, Choice
# Create your views here.

# class IndexView(generic.ListView):
#     """This is an alternate View for the main page"""
#     template_name = "polls/index.html"
#     context_object_name = "topic_list"

#     def get_queryset(self):
#         """Return a list of all topics"""
#         return Topic.objects.all()


def index_view(request):
    """This View is for the main page"""
    # Get the 5 most recently added questions
    latest_questions = Question.objects.order_by("-pub_date")[:5]

    return render (request, 'polls/index.html', {
        "latest_questions": latest_questions,
    })


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


def question_list_view(request, list_name):
    """This View lists all questions for a specific list based on the key in all_lists"""
    print(f"Received list_name: {list_name}")
    all_lists = get_question_lists() # Retrieve al lists
    list_info = all_lists.get(list_name, ("Unknown List", [])) # Default if not found
    readable_name, selected_list = list_info

    return render(request, "polls/question_list.html", {
        "list_name": readable_name, # Display the readable title
        "question_list": selected_list,
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
    topic_list = Topic.objects.all()

    return render(request, "polls/questions.html",
        {
            "topic_list": topic_list
    })


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
    topics = Topic.objects.all() # Retrieve topics from the database

    if request.method == "POST":
        question_text = request.POST.get("question_text")
        topic_name = request.POST.get("new_topic")
        topic_ids = request.POST.getlist("topic") # getlist() for multiple topics
        choice_texts = request.POST.getlist("choice") # getlist() for multiple choices
        filtered_choices = [choice for choice in choice_texts if choice.strip()]
        # Filter to remove empty choices

        # Make sure at least 2 choices were entered
        if len(filtered_choices) < 2:

            return render(request, "polls/add_question.html", {
                "topics": topics,
                "error_message": "You must provice at least two choices.",
                "question_text": question_text,
                "selected_topic_ids": topic_ids,
                "new_topic": topic_name,
                "choices": choice_texts,
                }
            )

        # Check if all required fields are filled
        if not question_text or (not topic_ids and not topic_name):

            return render(request, "polls/add_question.html", {
                "topics": topics,
                "error_message": "You must provide question text and at least one topic.",
                "question_text": question_text,
                "selected_topic_ids": topic_ids,
                "new_topic": topic_name,
                "choices": choice_texts,

                }
            )

        # Create the Question instance
        question = Question.objects.create(
            question_text=question_text,
            pub_date=timezone.now()
        )

        # Add any new topics
        if topic_name:
            topic, _ = Topic.objects.get_or_create(
                topic_name=topic_name,
                defaults={"pub_date": timezone.now()}
            )
            topic_ids.append(str(topic.id))

        if topic_ids:
            question.topic.set(Topic.objects.filter(id__in=topic_ids))

        # Create Choices linked to the question
        for choice_text in filtered_choices:
            Choice.objects.create(
                question=question,
                choice_text=choice_text,
                votes=0
            )

        # Redirect to index page after successful submission
        # Include a message to indicate the question adding was successful
        messages.success(request, "Your question has been successfully added!")
        return redirect(reverse("polls:index"))

    # If request method is GET, render the form
    return render(request, "polls/add_question.html", {"topics": topics})

def question_search_view(request):
    """This view defines how to search for keywords in all models"""
    query = request.GET.get("q", "") # Get search query from URL parameter

    if query:
        questions = (
            Question.objects.filter(
                Q(question_text__icontains=query)  |
                Q(topic__topic_name__icontains=query)  |
                Q(choice__choice_text__icontains=query)
            )
            .select_related() # for foreign keys like topic
            .prefetch_related("choice_set") # for reverse foreign key (choices)
            .distinct()
        )
    else:
        questions = Question.objects.none()

    return render(request, "polls/search.html", {
        "query": query,
        "questions": questions,
    })


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
