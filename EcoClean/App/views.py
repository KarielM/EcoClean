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


ZIPCODE_FILE_PATH = os.path.join(settings.BASE_DIR, "zipcode.json")

def load_zip_codes():
    with open(ZIPCODE_FILE_PATH, "r") as file:
        data = json.load(file)
    return {int(k): v for k, v in data.items()}


def validate_zipcode(request):
    print(request.POST.get("code"))
    zip_code = request.GET.get("code")
    print (zip_code)
    try:
        zip_code = int(zip_code)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Valid ZIP code is required and must be an integer."}, status=400
        )

    zip_codes = load_zip_codes()
    exists = zip_code in zip_codes
    return JsonResponse({"exists": exists})


def contactFormView(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            email_subject = subject or "Contact Us Form Submission"
            email_body = (
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone Number: {phone_number}\n"
                f"Message:\n{message}"
            )
            try:
                send_mail(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )
                return redirect('home')
            except Exception as e:
                print(f"Error sending email: {e}")
                return redirect('home')
                
    else:
        form = ContactUsForm()
    return render(request, "contactUs.html", {"form": form})
