from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from django.contrib import messages
from ..models import Payment, Student, School, Sponsor


@login_required(login_url="signin")
def payment_index(request):
    payments = Payment.objects.order_by("-id")
    paginator = Paginator(payments, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "payment/index.html", {"page_object": page_object})


@login_required(login_url="signin")
def payment_show(request, id):
    payment = get_object_or_404(Payment, pk=id)
    return JsonResponse(model_to_dict(payment))


@login_required(login_url="signin")
def payment_create(request):
    if request.method == "GET":
        schools = School.objects.all()
        sponsors = Sponsor.objects.all()
        students = Student.objects.all()

        return render(
            request,
            "payment/create.html",
            {"schools": schools, "sponsors": sponsors, "students": students},
        )

    elif request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        payment_type = request.POST["type"]
        student = request.POST["student"]
        sponsor = request.POST["sponsor"]
        school = request.POST["school"]
        payment = Payment(
            amount=amount,
            description=description,
            payment_type=payment_type,
            student_id=student,
            sponsor_id=sponsor,
            school_id=school,
            user_id=request.user.id,
        )

        payment.save()

        messages.info(request, "payment saved")
        return redirect("payment.index")


@login_required(login_url="signin")
def payment_edit(request, id):
    payment = get_object_or_404(Payment, pk=id)

    if request.method == "GET":
        schools = School.objects.all()
        sponsors = Sponsor.objects.all()
        students = Student.objects.all()

        return render(
            request,
            "payment/edit.html",
            {
                "payment": payment,
                "schools": schools,
                "sponsors": sponsors,
                "students": students,
            },
        )

    elif request.method == "POST":
        payment.amount = request.POST["amount"]
        payment.student_id = request.POST["student"]
        payment.sponsor_id = request.POST["sponsor"]
        payment.school_id = request.POST["school"]
        payment.description = request.POST["description"]
        payment.payment_type = request.POST["type"]

        if payment.user_id == request.user.id:
            payment.save()
            messages.info(request, "payment updated")

        return redirect("payment.index")


@login_required(login_url="signin")
def payment_delete(request, id):
    payment = get_object_or_404(Payment, pk=id)

    if payment.user_id == request.user.id:
        payment.delete()
        messages.info(request, "payment deleted")

    return redirect("payment.index")
