from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import time
from App.models import *
import os
from django.conf import settings

ZIPCODE_FILE_PATH = os.path.join(settings.BASE_DIR, "zipcode.json")


class ZipCodeForm(forms.Form):
    zipcode = forms.CharField(max_length=10, label="zipcode")


class ContactUsForm(forms.Form):
    name = forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Name"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Your Email"}
        ),
    )
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
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Phone Number"}
        ),
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Your Message"}
        ),
    )


class BookUsForm(forms.Form):
    Time_Slot_Options = (
        ("Morning", "8:00 AM - 12:30 PM"),
        ("Afternoon", "12:30 PM - 4:30 PM"),
    )
    States_Serviced = (
        ("AR", "Arkansas"),
        ("MS", "Mississippi"),
        ("TN", "Tennessee"),
    )

    business_name = forms.CharField(
        label="Business Name",
        max_length=250,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Business Name"}
        ),
    )
    name = forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Name"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your Email (EXAMPLE@EXAMPLE.COM)",
            }
        ),
    )
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
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your Phone Number (1234567890)",
            }
        ),
    )
    street_address_1 = forms.CharField(
        label="Street Address",
        max_length=250,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Street Address"}
        ),
    )
    street_address_2 = forms.CharField(
        label="Apt./Suite",
        max_length=250,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Apt./Suite"}
        ),
    )
    city = forms.CharField(
        label="City",
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your City"}
        ),
    )
    state = forms.ChoiceField(
        label="State",
        choices=States_Serviced,
        widget=forms.RadioSelect,
        required=True,
        initial=None,
    )
    zip_code = forms.CharField(
        label="ZIP",
        max_length=5,
        validators=[
            RegexValidator(regex=r"^\d+$", message="ZIP code must contain only digits.")
        ],
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your ZIP (12345)"}
        ),
    )
    date_requested = forms.DateField(
        input_formats=["%m/%d/%Y"],
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Date Requested (MM/DD/YYYY)",
            }
        ),
    )
    time = forms.ChoiceField(
        label="Time Slot Requested:",
        choices=Time_Slot_Options,
        initial="",
    )

    def clean(self):
        cleaned_data = super().clean()
        date_requested = cleaned_data.get("date_requested")

        if date_requested:
            cleaned_data["date_requested"] = date_requested.strftime("%m/%d/%Y")

        return cleaned_data

    def get_value_and_display_text(self):
        selected_time_value = self.cleaned_data.get("time")
        selected_time_display_text = dict(self.Time_Slot_Options).get(
            selected_time_value
        )
        return selected_time_value, selected_time_display_text
