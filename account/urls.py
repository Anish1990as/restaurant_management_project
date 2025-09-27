from django.urls import path, include
from .views import *
from .views import UserProfileUpdateView

urlpatterns = [
    path('api/account/', include('account.urls')),
    path("profile/", profile_view, name="profile"),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
]