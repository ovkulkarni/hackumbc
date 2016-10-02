from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify

from ..users.models import User


def user_directory_path(instance, filename):
    cleaned_filename = ".".join([slugify(f) for f in filename.rsplit(".", 1)])
    return 'user_{0}/{1}'.format(instance.user.id, cleaned_filename)


class Receipt(models.Model):
    user = models.ForeignKey(User, related_name="receipts", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, null=True)


class Item(models.Model):
    receipt = models.ForeignKey(Receipt, related_name="items", on_delete=models.CASCADE)
    bought_by = models.ForeignKey(User, related_name="purchases", on_delete=models.CASCADE, null=True)
    bought_for = models.ForeignKey(User, related_name="dues", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    paid = models.BooleanField(default=False)
