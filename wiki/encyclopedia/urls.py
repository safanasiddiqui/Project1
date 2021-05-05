from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.topic , name="topic"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("edit", views.edit, name="edit"),
    path("edit/<str:title>", views.edit, name="edit"), 
    path("random", views.randompage , name="randompage")
]
