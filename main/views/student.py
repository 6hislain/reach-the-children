from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from django.contrib import messages
from ..models import Student, Sponsor, School, Grade


@login_required(login_url="signin")
def student_index(request):
    students = Student.objects.order_by("-id")
    paginator = Paginator(students, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "student/index.html", {"page_object": page_object})


def student_show(request, id):
    student = get_object_or_404(Student, pk=id)
    grades = Grade.objects.filter(student_id=id).all()

    return render(request, "student/show.html", {"student": student, "grades": grades})


@login_required(login_url="signin")
def student_create(request):
    if request.method == "GET":
        schools = School.objects.all()
        sponsors = Sponsor.objects.all()

        return render(
            request, "student/create.html", {"schools": schools, "sponsors": sponsors}
        )

    elif request.method == "POST":
        name = request.POST["name"]
        gender = request.POST["gender"]
        level = request.POST["level"]
        father = request.POST["father"]
        mother = request.POST["mother"]
        phone = request.POST["phone"]
        siblings = request.POST["siblings"]
        dob = request.POST["dob"]
        details = request.POST["details"]
        sponsor = request.POST["sponsor"]
        school = request.POST["school"]
        address = request.POST["address"]
        student = Student(
            gender=gender,
            academic_level=level,
            father=father,
            mother=mother,
            phone=phone,
            siblings=siblings,
            name=name,
            details=details,
            address=address,
            dob=dob,
            sponsor_id=sponsor,
            school_id=school,
            user_id=request.user.id,
        )

        if request.FILES.get("image") != None:
            student.image = request.FILES.get("image")

        student.save()

        messages.info(request, "student saved")
        return redirect("student.index")


@login_required(login_url="signin")
def student_edit(request, id):
    student = get_object_or_404(Student, pk=id)

    if request.method == "GET":
        return render(request, "student/edit.html", {"student": student})

    elif request.method == "POST":
        student.name = request.POST["name"]
        student.phone = request.POST["phone"]
        student.gender = request.POST["gender"]
        student.details = request.POST["details"]
        student.address = request.POST["address"]
        student.academic_level = request.POST["level"]
        student.father = request.POST["father"]
        student.mother = request.POST["mother"]
        student.siblings = request.POST["siblings"]
        # student.dob = request.POST["dob"]
        student.sponsor_id = request.POST["sponsor"]
        student.school_id = request.POST["school"]

        if request.FILES.get("image") != None:
            student.image = request.FILES.get("image")

        if student.user_id == request.user.id:
            student.save()
            messages.info(request, "student updated")

        return redirect("student.index")


@login_required(login_url="signin")
def student_delete(request, id):
    student = get_object_or_404(Student, pk=id)

    if student.user_id == request.user.id:
        student.delete()
        messages.info(request, "student deleted")

    return redirect("student.index")
