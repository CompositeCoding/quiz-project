
from .models import Dog, HardDealbreaker, SoftDealbreaker, Score, QuizResult, QuizQuestion


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
