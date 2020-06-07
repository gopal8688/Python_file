from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerForm


# Create your views here.


def user_register(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            Customer.objects.create_user(request.POST['email'], request.POST['name'], request.POST['password'])
            return redirect("login")
        else:
            render(request, "employee/registration.html", {"errors": form.errors, "form": CustomerForm()})
    return render(request, "employee/registration.html", {"form": CustomerForm()})


def user_login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect("details")
        else:
            return render(request, "employee/login.html", {"errors": "Invalid Credentials."})
    else:
        return render(request, "employee/login.html")


@login_required(login_url="/login/")
def user_edit(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if request.method == "POST":
        customer.name = request.POST.get('name')
        customer.set_password(request.POST.get("password"))
        customer.save()
        return redirect("details")
    return render(request, "employee/edit_user.html", {"customer": customer})


@login_required(login_url="/login/")
def user_details(request):
    customers = Customer.objects.all()
    return render(request, "employee/details.html", {"customers": customers})


@login_required(login_url="/login/")
def user_logout(request):
    logout(request)
    return redirect("login")
