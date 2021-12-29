from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import *
from .forms import *
from django.urls import reverse_lazy
# Create your views here.


class HomeView(ListView):
    model = Test
    template_name = 'Exam/home.html'


def CreateExamView(request, ider):
    user = User.objects.get(pk=ider)
    if request.method == 'POST':
        form = CreateExam(request.POST)
        if form.is_valid():
            test = form.save()
            return render(request, 'Exam/choose_question_type.html', {'test': test})
    else:
        form_class = CreateExam(initial={'proctor': user})
        return render(request, 'Exam/create_exam.html', {'user': user, 'form': form_class})


class EditExamView(UpdateView):
    model = Test
    template_name = 'Exam/update_exam.html'
    form_class = UpdateExam
    success_url = reverse_lazy('home')


def CreateFIBView(request, ider):
    test = Test.objects.get(pk=ider)
    if request.method == 'POST':
        form = CreateFIBForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'Exam/choose_question_type.html', {'test': test})
    else:
        form_class = CreateFIBForm(initial={'exam': test})
        return render(request, 'Exam/create_FIB.html', {'test': test, 'form': form_class})


def CreateTFView(request, ider):
    test = Test.objects.get(pk=ider)
    if request.method == 'POST':
        form = CreateTFForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'Exam/choose_question_type.html', {'test': test})
    else:
        form_class = CreateTFForm(initial={'exam': test})
        return render(request, 'Exam/create_TF.html', {'test': test, 'form': form_class})


def CreateMCView(request, ider):
    test = Test.objects.get(pk=ider)
    if request.method == 'POST':
        form = CreateFIBForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'Exam/choose_question_type.html', {'test': test})
    else:
        form_class = CreateMCForm(initial={'exam': test})
        return render(request, 'Exam/create_MC.html', {'test': test, 'form': form_class})


def ChooseQuestionView(request, ider):
    test = Test.objects.get(pk=ider)
    return render(request, 'Exam/choose_question_type.html', {'test': test})
