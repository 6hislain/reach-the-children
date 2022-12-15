from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from django.contrib import messages
from ..models import Student, School, Grade


@login_required(login_url="signin")
def grade_index(request):
    grades = Grade.objects.order_by("-id")
    paginator = Paginator(grades, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "grade/index.html", {"page_object": page_object})


@login_required(login_url="signin")
def grade_show(request, id):
    grade = get_object_or_404(Grade, pk=id)
    return JsonResponse(model_to_dict(grade))


@login_required(login_url="signin")
def grade_create(request):
    if request.method == "GET":
        schools = School.objects.all()
        students = Student.objects.all()

        return render(
            request,
            "grade/create.html",
            {"schools": schools, "students": students},
        )

    elif request.method == "POST":
        marks = request.POST["marks"]
        semester = request.POST["semester"]
        year = request.POST["year"]
        description = request.POST["description"]
        student = request.POST["student"]
        school = request.POST["school"]
        grade = Grade(
            marks=marks,
            year=year,
            semester=semester,
            description=description,
            student_id=student,
            school_id=school,
            user_id=request.user.id,
        )

        grade.save()

        messages.info(request, "grade saved")
        return redirect("grade.index")


@login_required(login_url="signin")
def grade_edit(request, id):
    grade = get_object_or_404(Grade, pk=id)

    if request.method == "GET":
        schools = School.objects.all()
        students = Student.objects.all()
        return render(request, "grade/edit.html", {"grade": grade, "schools": schools})

    elif request.method == "POST":
        grade.marks = request.POST["marks"]
        grade.semester = request.POST["semester"]
        grade.year = request.POST["year"]
        grade.description = request.POST["description"]
        grade.student_id = request.POST["student"]
        grade.school_id = request.POST["school"]

        if grade.user_id == request.user.id:
            grade.save()
            messages.info(request, "grade updated")

        return redirect("grade.index")


@login_required(login_url="signin")
def grade_delete(request, id):
    grade = get_object_or_404(Grade, pk=id)

    if grade.user_id == request.user.id:
        grade.delete()
        messages.info(request, "grade deleted")

    return redirect("grade.index")
