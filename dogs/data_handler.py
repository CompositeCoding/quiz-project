
from .models import Dog, HardDealbreaker, SoftDealbreaker, Score, QuizResult, QuizQuestion


def data_handler(form_data):

    """
    This function receives the data from the form submitted by the user.

    First the dogs are fetched from the database and a nested dictionary
    is created where the name of the dog is the key and a dictionary
    with the dealbreaks as value


    """

    # Setup dictionary to store dogs
    bakje = dict()

    # Fetch dogs and store the objects in the bakje dictionary
    for dog in Dog.objects.all():
        bakje[dog.name] = {'_h_': dict() ,'_s_': dict(),'_c_': dict()}

        # This section iterated over the the dealbreakers that have
        # a relationship with the dog object, and populates the dictionary
        # with the values
        for breaker in dog.harddealbreakers.all():
            if breaker.name in form_data:
                if breaker.name in bakje[dog.name]['_h_']:
                    bakje[dog.name]['_h_'][breaker.name].append(breaker.value)
                else:
                    bakje[dog.name]['_h_'][breaker.name] = [breaker.value]

        # This section does the same with the soft dealbreakers and the score
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
            # Check if there is a match between the result of the quiz and
            # the values from the dog dictionary, if there is no match,
            # remove from the dictionary
            if not isinstance(form_data[column], list):
                if not int(form_data[column]) in [int(x) for x in value]:
                    if ras in tempBakje:
                        del tempBakje[ras]
            else:
                if not len(set([int(x) for x in value]).intersection(set([int(x) for x in form_data[column]]))) > 0:
                    if ras in tempBakje:
                        del tempBakje[ras]

    # Create copy of tempBakje to delete the dogs from
    returnBakje = tempBakje.copy()

    #
    for ras, dealbreakers in tempBakje.items():
        for column, value in dealbreakers['_s_'].items():
            # If dealbreaker is smaller or equal to form value
            if not int(value) <= int(form_data[column]):
                if ras in returnBakje:
                    del returnBakje[ras]

    manyDogs = []

    # Return the rassen in returnbakje if they are there, else return nothing.
    if len([key for key,value in returnBakje.items()]) == 0:
        return "No Dogs"

    # If there are less than 6 dogs left, return them
    if len([key for key,value in returnBakje.items()]) <= 6:
        return ";".join([key for key,value in returnBakje.items()])

    # If there are more than 6 dogs left, take the scores into account
    if len([key for key,value in returnBakje.items()]) > 6:
        for ras, dealbreakers in returnBakje.items():
            for column, value in dealbreakers['_c_'].items():
                if int(value) == int(form_data[column]):
                    manyDogs.append(ras)

        # If, after taking the scores into account 0 dogs are left,
        # return the original dictionary
        if len(manyDogs) == 0:
            return ";".join([key for key,value in returnBakje.items()])
        else:
            return ";".join(manyDogs)
