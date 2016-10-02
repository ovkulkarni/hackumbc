from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from tesserocr import PyTessBaseAPI
from decimal import Decimal

from ..users.models import User
from .models import Receipt, Item
from .forms import NewReceiptForm


def read_receipt_text(image):
    with PyTessBaseAPI() as api:
        api.SetImageFile(image)
        return api.GetUTF8Text()


def handle_receipt_text(text, receipt):
    i = Item()
    i.receipt = receipt
    i.name = "Test Item"
    i.price = 125.00
    i.save()
    return [i]


@login_required
def create_new_receipt_view(request):
    if request.method == "POST":
        form = NewReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            r = form.save(commit=False)
            r.user = request.user
            r.save()
            return redirect(reverse("edit_receipt", r.id))
    else:
        form = NewReceiptForm()
    context = {"form": form}
    return render(request, "purchases/create_new_receipt.html", context)


@login_required
def edit_receipt_view(request, receipt_id):
    receipt = Receipt.objects.get(id=receipt_id)
    context = {"receipt": receipt}
    if request.method == "POST":
        for field in request.POST:
            if field.startswith("item"):
                i = Item.objects.get(id=int(request.POST[field]))
                u = User.objects.get(username=request.POST["dueBy-{}".format(i.id)])
                i.bought_by = request.user
                i.bought_for = u
                i.save()
        return redirect(reverse("index"))
    else:
        items = handle_receipt_text(read_receipt_text(settings.MEDIA_ROOT + receipt.image.url), receipt)
        context["items"] = items
        context["users"] = User.objects.all()
    return render(request, "purchases/handle_new_receipt.html", context)
