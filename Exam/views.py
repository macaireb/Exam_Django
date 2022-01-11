from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from itertools import chain
# Create your views here.


class HomeView(ListView):
    model = Test
    template_name = 'Exam/home.html'


def CreateExamView(request, ider):
    proctor = User.objects.get(pk=ider)
    if request.method == 'POST':
        form = CreateExam(request.POST)
        if form.is_valid():
            test = form.save()
            return render(request, 'Exam/choose_question_type.html', {'test': test})
    else:
        form_class = CreateExam(initial={'proctor': proctor})
        return render(request, 'Exam/create_exam.html', {'form': form_class})


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
            return ExamDetailView(request, ider)
            #return render(request, 'Exam/choose_question_type.html', {'test': test})
    else:
        form_class = CreateFIBForm(initial={'exam': test})
        return render(request, 'Exam/create_FIB.html', {'test': test, 'form': form_class})


def CreateTFView(request, ider):
    test = Test.objects.get(pk=ider)
    if request.method == 'POST':
        form = CreateTFForm(request.POST)
        if form.is_valid():
            form.save()
            return ExamDetailView(request, ider)
            #return render(request, 'Exam/choose_question_type.html', {'test': test})
            #return render(request, 'Exam/home.html', {})
            #eturn reverse_lazy('exam_detail', kwargs={'ider': ider})
            #return render(request, 'Exam/exam_detail.html', {'ider': ider, 'test': test})
    else:
        form_class = CreateTFForm(initial={'exam': test})
        return render(request, 'Exam/create_TF.html', {'test': test, 'form': form_class})


def CreateMCView(request, ider):
    test = Test.objects.get(pk=ider)
    if request.method == 'POST':
        form = CreateFIBForm(request.POST)
        if form.is_valid():
            form.save()
            return ExamDetailView(request, ider)
            #return render(request, 'Exam/choose_question_type.html', {'test': test})
    else:
        form_class = CreateMCForm(initial={'exam': test})
        return render(request, 'Exam/create_MC.html', {'test': test, 'form': form_class})


def ChooseQuestionView(request, ider):
    test = Test.objects.get(pk=ider)
    return render(request, 'Exam/choose_question_type.html', {'test': test})


def ExamDetailView(request, ider):
    c_exam = Test.objects.get(pk=ider)
    mcs = MC_Question.objects.all().filter(exam=Test.objects.get(pk=ider))
    tfs = TF_Question.objects.all().filter(exam=Test.objects.get(pk=ider))
    fibs = FIB_Question.objects.all().filter(exam=Test.objects.get(pk=ider))
    return render(request, 'Exam/exam_detail.html', {'mcs': mcs, 'tfs': tfs, 'fibs': fibs, 'test': c_exam})


def StartExam(request, ider):
    exam_c = Test.objects.get(pk=ider)
    if request.user.is_authenticated:
        assigned = Assignment.objects.all().filter(test=exam_c, student=request.user)
        assignment = Assignment(test=exam_c, student=request.user)
        if assignment is not assigned:
            assignment.save()
        return render(request, 'Exam/start_exam.html', {'assignment': assignment})
    elif request.user.is_anonymous:
        return render(request, 'Exam/start_exam.html')
    #create another page when an exam can't be start, use else statement here


def AskQuestion(request, ider):
    assignment = Assignment.objects.get(pk=ider)
    mcs = MC_Question.objects.all().filter(exam=assignment.test)
    tfs = TF_Question.objects.all().filter(exam=assignment.test)
    fibs = FIB_Question.objects.all().filter(exam=assignment.test)
    questions = list(chain(mcs, tfs, fibs))
    return render(request, 'Exam/ask_question.html', {'questions': questions})

def ViewAssignments(request, ider):
    assignments = Assignment.objects.all().filter(student=request.user)
    return render(request, 'Exam/view_assignments.html', {'assignments': assignments})
