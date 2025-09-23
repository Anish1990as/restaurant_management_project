from django.http import JsonResponse
from utils.validation_utils import is_valid_email
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")   
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "account/profile.html", {"form": form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


def register_user(request):
    email = request.POST.get("email")
    if not is_valid_email(email):
        return JsonResponse({"error": "Invalid email address"}, status=400)

    # user creation logic yaha aayega
    return JsonResponse({"success": "User registered"})
