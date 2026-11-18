from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("vacancies/", views.vacancy_list, name="vacancy_list"),
    path("vacancies/<int:pk>/", views.vacancy_detail, name="vacancy_detail"),
    path("apply/", views.apply, name="apply"),
    path("shipowners/", views.shipowners, name="shipowners"),
]
