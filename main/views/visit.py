from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from django.contrib import messages
from ..models import Student, School, Grade, Visit, Sponsor


@login_required(login_url="signin")
def visit_index(request):
    visits = Visit.objects.order_by("-id")
    paginator = Paginator(visits, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "visit/index.html", {"page_object": page_object})


@login_required(login_url="signin")
def visit_show(request, id):
    visit = get_object_or_404(Visit, pk=id)
    return JsonResponse(model_to_dict(visit))


@login_required(login_url="signin")
def visit_create(request):
    if request.method == "GET":
        schools = School.objects.all()
        students = Student.objects.all()
        sponsors = Sponsor.objects.all()

        return render(
            request,
            "visit/create.html",
            {"schools": schools, "students": students, "sponsors": sponsors},
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
def visit_edit(request, id):
    grade = get_object_or_404(Grade, pk=id)

    if request.method == "GET":
        schools = School.objects.all()
        students = Student.objects.all()
        return render(request, "visit/edit.html", {"grade": grade, "schools": schools})

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
def visit_delete(request, id):
    visit = get_object_or_404(Visit, pk=id)

    if visit.user_id == request.user.id:
        visit.delete()
        messages.info(request, "visit deleted")

    return redirect("visit.index")
