from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import time
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
    message = forms.CharField(label="Message", widget=forms.Textarea)


from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import time

class BookUsForm(forms.Form):
    business_name = forms.CharField(label="Business Name", max_length=250)
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
    street_address_1 = forms.CharField(label="Street Address", max_length=250)
    street_address_2 = forms.CharField(label="Apt./Suite", max_length=250, required=False)
    city = forms.CharField(label="City", max_length=50)
    state = forms.CharField(label="State", max_length=2)
    zip_code = forms.CharField(
        label="ZIP",
        max_length=5,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='ZIP code must contain only digits.'
            )
        ],
        required=True
    )
    date_requested = forms.DateField(input_formats=['%m/%d/%Y'], required=True)
    time = forms.TimeField(input_formats=['%I:%M %p'], required=True)

    def clean(self):
        cleaned_data = super().clean()
        date_requested = cleaned_data.get('date_requested')
        time_requested = cleaned_data.get('time')

        if time_requested:
            start_time = time(8, 0)
            end_time = time(16, 30)
            if not (start_time <= time_requested <= end_time):
                raise ValidationError(f'Requested time must be between {start_time.strftime("%H:%M %p")} and {end_time.strftime("%I:%M %p")}.')

        if date_requested:
            cleaned_data['date_requested'] = date_requested.strftime('%m/%d/%Y')
        if time_requested:
            cleaned_data['time'] = time_requested.strftime('%I:%M %p')

        return cleaned_data

