from django.urls import path
from . import views

urlpatterns = [
    path('migrate/', views.migrate, name='migrate'),
    path('', views.home, name='home'),
    path('results/<form>/', views.results, name='results'),
    path('quiz/', views.QuizWizard.as_view(), name='quiz'),
    path('api/<key>/', views.returnAPI, name='api'),
]
