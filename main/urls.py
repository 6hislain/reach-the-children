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
    path("payment", views.payment_index, name="payment.index"),
    path("payment/create", views.payment_create, name="payment.create"),
    path("payment/<int:id>/edit", views.payment_edit, name="payment.edit"),
    path("payment/<int:id>/delete", views.payment_delete, name="payment.delete"),
    path("payment/<int:id>", views.payment_show, name="payment.show"),
]
