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
        form = CreateMCForm(request.POST)
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
    mcs = MC_Question.objects.all().filter(exam=Test.objects.get(pk=ider), assignment=None)
    tfs = TF_Question.objects.all().filter(exam=Test.objects.get(pk=ider), assignment=None)
    fibs = FIB_Question.objects.all().filter(exam=Test.objects.get(pk=ider), assignment=None)
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

    def get_question():
        print("getting question")
        q_text = []
        for q in questions:
            print(q.text)
            if q.assignment:
                print("removed " + str(questions.index(q)) + q.text)
                q_text.append(q.text)
                questions.pop(questions.index(q))
        for que in q_text:
            for ques in questions:
                print(que + ' ' + ques.text)
                if que == ques.text: #remove duplicate unassigned question from list
                    try:
                        print("removed unassigned " + str(questions.index(ques)) + ques.text)
                        questions.pop(questions.index(ques))
                    except ValueError:
                        print("Got a value error")
        try:
            return questions.pop()
        except IndexError:
            print("There's no question to return!")
            return None

    if request.method == 'POST':
        question = get_question()
        print("Question is: " + question.text)
        if question == None:
            print("Trying to return to home page")
            return ExamDetailView(request, assignment.test.pk)
        elif isinstance(question, TF_Question):
            form = AskTFQuestionForm(request.POST)
        elif isinstance(question, FIB_Question):
            form = AskFIBQuestionForm(request.POST)
        elif isinstance(question, MC_Question):
            form = AskMCQuestionForm(request.POST)
        if form.is_valid():
            original = True
            for i in original_questions:
                if i.text == form.cleaned_data['text'] and i.assignment and i.assignment.student == request.user:
                    original = False
                    print('Answer is a duplicate, not saving')
            if original:
                form.save()
                print('Saved Answered')
            if isinstance(question, TF_Question):
                form_class = AskTFQuestionForm(
                    initial={'assignment': assignment, 'exam': question.exam,
                             'correct_answer': question.correct_answer,
                             'text': question.text})
                return render(request, 'Exam/ask_question.html', {'question': question, 'form': form_class})
            if isinstance(question, FIB_Question):
                form_class = AskFIBQuestionForm(
                    initial={'assignment': assignment, 'exam': question.exam,
                             'correct_answer': question.correct_answer,
                             'text': question.text})
                return render(request, 'Exam/ask_question.html', {'question': question, 'form': form_class})
            if isinstance(question, MC_Question):
                form_class = AskMCQuestionForm(
                    initial={'assignment': assignment, 'exam': question.exam,
                             'correct_answer': question.correct_answer,
                             'text': question.text})
                mc_choices = []
                if question.One:
                    mc_choices.append((1, question.One))
                if question.Two:
                    mc_choices.append((2, question.Two))
                if question.Three:
                    mc_choices.append((3, question.Three))
                if question.Four:
                    mc_choices.append((4, question.Four))
                if question.Five:
                    mc_choices.append((5, question.Five))
                mc_choices = tuple(mc_choices)
                form_class.fields['user_answer'].choices = mc_choices
                return render(request, 'Exam/ask_question.html', {'question': question, 'form': form_class})
    question = get_question()
    if question is None:
        print("Trying to go home")
        return ExamDetailView(request, assignment.test.pk)
    if isinstance(question, TF_Question):
        #Need a check to see if question already has an assignment
        form_class = AskTFQuestionForm(initial={'assignment': assignment, 'exam': question.exam, 'correct_answer':
            question.correct_answer, 'text': question.text})
        print("Too However question exam is: " + question.exam.title)
        return render(request, 'Exam/ask_question.html', {'question': question, 'form': form_class})
    if isinstance(question, FIB_Question):
        form_class = AskFIBQuestionForm(initial={'assignment': assignment, 'exam': question.exam, 'correct_answer':
            question.correct_answer, 'text': question.text})
        return render(request, 'Exam/ask_question.html', {'question': question, 'form': form_class})
    if isinstance(question, MC_Question):
        print("Is multiple choice question")
        form_class = AskMCQuestionForm()
        mc_choices = []
        if question.One:
            mc_choices.append(tuple((1, question.One)))
        if question.Two:
            mc_choices.append(tuple((2, question.Two)))
        if question.Three:
            mc_choices.append(tuple((3, question.Three)))
        if question.Four:
            mc_choices.append(tuple((4, question.Four)))
        if question.Five:
            mc_choices.append(tuple((5, question.Five)))
        mc_choices = tuple(mc_choices)
        print(mc_choices)
        form_class.fields['user_answer'].widget.choices = mc_choices
        form_class.fields['assignment'].initial = assignment
        form_class.fields['exam'].initial = question.exam
        form_class.fields['correct_answer'].initial = question.correct_answer
        form_class.fields['text'].initial = question.text
        print("About to render page for MC question")
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
