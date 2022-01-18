from django import forms
from .models import *
from django.contrib.auth.models import User


class CreateExam(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('title', 'proctor')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Please Enter the exams Title'}),
            'proctor': forms.Select(attrs={'class': 'form-control',})
        }


class UpdateExam(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Please Enter the exams Title'}),
        }


class CreateFIBForm(forms.ModelForm):
    class Meta:
        model = FIB_Question
        fields = ('text', 'correct_answer', 'exam')
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Enter text of the question'}),
            'correct_answer': forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Enter the correct answer'}),
            'exam': forms.Select(attrs={'class': 'form-control'}),
        }


class CreateTFForm(forms.ModelForm):
    class Meta:
        model = TF_Question
        fields = ('text', 'correct_answer', 'exam')
        true_false_choices = (
            (True, 'Yes'),
            (False, 'No')
        )
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Enter text of the question'}),
            'correct_answer': forms.Select(choices=true_false_choices, attrs={'class': 'form-control'}),
            'exam': forms.Select(attrs={'class': 'form-control'}),
        }


class CreateMCForm(forms.ModelForm):
    class Meta:
        model = MC_Question
        fields = ('text', 'One', 'Two', 'Three', 'Four',
                  'Five', 'correct_answer', 'exam')
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Enter text of the question'}),
            'One': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Enter text of possible answer 1'}),
            'Two': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Enter text of possible answer 2'}),
            'Three': forms.TextInput(attrs={'class': 'form-control',
                                          'placeholder': 'Enter text of possible answer 3'}),
            'Four': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Enter text of possible answer 4'}),
            'Five': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Enter text of possible answer 5'}),
            'correct_answer': forms.Select(attrs={'class': 'form-control'}),
            'exam': forms.Select(attrs={'class': 'form-control'}),
        }


class AskTFQuestionForm(forms.ModelForm):
    class Meta:
        model = TF_Question
        fields = ('text', 'user_answer', 'assignment', 'correct_answer', 'exam',)
        true_false_choices = (
            (True, 'Yes'),
            (False, 'No')
        )
        widgets = {
            'user_answer': forms.Select(choices=true_false_choices, attrs={'class': 'form-control'}),
            'assignment': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'correct_answer': forms.HiddenInput(),
            'exam': forms.HiddenInput(),
        }


class AskFIBQuestionForm(forms.ModelForm):
    class Meta:
        model = FIB_Question
        fields = ('text', 'user_answer', 'assignment', 'correct_answer', 'exam',)
        widgets = {
            'user_answer': forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Enter text of the answer'}),
            'text': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'assignment': forms.Select(attrs={'class': 'form-control'}),
            'correct_answer': forms.HiddenInput(),
            'exam': forms.HiddenInput(),
        }


class AskMCQuestionForm(forms.ModelForm):
    class Meta:
        model = MC_Question
        fields = ('text', 'user_answer', 'assignment', 'correct_answer', 'exam',)
        empty_choices = ((1, 'One'),
                         (2, 'Two')
                         )
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'user_answer': forms.Select(attrs={'class': 'form-control'}),
            'assignment': forms.Select(attrs={'class': 'form-control'}),
            'correct_answer': forms.HiddenInput(),
            'exam': forms.HiddenInput(),

        }


class AssignExamForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('student', 'test', 'correct', 'incorrect',)
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'test': forms.Select(attrs={'class': 'form-control'}),
            'correct': forms.HiddenInput(),
            'incorrect': forms.HiddenInput(),
        }