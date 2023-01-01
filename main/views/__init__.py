from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.db.models import Sum
from django.contrib import messages
from ..models import School, Sponsor, Student
from .sponsor import *
from .student import *
from .school import *
from .visit import *
from .grade import *

# Create your views here.
@require_http_methods(["GET"])
def home(request):
    schools = School.objects.order_by("-id")[:10]
    sponsors = Sponsor.objects.order_by("-id")[:10]

    return render(
        request,
        "home.html",
        {"schools": schools, "sponsors": sponsors},
    )


@require_http_methods(["GET"])
@login_required(login_url="signin")
def dashboard(request):
    school_count = School.objects.count()
    sponsor_count = Sponsor.objects.count()
    student_count = Student.objects.count()

    return render(
        request,
        "dashboard.html",
        {
            "school_count": school_count,
            "student_count": student_count,
            "sponsor_count": sponsor_count,
        },
    )


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")

    elif request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == "" or password != confirm_password:
            messages.info(request, "Password do not match")
            return redirect("signup")

        if email == "" or User.objects.filter(email=email).exists():
            messages.info(request, "Email already taken")
            return redirect("signup")

        if username == "" or User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect("signup")

        new_user = User.objects.create_user(
            username=username, email=email, password=password
        )
        new_user.save()

        user_login = auth.authenticate(username=username, password=password)
        auth.login(request, user_login)

        user_model = User.objects.get(email=email)
        return redirect("dashboard")


@require_http_methods(["GET", "POST"])
def signin(request):
    if request.method == "GET":
        return render(request, "signin.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Invalid credentials")
            return redirect("signin")

        auth.login(request, user)
        return redirect("dashboard")


@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("home")
