from django.contrib import admin
from django.urls import path
from App.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("contact/", contact, name="contact"),
    path("about/", aboutUs, name="about"),
    path("gallery/", gallery, name="gallery"),
    path("services/", services, name="services"),
    path("check-zip-code/", validate_zipcode, name="check_zip_code"),
    path("contact_us/", contactFormView, name="contactUs"),
]
