"""Main URL configuration for the movie theater booking project."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "",
        include("bookings.urls"),
    ),
]