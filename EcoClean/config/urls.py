
from django.contrib import admin
from django.urls import path
from App.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("/contact", contact, name ="contact"),
    path("/about", aboutUs, name="about"),
    path("/services", services, name="services"),
    path('add-zip-code/', add_zip_code, name='add_zip_code'),
    path('check-zip-code/', check_zip_code, name='check_zip_code'),
]
