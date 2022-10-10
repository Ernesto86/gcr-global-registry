from django.urls import path

from . import views

urlpatterns = [
    path(
        "countries/", views.ListSysCountriesAPIView.as_view(), name="countries"
    ),
]
