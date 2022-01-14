from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.urls import reverse_lazy
from itertools import chain
from django.core.exceptions import ObjectDoesNotExist
import logging
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
        try:
            assigned = Assignment.objects.get(test=exam_c, student=request.user)
        except ObjectDoesNotExist:
            assigned = Assignment(test=exam_c, student=request.user)
            assigned.save()
        return render(request, 'Exam/start_exam.html', {'assignment': assigned})
    elif request.user.is_anonymous:
        return render(request, 'Exam/start_exam.html')
    #create another page when an exam can't be start, use else statement here


def AskQuestion(request, ider):
    print("Hello user")
    assignment = Assignment.objects.get(pk=ider)
    mcs = MC_Question.objects.all().filter(exam=assignment.test)
    tfs = TF_Question.objects.all().filter(exam=assignment.test)
    fibs = FIB_Question.objects.all().filter(exam=assignment.test)
    questions = list(chain(mcs, tfs, fibs))
    original_questions = list(chain(mcs, tfs, fibs))
    logger = logging.getLogger(__name__)

    def get_question():
        print("getting question")
        q_text = []
        for q in questions:
            print(q.assignment)
            if q.assignment:
                questions.pop(questions.index(q))
                q_text.append(q.text)
                print("removed " + q.text)
        for ques in questions:
            for que in q_text:
                if que == ques.text: #remove unassigned question from list
                    try:
                        questions.pop(questions.index(ques))
                        print("removed unassigned" + ques.text)
                    except ValueError:
                        pass
        return questions.pop()
    if request.method == 'POST':
        question = get_question()
        if isinstance(question, TF_Question):
            form = AskTFQuestionForm(request.POST)
            print(form.is_valid())
            print(form.cleaned_data)
            print("However question exam is: " + question.exam.title)
            if form.is_valid():
                original = True
                for i in original_questions:
                    if i.text == form.cleaned_data['text'] and i.assignment and i.assignment.student == request.user:
                        original = False
                        print('Answer is a duplicate, not saving')
                if original:
                    form.save()
                    print('Saved Answered')
                form_class = AskTFQuestionForm(
                    initial={'assignment': assignment, 'exam': question.exam, 'correct_answer': question.correct_answer,
                             'text': question.text})
                return render(request, 'Exam/ask_question.html', {'question': question, 'form': form_class})
    question = get_question()
    if (isinstance(question, TF_Question)):
        #Need a check to see if question already has an assignment
        form_class = AskTFQuestionForm(initial={'assignment': assignment, 'exam': question.exam, 'correct_answer':
            question.correct_answer, 'text': question.text})
        print("Too However question exam is: " + question.exam.title)
    return render(request, 'Exam/ask_question.html', {'question': question, 'form': form_class})


def ViewAssignments(request, ider):
    assignments = Assignment.objects.all().filter(student=request.user)
    return render(request, 'Exam/view_assignments.html', {'assignments': assignments})

def AssignExam(request, ider):
    users = User.objects.all()
    exam = Test.objects.get(pk=ider)
    if request.method == "POST":
        form = AssignExamForm(request.POST)
        print(form.is_valid())
        print(form.cleaned_data)
        if form.is_valid():
            duplicate = Assignment.objects.all().filter(
                student=request.POST.get("student", ''), test=request.POST.get("test", ''))
            print(not duplicate)
            if not duplicate:
                form.save()
            mcs = MC_Question.objects.all().filter(exam=Test.objects.get(pk=ider))
            tfs = TF_Question.objects.all().filter(exam=Test.objects.get(pk=ider))
            fibs = FIB_Question.objects.all().filter(exam=Test.objects.get(pk=ider))
            return render(request, 'Exam/exam_detail.html', {'mcs': mcs, 'tfs': tfs, 'fibs': fibs, 'test': exam})
    else:
        form_class = AssignExamForm()
        form_class.fields['student'].choices = [(user.pk, user.username) for user in users]
        form_class.fields['test'].initial = exam
        return render(request, 'Exam/assign_exam.html', {'form': form_class})
