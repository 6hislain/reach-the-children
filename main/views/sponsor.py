from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from django.contrib import messages
from ..models import Sponsor, Student


@login_required(login_url="signin")
def sponsor_index(request):
    sponsors = Sponsor.objects.order_by("-id")
    paginator = Paginator(sponsors, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "sponsor/index.html", {"page_object": page_object})


def sponsor_show(request, id):
    sponsor = get_object_or_404(Sponsor, pk=id)
    students = Student.objects.filter(sponsor_id=id).all()

    return render(
        request, "sponsor/show.html", {"sponsor": sponsor, "students": students}
    )


@login_required(login_url="signin")
def sponsor_create(request):
    if request.method == "GET":
        return render(request, "sponsor/create.html")

    elif request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        details = request.POST["details"]
        address = request.POST["address"]
        sponsor = Sponsor(
            name=name,
            email=email,
            phone=phone,
            details=details,
            address=address,
            user_id=request.user.id,
        )

        if request.FILES.get("image") != None:
            sponsor.image = request.FILES.get("image")

        sponsor.save()

        messages.info(request, "sponsor saved")
        return redirect("sponsor.index")


@login_required(login_url="signin")
def sponsor_edit(request, id):
    sponsor = get_object_or_404(Sponsor, pk=id)

    if request.method == "GET":
        return render(request, "sponsor/edit.html", {"sponsor": sponsor})

    elif request.method == "POST":
        sponsor.name = request.POST["name"]
        sponsor.phone = request.POST["phone"]
        sponsor.email = request.POST["email"]
        sponsor.details = request.POST["details"]
        sponsor.address = request.POST["address"]

        if request.FILES.get("image") != None:
            sponsor.image = request.FILES.get("image")

        if sponsor.user_id == request.user.id:
            sponsor.save()
            messages.info(request, "sponsor updated")

        return redirect("sponsor.index")


@login_required(login_url="signin")
def sponsor_delete(request, id):
    sponsor = get_object_or_404(Sponsor, pk=id)

    if sponsor.user_id == request.user.id:
        sponsor.delete()
        messages.info(request, "sponsor deleted")

    return redirect("sponsor.index")
