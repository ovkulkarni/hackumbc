from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import AuthenticateForm, CreateUserForm
from .models import User


def login_view(request):
    if request.method == "POST":
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            print("Form is valid!")
            login(request, form.get_user())
            next_page = request.POST.get("next", request.GET.get("next", reverse("index")))
            return redirect(next_page)
    else:
        form = AuthenticateForm()
    context = {"form": form}
    return render(request, "show_form.html", context)


def profile_view(request):
    my_dues = request.user.dues.exclude(bought_by=request.user)
    receipts_for_dues = set([item.receipt for item in my_dues])
    context = {"receipts_due": receipts_for_dues}
    return render(request, "users/profile.html", context)


def registration_view(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            u = User.objects.create_user(username=form.cleaned_data.get("username"),
                                         email=form.cleaned_data.get("email"),
                                         first_name=form.cleaned_data.get("first_name"),
                                         last_name=form.cleaned_data.get("last_name"),
                                         password=form.cleaned_data.get("password"))
            return redirect(reverse("login"))
    else:
        form = CreateUserForm()
    context = {"form": form}
    return render(request, "show_form.html", context)


def logout_view(request):
    logout(request)
    return redirect(reverse("index"))
