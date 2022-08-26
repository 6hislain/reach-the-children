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
        amount = request.POST["amount"]
        description = request.POST["description"]
        grade_type = request.POST["type"]
        student = request.POST["student"]
        sponsor = request.POST["sponsor"]
        school = request.POST["school"]
        grade = Grade(
            amount=amount,
            description=description,
            grade_type=grade_type,
            student_id=student,
            sponsor_id=sponsor,
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
        return render(request, "grade/edit.html", {"grade": grade})

    elif request.method == "POST":
        grade.name = request.POST["name"]
        grade.phone = request.POST["phone"]
        grade.email = request.POST["email"]
        grade.details = request.POST["details"]
        grade.address = request.POST["address"]

        if request.FILES.get("image") != None:
            grade.image = request.FILES.get("image")

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
