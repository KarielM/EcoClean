from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import *
from django.conf import settings
from django.core.mail import send_mail
import json
import os


# Create your views here.


def base(request):
    return redirect(request, "home,html")


def home(request):
    return render(request, "home.html")


def aboutUs(request):
    return render(request, "aboutUs.html")


def services(request):
    return render(request, "services.html")


def contact(request):
    return render(request, "contact.html")


def gallery(request):
    return render(request, "gallery.html")


ZIPCODE_FILE_PATH = os.path.join(settings.BASE_DIR, "zipcode.json")


def load_zip_codes():
    with open(ZIPCODE_FILE_PATH, "r") as file:
        data = json.load(file)
        print({int(k): v for k, v in data.items()})
    return {int(k): v for k, v in data.items()}


def validate_zipcode(request):
    print(request.POST.get("code"))
    if request.method == "POST":
        zip_code = request.POST.get("code")
        if zip_code is None:
            return JsonResponse({"error": "ZIP code is required."}, status=400)
        try:
            zip_code = int(zip_code)
        except ValueError:
            return JsonResponse(
                {"error": "Valid ZIP code is required and must be an integer."},
                status=400,
            )

        zip_codes = load_zip_codes()
        exists = zip_code in zip_codes
        return JsonResponse({"exists": exists})

    return JsonResponse({"error": "Invalid request method."}, status=405)


def contactFormView(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            message = form.cleaned_data["message"]

            email_body = (
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone Number: {phone_number}\n"
                f"{message}"
            )
            try:
                send_mail(
                    "Additional Info Requested",
                    email_body,
                    email,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                return redirect("home")
            except Exception as e:
                print(f"Error sending email: {e}")
                return redirect("home")

    else:
        form = ContactUsForm()
    return render(request, "contactUs.html", {"form": form})


def bookUsView(request):
    if request.method == "POST":
        form = BookUsForm(request.POST)

        if form.is_valid():
            business_name = form.cleaned_data["business_name"]
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            date = form.cleaned_data["date_requested"]
            street_address_1 = form.cleaned_data["street_address_1"]
            street_address_2 = (
                None
                if form.cleaned_data["street_address_2"] is not None
                else form.cleaned_data["street_address_2"]
            )
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            print(state)
            zip_code = form.cleaned_data["zip_code"]
            time_of_day, time_range = form.get_value_and_display_text()
            print(time_of_day)
            print(time_range)

            email_body = (
                "I would like to schedule an appointment and am providing the necessary details below:\n"
                f"Business Name: {business_name}\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone Number: {phone_number}\n"
                f"Address: {street_address_1}"
                + (f" {street_address_2}" if street_address_2 else "")
                + f", {city}, {state} {zip_code}\n"
                f"Preferred Date: {date}\n"
                f"Preferred Time: {time_of_day}, {time_range}\n"
                "Please let me know if this time is available or if there are any other suitable time slots. If you need any additional information to confirm the appointment, feel free to reach out.\n"
                "Thank you for your assistance, and I look forward to your response.\n"
                "Best regards,\n"
                f"{name}"
            )
            try:
                send_mail(
                    "Booking Request",
                    email_body,
                    email,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                return redirect("home")
            except Exception as e:
                print(f"Error sending email: {e}")
    else:
        form = BookUsForm()
    return render(request, "bookUs.html", {"form": form})
