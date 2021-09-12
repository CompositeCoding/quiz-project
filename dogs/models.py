from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

#############################################################################################################################################################
#
# Base breed model
#
##############################################################################################################################################################

class Dog(models.Model):
    # DB model that stores breeds with the breed name, link to image, and link to rassenpagina
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    image = models.URLField(max_length=250,null=True, blank=True)
    link = models.URLField(max_length=250,null=True, blank=True)

    def __str__(self):
        return self.name

#############################################################################################################################################################
#
# Relationship to the breed model
#
##############################################################################################################################################################

class HardDealbreaker(models.Model):
    # hard dealbreaker are quiz question which creates a 'hard' subsection of dogs based on the respected answer. e.g. if you want a large dog you don't want a small dog
    dog = models.ForeignKey(Dog, related_name='harddealbreakers', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return self.name

class SoftDealbreaker(models.Model):
    # Soft dealbreakers which create a 'soft' subsection of dogs. e.g. If you live in a big house you can also have dogs that are fitted for small housess
    dog = models.ForeignKey(Dog, related_name='softdealbreakers', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(4)])

    def __str__(self):
        return self.name

class Score(models.Model):
    dog = models.ForeignKey(Dog,related_name='scores', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(4)])

    def __str__(self):
        return self.name

#############################################################################################################################################################
#
# Models for saving questions to database
#
##############################################################################################################################################################
class QuizResult(models.Model):
    created_at = models.DateTimeField()

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(QuizResult,related_name='quiz', on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    answer =  models.CharField(max_length=100)
