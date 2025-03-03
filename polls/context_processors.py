from .models import Question
from django.db.models import Sum

def get_question_lists():
    """ Retrieve various filtered question lists. """
    questions = Question.objects.annotate(total_votes=Sum('choice__votes'))
    return {
        "latest_questions": ("Most Recent Questions", Question.objects.order_by("-pub_date")[:5]),
        "oldest_questions": ("Oldest Questions", Question.objects.order_by("pub_date")[:5]),
        "popular_questions": ("Most Popular Questions", questions.order_by('-total_votes')[:5]),
        "all_questions": ("All Questions", Question.objects.all()),
    }


def latest_questions(request):
    """ Add the most recent questions to the context """
    return {"latest_questions": get_question_lists()["latest_questions"]}

def oldest_questions(request):
    """ Add the oldest questions to the context """
    return {"oldest_questions": get_question_lists()["oldest_questions"]}

def popular_questions(request):
    """ Add the most popular questions by voting total to the context """
    return {"popular_questions": get_question_lists()["popular_questions"]}

def all_questions(request):
    """ Add all questions to the context """
    return {"all_questions": get_question_lists()["all_questions"]}

def all_lists(request):
    """ Combine all lists into a dictionary to add to the context """
    return {"all_lists": get_question_lists()}

def specific_question_list(request):
    """ Get a specific list from the request parameters """
    list_name = request.GET.get("list_name") # Extract list name from GET params
    question_list = get_question_lists().get(list_name, []) # Get selected list or empty
    return {"list_name": list_name, "question_list": question_list}
