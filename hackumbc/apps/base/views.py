from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index_view(request):
    context = {}
    return render(request, "base/index.html", context)
