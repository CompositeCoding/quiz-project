from django.shortcuts import render, redirect
from .dbmigrations import migrate_dogs
from django.http import HttpResponse
from .models import Dog, HardDealbreaker, SoftDealbreaker, Score, QuizResult, QuizQuestion
from formtools.wizard.views import SessionWizardView
from .forms import Quiz1 ,Quiz2, Quiz3, Quiz4, Quiz5, Quiz6, Quiz7, Quiz8, Quiz9
from datetime import date
from django.http import JsonResponse

def migrate(request):
    """ View to call migrate butto  """
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


def data_handler(form_data):

    """
    This function receives the form data and checks it vs the dealbreakers of the dogs in the database. First it fetches the dogs in the db and places
    them in a dictionary. Then it iterates over this dictionary taking the hard dealbreakers out a copy of that dictionart. Then it iterates over the new dictionary
    and takes the softdealbreaker out of a copy of the new dictionary and returns the name of the breed.
    """

    # Setup dictionary to store dogs
    bakje = dict()

    # Fetch dogs
    for dog in Dog.objects.all():
        # Dict with ras as key
        bakje[dog.name] = {'_h_': dict() ,'_s_': dict(),'_c_': dict()}
        # Grab hard dealbreakers and if in form add them to dict in a list of value.
        for breaker in dog.harddealbreakers.all():
            if breaker.name in form_data:
                if breaker.name in bakje[dog.name]['_h_']:
                    bakje[dog.name]['_h_'][breaker.name].append(breaker.value)
                else:
                    bakje[dog.name]['_h_'][breaker.name] = [breaker.value]

        # Grab soft dealbreakers and if in form set them as a value.
        for breaker in dog.softdealbreakers.all():
            if breaker.name in form_data:
                bakje[dog.name]['_s_'][breaker.name] = breaker.value

        for breaker in dog.scores.all():
            if breaker.name in form_data:
                bakje[dog.name]['_c_'][breaker.name] = breaker.value


    # Create copy of bakje to delete the dogs from
    tempBakje = bakje.copy()

    # Iterate over dogs, iterate over hard dealbreakers
    for ras, dealbreakers in bakje.items():
        for column, value in dealbreakers['_h_'].items():
            # Check if list,
            if not isinstance(form_data[column], list):
                if not int(form_data[column]) in [int(x) for x in value ]:
                    if ras in tempBakje:
                        del tempBakje[ras]
                        # print("Hard: ",column ,ras, 'quiz waarde:', form_data[column], 'Ras waarde', value)
            else:
                if not len(set([int(x) for x in value]).intersection(set([int(x) for x in form_data[column]]))) > 0:
                    if ras in tempBakje:
                        del tempBakje[ras]
                        # print("Hard: ",column ,ras,form_data[column],value)

    # Create copy of tempBakje to delete the dogs from
    returnBakje = tempBakje.copy()

    # iterate over dogs, iterate over soft dealreakers
    for ras, dealbreakers in tempBakje.items():
        for column, value in dealbreakers['_s_'].items():
            # If dealbreaker is smaller or equal to form value
            if not int(value) <= int(form_data[column]):
                if ras in returnBakje:
                    del returnBakje[ras]
                    # print("Soft: ",column,ras, 'quiz waarde: ', form_data[column],'Ras waarde: ', value)


    manyDogs = []

    # Return the rassen in returnbakje if they are there, else return nothing.
    if len([key for key,value in returnBakje.items()]) == 0:
        return "No Dogs"

    if len([key for key,value in returnBakje.items()]) <= 6:
        return ";".join([key for key,value in returnBakje.items()])

    if len([key for key,value in returnBakje.items()]) > 6:
        for ras, dealbreakers in returnBakje.items():
            for column, value in dealbreakers['_c_'].items():
                if int(value) == int(form_data[column]):
                    manyDogs.append(ras)
        if len(manyDogs) == 0:
            return ";".join([key for key,value in returnBakje.items()])
        else:
            return ";".join(manyDogs)



class QuizWizard(SessionWizardView):

    """
    This class based view is a WizardView, it create a form that spans multiple pages.
    It takes a number of forms as input(form_list) and the done function is called
    when the form is submitted
    https://django-formtools.readthedocs.io/en/latest/wizard.html#
    """

    # Determine which questions should be shown
    form_list = [Quiz1,Quiz2, Quiz3, Quiz4, Quiz5, Quiz6, Quiz7, Quiz8,Quiz9]
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

        return redirect('results',form=rassen)
