from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Test(models.Model):
    title = models.CharField(max_length=100)
    proctor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' | ' + self.proctor.username

    def get_absolute_url(self):
        return reverse('choose_question', args=(self.pk,))


class FIB_Question(models.Model):
    text = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)
    user_answer = models.CharField(max_length=200, blank=True, null=True)
    exam = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('choose_question', args=(self.exam.primary_key,))


class TF_Question(models.Model):
    text = models.CharField(max_length=200)
    correct_answer = models.BooleanField()
    user_answer = models.BooleanField(blank=True, null=True)
    exam = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('choose_question', args=(self.exam.primary_key,))


class MC_Question(models.Model):
    One = models.CharField(max_length=200)
    Two = models.CharField(max_length=200)
    Three = models.CharField(max_length=200, blank=True, null=True)
    Four = models.CharField(max_length=200, blank=True, null=True)
    Five = models.CharField(max_length=200, blank=True, null=True)

    class Answers(models.IntegerChoices):
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5
    text = models.CharField(max_length=200)
    correct_answer = models.IntegerField(choices=Answers.choices, blank=True, null=True)
    user_answer = models.CharField(max_length=200)
    exam = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('choose_question', args=(self.exam.primary_key,))
