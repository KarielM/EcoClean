from django.shortcuts import render, redirect

# Create your views here.


def base(request):

    return render(request, "base.html")


def home(request):
    return render(request, "home.html")


def aboutUs(request):
    return render(request, "aboutUs.html")


def services(request):
    return render(request, "services.html")


def contact(request):
    return render(request, "contact.html")
