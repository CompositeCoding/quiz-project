from django import forms

""" The forms that are loaded in the formwizzard """


class Quiz1(forms.Form):

    # Meerdere aanklikken, Elk formaat is goed voor mij.

    CHOICES= [('1','Kleine honden')
             ,('2','Middelgrote honden')
             ,('3','Grote honden')]

    _db_h_size = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['_db_h_size'].widget.attrs.update({'class': 'formfield'})
        self.fields['_db_h_size'].label = "Welk formaat hond heeft jouw voorkeur? (Meerdere opties mogelijk)"

class Quiz2(forms.Form):

    CHOICES= [('1','Een appartement zonder tuin.')
             ,('2','Een huis met een kleine tuin.')
             ,('3','Een huis met een grote tuin.')]

    _db_s_house = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['_db_s_house'].widget.attrs.update({'class': 'formfield'})
        self.fields['_db_s_house'].label = "Waar gaat de hond wonen?"

class Quiz3(forms.Form):

    CHOICES= [('1','Ja, kinderen jonger dan 12 jaar.')
             ,('2','Ja, kinderen ouder dan 12 jaar.')
             ,('2','Nee, de hond zal niet met kinderen wonen.')]

    _db_s_child = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['_db_s_child'].widget.attrs.update({'class': 'formfield'})
        self.fields['_db_s_child'].label = "Gaat de hond met kinderen wonen?"


class Quiz4(forms.Form):

    CHOICES= [('1','Nee, dit wordt mijn eerste hond.')
             ,('2','Ja, ik heb eerder honden gehad maar ben geen expert.')
             ,('3','Ja, ik heb mijn hele leven al honden en heb veel ervaring met training en socialisatie.')]

    _db_s_experience = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['_db_s_experience'].widget.attrs.update({'class': 'formfield'})
        self.fields['_db_s_experience'].label = "Heb je ervaring met honden?"


class Quiz5(forms.Form):

    CHOICES= [('1','Niet veel tijd, alleen kammen wanneer dat hoog nodig is.')
             ,('2','Regelmatig kammen vind ik geen probleem.')
             ,('3','Ik vind het leuk om veel tijd aan de vacht van mijn hond te besteden en vind een bezoek aan de trimmer niet erg.')]

    _db_s_care = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['_db_s_care'].widget.attrs.update({'class': 'formfield'})
        self.fields['_db_s_care'].label = "Hoeveel tijd wil je kwijt zijn aan de vacht van de hond?"

class Quiz6(forms.Form):

    CHOICES= [('1','Ik vind haren op mijn kleding en bank onprettig en wil dit liever niet.')
             ,('2','Een klein beetje hondenhaar maakt mij niet uit.')
             ,('3','Hondenhaar hoort nou eenmaal bij een hond.')]

    _db_s_fur = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['_db_s_fur'].widget.attrs.update({'class': 'formfield'})
        self.fields['_db_s_fur'].label = "Hoeveel last heb jij van hondenharen?"



class Quiz7(forms.Form):

    CHOICES= [('1','We gaan een klein blokje om, maar zijn liever lekker thuis.')
             ,('2','Doordeweeks een blokje om, maar in het weekend er lekker op uit.')
             ,('3','Ik ga elke dag minimaal een uur met de hond wandelen.')
             ,('4','Ik ben erg sportief en wil vaak lange tochten maken met de hond.')]

    _db_h_move = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['_db_h_move'].widget.attrs.update({'class': 'formfield'})
        self.fields['_db_h_move'].label = "Hoeveel wil jij met de hond bewegen op een doordeweekse dag?"


class Quiz8(forms.Form):

    CHOICES= [('1','Ik wil dat na één keer puppytraining de hond naar mij luistert.')
             ,('2','Ik wil er best wat tijd in investeren, maar wordt niet boos als de hond een keer niet luistert.')
             ,('3','Ik wil veel tijd steken in de opvoeding van de hond.')
             ,('4','Ik wil er erg veel tijd in steken, maar heb er ook vrede mee als de hond niet luistert.')]

    _db_s_train = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['_db_s_train'].widget.attrs.update({'class': 'formfield'})
        self.fields['_db_s_train'].label = "Wat zijn je inzet en verwachtigen met betrekking tot de opvoeding van de hond?"


class Quiz9(forms.Form):

    CHOICES= [('1','Ik zoek in een hond vooral gezelschap. Ik wil een makkelijke hond die buiten gezellig achter mij aanloopt.')
             ,('2','Ik ben lekker actief en wil een hond om lekker mee te lopen, maar ook een vriend om liefde te kunnen geven.')
             ,('3','Ik zoek in een hond een trouw maatje. Ik wil veel aandacht te steken in beweging.')
             ,('4','Ik ben fysiek sterk en heb ervaring met honden. Ik wil vooral met de hond werken. Ik ga veel tijd steken in training, mentale uitdaging en beweging.')
             ,('5','Ik heb veel ervaring met honden en een sterke wil. Ik kan een uitdagende hond waarderen. Ik ben de leider en ik wil dat de hond gehoorzaam naast mij leeft.')]

    _db_c_owner = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['_db_c_owner'].widget.attrs.update({'class': 'formfield'})
        self.fields['_db_c_owner'].label = "Welke zin omschrijft jou het beste als toekomstige honden eigenaar?"

"""
    _db_h_size : Welk formaat hond heeft jouw voorkeur?
    _db_s_house : "Waar gaat de hond wonen?
    _db_s_child : Hoe oud zijn de kinderen in het gezin?
    _db_s_experience :  Heb je ervaring met honden?
    _db_s_care : Hoeveel tijd wil je kwijt zijn aan de vacht van de hond?
    _db_s_fur : Hoeveel last heb jij van hondenharen?
    _db_h_move : Hoe veel wil jij met je hond bewegen op een doordeweekse dag?
    _db_s_train : Wat zijn je inzet en verwachtigen met betrekking tot de opvoeding van de hond?"
    _db_h_owner : "Welke zin omschrijft jou het beste als toekomstige honden eigenaar?"
"""
