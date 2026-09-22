from django.urls import path

from . import views

app_name = "tank"

urlpatterns = [
    path("", views.index, name="index"),
    path("fish/<int:pk>/feed/", views.feed, name="feed"),
    path("fish/<int:pk>/release/", views.release, name="release"),
]
