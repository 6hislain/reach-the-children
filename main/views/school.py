from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from django.contrib import messages
from ..models import School


@login_required(login_url="signin")
def school_index(request):
    schools = School.objects.order_by("-id")
    paginator = Paginator(schools, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "school/index.html", {"page_object": page_object})


@login_required(login_url="signin")
def school_show(request, id):
    school = get_object_or_404(School, pk=id)
    return JsonResponse(model_to_dict(school))


@login_required(login_url="signin")
def school_create(request):
    if request.method == "GET":
        return render(request, "school/create.html")

    elif request.method == "POST":
        name = request.POST["name"]
        details = request.POST["details"]
        address = request.POST["address"]
        school = School(
            name=name, details=details, address=address, user_id=request.user.id
        )

        if request.FILES.get("image") != None:
            school.image = request.FILES.get("image")

        school.save()

        messages.info(request, "school saved")
        return redirect("school.index")


@login_required(login_url="signin")
def school_edit(request, id):
    school = get_object_or_404(School, pk=id)

    if request.method == "GET":
        return render(request, "school/edit.html", {"school": school})

    elif request.method == "POST":
        school.name = request.POST["name"]
        school.details = request.POST["details"]
        school.address = request.POST["address"]

        if request.FILES.get("image") != None:
            school.image = request.FILES.get("image")

        if school.user_id == request.user.id:
            school.save()
            messages.info(request, "school updated")

        return redirect("school.index")


@login_required(login_url="signin")
def school_delete(request, id):
    school = get_object_or_404(School, pk=id)

    if school.user_id == request.user.id:
        school.delete()
        messages.info(request, "school deleted")

    return redirect("school.index")
