from django.contrib import admin
from .models import Dog ,HardDealbreaker ,SoftDealbreaker ,Score, QuizResult, QuizQuestion



admin.site.register(Dog)
admin.site.register(HardDealbreaker)
admin.site.register(SoftDealbreaker)
admin.site.register(Score)
admin.site.register(QuizResult)
admin.site.register(QuizQuestion)
