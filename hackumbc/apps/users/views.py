from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import AuthenticateForm, CreateUserForm
from .models import User


def login_view(request):
    if request.method == "POST":
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_page = request.POST.get("next", request.GET.get("next", reverse("index")))
            messages.success(request, "Successfully Logged In!")
            return redirect(next_page)
    else:
        form = AuthenticateForm()
    context = {"form": form}
    return render(request, "show_form.html", context)


@login_required
def profile_view(request):
    my_dues = request.user.dues.exclude(bought_by=request.user)
    receipts_for_dues = set([item.receipt for item in my_dues])
    context = {"receipts_due": receipts_for_dues}
    return render(request, "users/profile.html", context)


def registration_view(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                u = User.objects.create_user(username=form.cleaned_data.get("username"),
                                             email=form.cleaned_data.get("email"),
                                             first_name=form.cleaned_data.get("first_name"),
                                             last_name=form.cleaned_data.get("last_name"),
                                             password=form.cleaned_data.get("password"))
                messages.success(request, "Successfully Registered!")
                return redirect(reverse("login"))
            except Exception as e:
                messages.error(request, e)
                context = {"form": form}
                return render(request, "show_form.html", context)
    else:
        form = CreateUserForm()
    context = {"form": form}
    return render(request, "show_form.html", context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Successfully Logged Out!")
    return redirect(reverse("index"))
