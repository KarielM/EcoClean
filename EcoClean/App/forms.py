from django import forms
from django.core.validators import RegexValidator
from App.models import *


class ZipCodeAddForm(forms.ModelForm):
    class Meta:
        model = ZipCode
        fields = ["code"]
        widgets = {
            "code": forms.TextInput(attrs={"placeholder": "Enter zip code"}),
        }


class ZipCodeCheckForm(forms.Form):
    code = forms.IntegerField(
        required=True,
        min_value=0,
        error_messages={
            "required": "Zip code is required.",
            "invalid": "Enter a valid integer zip code.",
        },
    )
