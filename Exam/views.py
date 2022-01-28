from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
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
    template_name = 'Exam/edit_exam.html'
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
        #Need to take care of this problem later, but I believe questions are being asked twice. Once for the original
        #Then an additional time because if method==POST get_question is called before the original question was saved
        #So it sees the question it used last time still with no assignment and asks it again.
        question = get_question()
        if question:
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


def DeleteExam(request, ider):
    a = Test.objects.get(pk=ider)
    MC_Question.objects.all().filter(exam=a, assignment=None, user_answer=None).delete()
    TF_Question.objects.all().filter(exam=a, assignment=None, user_answer=None).delete()
    FIB_Question.objects.all().filter(exam=a, assignment=None, user_answer=None).delete()
    Test.objects.get(pk=ider).delete()
    return render(request, 'Exam/delete_exam.html', {'test': a})


def Delete_TF_Question(request, ider):
    a = TF_Question.objects.get(pk=ider)
    print("Trying to delete TF")
    if request.method == 'POST':
        form = delete_question(request.POST)
        print("Is form valid: " + str(form.is_valid()))
        if form.is_valid():
            delete = form.cleaned_data
            delete = delete.get('delete')
            print(str(delete) + " delete")
            if delete:
                print("attempting actual TF delete")
                TF_Question.objects.get(pk=ider).delete()
            return ExamDetailView(request, a.exam.pk)
    else:
        return render(request, 'Exam/delete_tf.html', {'form': delete_question(), 'pk': ider})


def Delete_MC_Question(request, ider):
    a = MC_Question.objects.get(pk=ider)
    if request.method == 'POST':
        form = delete_question(request.POST)
        if form.is_valid():
            delete = form.cleaned_data
            delete = delete.get('delete')
            if delete:
                MC_Question.objects.get(pk=ider).delete()
            return ExamDetailView(request, a.exam.pk)
    else:
        return render(request, 'Exam/delete_mc.html', {'form': delete_question(), 'pk': ider})


def Delete_FIB_Question(request, ider):
    a = FIB_Question.objects.get(pk=ider)
    if request.method == 'POST':
        form = delete_question(request.POST)
        if form.is_valid():
            delete = form.cleaned_data
            delete = delete.get('delete')
            if delete:
                FIB_Question.objects.get(pk=ider).delete()
            return ExamDetailView(request, a.exam.pk)
    else:
        return render(request, 'Exam/delete_fib.html', {'form': delete_question(), 'pk': ider})


class Edit_TF(UpdateView):
    model = TF_Question
    template_name = 'Exam/edit_question.html'
    form_class = edit_tf_form
    success_url = reverse_lazy('home')


class Edit_MC(UpdateView):
    model = MC_Question
    template_name = 'Exam/edit_question.html'
    form_class = edit_mc_form
    success_url = reverse_lazy('home')


class Edit_FIB(UpdateView):
    model = FIB_Question
    template_name = 'Exam/edit_question.html'
    form_class = edit_fib_form
    success_url = reverse_lazy('home')


def view_assignments(request):
    assignments = Assignment.objects.all().filter(student=request.user)
    return render(request, 'Exam/view_assignments.html', {'assignments': assignments})


def score_assignment(request, ider):
    assignment = Assignment.objects.get(pk=ider)
    tfs = TF_Question.objects.all().filter(assignment=assignment)
    fibs = FIB_Question.objects.all().filter(assignment=assignment)
    mcs = MC_Question.objects.all().filter(assignment=assignment)
    questions = list(chain(mcs, tfs, fibs))

    def score_tf(question):
        if question.user_answer is not None:
            if question.user_answer == question.correct_answer:
                print(question.text + ' is correct')
                if assignment.correct is None:
                    assignment.correct = 1
                elif assignment.correct > 0:
                    assignment.correct = assignment.correct + 1
            elif question.user_answer != question.correct_answer:
                print(question.text + ' is incorrect')
                if assignment.incorrect is None:
                    assignment.incorrect = 1
                elif assignment.incorrect > 0:
                    assignment.incorrect = assignment.incorrect + 1

    #Will need to update score_mc when there admins are able to allow multiple questions to be correct
    def score_mc(question):
        if question.user_answer is not None:
            if int(question.correct_answer) is int(question.user_answer):
                print(question.text + ' is correct')
                if assignment.correct is None:
                    assignment.correct = 1
                elif assignment.correct > 0:
                    assignment.correct = assignment.correct + 1
            elif int(question.correct_answer) is not int(question.user_answer):
                print(question.text + ' is incorrect')
                if assignment.incorrect is None:
                    assignment.incorrect = 1
                elif assignment.incorrect > 0:
                    assignment.incorrect = assignment.incorrect + 1

    def score_fib(question):
        if question.user_answer is not None:
            ua = question.user_answer.lower()
            ca = question.correct_answer.lower()
            ua = ua.replace(' the ', '')
            ca = ca.replace(' the ', '')
            ua = ua.replace(' a ', '')
            ca = ca.replace(' a ', '')
            ua = ua.replace('\'', '')
            ca = ca.replace('\'', '')
            ua = ua.replace(',', '')
            ca = ca.replace(',', '')
            ua = ua.replace(' ', '')
            ca = ca.replace(' ', '')
            if ua == ca:
                print(question.text + ' is correct')
                if assignment.correct is None:
                    assignment.correct = 1
                elif assignment.correct > 0:
                    assignment.correct = assignment.correct + 1
            if ua != ca:
                print(question.text + ' is incorrect')
                if assignment.incorrect is None:
                    assignment.incorrect = 1
                elif assignment.incorrect > 0:
                    assignment.incorrect = assignment.incorrect + 1

    if assignment.correct is None and assignment.incorrect is None:
        if tfs:
            print("trying to score TF questions")
            for tf in tfs:
                score_tf(tf)
        if mcs:
            print("trying to score MC questions")
            for mc in mcs:
                score_mc(mc)
        if fibs:
            print("trying to score FIB questions")
            for fib in fibs:
                score_fib(fib)
    if assignment.incorrect is None:
        assignment.incorrect = 0
    if assignment.correct is None:
        assignment.correct = 0
    assignment.save()
    print(str(assignment.incorrect) + str(assignment.correct))
    return render(request, 'Exam/score_assignment.html', {'assignment': assignment, 'questions': questions})


def retake_assignment(request, ider):
    old_assignment = Assignment.objects.get(pk=ider)
    assignment = old_assignment
    tfs = TF_Question.objects.all().filter(assignment=assignment)
    fibs = FIB_Question.objects.all().filter(assignment=assignment)
    mcs = MC_Question.objects.all().filter(assignment=assignment)
    questions = list(chain(mcs, tfs, fibs))
    old_questions = questions
    assignment.pk = None
    assignment.correct = None
    assignment.incorrect = None
    assignment.save()
    for i in range(len(questions)):
        questions[i].user_answer = None
        questions[i].assignment = assignment
        questions[i].text = old_questions[i].text
        questions[i].correct_answer = old_questions[i].correct_answer
        questions[i].exam = old_questions.exam
        if isinstance(questions[i], MC_Question):
            questions[i].One = old_questions[i].One
            if old_questions[i].Two:
                questions[i].Two = old_questions[i].Two
            if old_questions[i].Three:
                questions[i].Three = old_questions[i].Three
            if old_questions[i].Four:
                questions[i].Four = old_questions[i].Four
            if old_questions[i].Five:
                questions[i].Five = old_questions[i].Five

        questions[i].pk = None
        questions[i].save()
    return AskQuestion(request, assignment.pk)
