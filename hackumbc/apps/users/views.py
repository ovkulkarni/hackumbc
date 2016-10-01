from django.conf import settings
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import AuthenticateForm


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
    return render(request, "auth/login.html", context)


def logout_view(request):
    logout(request)
    return redirect(reverse("login"))
