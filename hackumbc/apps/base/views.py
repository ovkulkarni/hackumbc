from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..users.models import User


def index_view(request):
    context = {}
    return render(request, "base/index.html", context)


def info_view(request):
    context = {}
    return render(request, "base/info.html", context)
