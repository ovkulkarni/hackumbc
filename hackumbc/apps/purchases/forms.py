from django import forms

from .models import Receipt


class NewReceiptForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewReceiptForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Receipt
        fields = ["name", "image"]
