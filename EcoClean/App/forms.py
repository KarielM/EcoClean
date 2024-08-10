from django import forms
from django.core.validators import RegexValidator
from App.models import *

import json
import os
from django.conf import settings

ZIPCODE_FILE_PATH = os.path.join(settings.BASE_DIR, "zipcode.json")


class ZipCodeForm(forms.Form):
    zipcode = forms.CharField(max_length=10, label="zipcode")


class ContactUsForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    email = forms.EmailField(label="Email")
    phone_number = forms.CharField(
        label="Phone Number",
        max_length=11,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.',
            )
        ],
        required=False,
    )
    subject = forms.CharField(label="subject", max_length=250, required=False)
    message = forms.CharField(label="Message", widget=forms.Textarea)
