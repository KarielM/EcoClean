from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ZipCode
from .forms import ZipCodeAddForm, ZipCodeCheckForm
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


def add_zip_code(request):
    if request.method == 'POST':
        form = ZipCodeAddForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Zip code added successfully!'})
        else:
            return JsonResponse({'error': form.errors.as_json()}, status=400)
    else:
        form = ZipCodeAddForm()
    return render(request, 'contact.html', {'form': form})

def check_zip_code(request):
    if request.method == 'GET':
        form = ZipCodeCheckForm(request.GET)
        if form.is_valid():
            zip_code = form.cleaned_data['code']
            exists = ZipCode.objects.filter(code=zip_code).exists()
            return JsonResponse({'exists': exists})
        else:
            return JsonResponse({'error': form.errors.as_json()}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)



