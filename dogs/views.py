from django.shortcuts import render, redirect
from django.http import HttpResponse
from formtools.wizard.views import SessionWizardView
from datetime import date
from django.http import JsonResponse

from .models import Dog, HardDealbreaker, SoftDealbreaker, Score, QuizResult, QuizQuestion
from .forms import Quiz1 ,Quiz2, Quiz3, Quiz4, Quiz5, Quiz6, Quiz7, Quiz8, Quiz9
from .dbmigrations import migrate_dogs
from .data_handler import data_handler


def migrate(request):
    """ View to call migrate button"""
    if request.user.is_authenticated:
        try:
            migrate_dogs()
            return HttpResponse('Success')
        except Exception as e:
            print(e)
            return HttpResponse(f'Failed to migrate database\n reason: {e}')
    if not request.user.is_authenticated:
        return redirect("home")


def home(request):
    return render(request, 'home.html')

def results(request, form=None):
    context = dict()
    form = form.split(';')
    dogs = Dog.objects.filter(name__in=form).filter(image__isnull=False).filter(link__isnull=False)
    if form[0] == "No Dogs":
        context["NoDogs"] = True
    else:
        context["NoDogs"] = False
        context['rassen'] = dogs
    return render(request, 'results.html',context)


class QuizWizard(SessionWizardView):

    """
    This class based view is a WizardView, it create a form that spans multiple pages.
    It takes a number of forms as input(form_list) and the done function is called
    when the form is submitted
    https://django-formtools.readthedocs.io/en/latest/wizard.html#
    """

    # Determine which questions should be shown
    form_list = [Quiz1, Quiz2, Quiz3, Quiz4, Quiz5, Quiz6, Quiz7, Quiz8, Quiz9]
    template_name = 'quiz.html'

    def done(self, form_list, **kwargs):
        # The done method is called when all the quiz answers are being answered.
        form = [form.cleaned_data for form in form_list]
        form_data = dict()
        for data in form:
            key, value = data.popitem()
            form_data[key] = value

        # Create a new Quiz Object
        quiz = QuizResult(created_at=date.today())
        quiz.save()

        # Loop over form_data dict and add the answers to databse one to many
        for key,value in form_data.items():
            if isinstance(value, list):
                result = QuizQuestion(quiz=quiz,question=key ,answer="".join(value))
                result.save()
            if not isinstance(value, list):
                result = QuizQuestion(quiz=quiz,question=key,answer=value)
                result.save()

        # Call the data_handler function to process the quiz data and determine which rassen should be returned
        rassen = data_handler(form_data)

        # Return the rassen to the user
        return redirect('results', form=rassen)
