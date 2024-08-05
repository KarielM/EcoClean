
from django.contrib import admin
from django.urls import path
from App.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("/contact", contact, name ="contact"),
    path("/about", aboutUs, name="about"),
    path("/services", services, name="services")
]
