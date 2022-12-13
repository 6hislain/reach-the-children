from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("logout", views.logout, name="logout"),
    # path("search", views.search, name="search"),
    path("school", views.school_index, name="school.index"),
    path("school/create", views.school_create, name="school.create"),
    path("school/<int:id>/edit", views.school_edit, name="school.edit"),
    path("school/<int:id>/delete", views.school_delete, name="school.delete"),
    path("school/<int:id>", views.school_show, name="school.show"),
    path("student", views.student_index, name="student.index"),
    path("student/create", views.student_create, name="student.create"),
    path("student/<int:id>/edit", views.student_edit, name="student.edit"),
    path("student/<int:id>/delete", views.student_delete, name="student.delete"),
    path("student/<int:id>", views.student_show, name="student.show"),
    path("sponsor", views.sponsor_index, name="sponsor.index"),
    path("sponsor/create", views.sponsor_create, name="sponsor.create"),
    path("sponsor/<int:id>/edit", views.sponsor_edit, name="sponsor.edit"),
    path("sponsor/<int:id>/delete", views.sponsor_delete, name="sponsor.delete"),
    path("sponsor/<int:id>", views.sponsor_show, name="sponsor.show"),
    path("grade", views.grade_index, name="grade.index"),
    path("grade/create", views.grade_create, name="grade.create"),
    path("grade/<int:id>/edit", views.grade_edit, name="grade.edit"),
    path("grade/<int:id>/delete", views.grade_delete, name="grade.delete"),
    path("grade/<int:id>", views.grade_show, name="grade.show"),
]
