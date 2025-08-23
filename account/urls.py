from django.urls import path
from .views import *

urlpatterns = [
    path("profile/", profile_view, name="profile"),
]