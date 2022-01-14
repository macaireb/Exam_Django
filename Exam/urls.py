"""Exam_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('', HomeView.as_view() , name='home'),
    path('exam/<int:ider>/create_fib', CreateFIBView, name='create_fib'),
    path('exam/<int:ider>/create_tf', CreateTFView, name='create_tf'),
    path('exam/<int:ider>/create_mc', CreateMCView, name='create_mc'),
    path('exam/<int:ider>/create_exam', CreateExamView, name='create_exam'),
    path('exam/update_exam', EditExamView.as_view(), name='update_exam'),
    path('exam/<int:ider>/choose_question', ChooseQuestionView, name='choose_question'),
    path('exam/<int:ider>/exam_detail', ExamDetailView, name='exam_detail'),
    path('exam/<int:ider>/start_exam', StartExam, name='start_exam'),
    path('exam/<int:ider>/ask_question', AskQuestion, name='ask_question'),
    path('exam/<int:ider>/view_assignments', ViewAssignments, name='view_assignments'),
    path('exam/<int:ider>/assign_exam', AssignExam, name='assign_exam'),
]
