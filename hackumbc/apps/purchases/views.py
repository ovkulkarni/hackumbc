from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.text import slugify
from django.contrib import messages

from tesserocr import PyTessBaseAPI

from ..users.models import User
from .models import Receipt, Item
from .forms import NewReceiptForm


def read_receipt_text(image):
    with PyTessBaseAPI() as api:
        api.SetImageFile(image)
        return api.GetUTF8Text()


def is_float(value):
    try:
        float(value)
        if value.isdigit():
            return False
        return True
    except ValueError:
        return False


def handle_receipt_text(text, receipt):
    items_list = []
    lines = text.split("\n")
    END_WORDS = ["SUBTOTAL", "TAX", "TOTAL"]
    COMPLETED = False
    for line in lines:
        if COMPLETED:
            break
        item_name = ""
        item_price = None
        for word in line.split():
            if COMPLETED:
                break
            if not is_float(word):
                if slugify(word).upper() not in END_WORDS:
                    item_name += " {}".format(slugify(word).upper())
                else:
                    COMPLETED = True
                    break
            else:
                item_price = float(word)
                break
        if not item_price or not item_name:
            continue
        i = Item()
        i.receipt = receipt
        i.name = item_name
        i.price = item_price
        print(i)
        i.save()
        items_list.append(i)
    return items_list


@login_required
def create_new_receipt_view(request):
    if request.method == "POST":
        form = NewReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            r = form.save(commit=False)
            r.user = request.user
            r.save()
            return redirect(reverse("edit_receipt", kwargs={'receipt_id': r.id}))
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
        return redirect(reverse("user_profile"))
    else:
        if not receipt.items.all().count() > 0:
            items = handle_receipt_text(read_receipt_text(settings.MEDIA_ROOT + receipt.image.url), receipt)
            context["items"] = items
        else:
            context["items"] = receipt.items.all()
        context["users"] = User.objects.all()
    return render(request, "purchases/handle_new_receipt.html", context)


@login_required
def receipt_info_view(request, receipt_id):
    r = Receipt.objects.get(id=receipt_id)
    if r.user is request.user or r.items.filter(bought_for=request.user).count() > 0:
        total = 0.00
        for item in receipt.items:
            if r.user is request.user or item.bought_for is request.user:
                total += item.price
        context = {"receipt": r, "total": total}
        return render(request, "purchases/receipt_info.html", context)
    else:
        messages.error(request, "Permission Denied")
        return redirect(reverse("index"))
