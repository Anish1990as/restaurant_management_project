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
            return redirect("profile")  # same page reload
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "account/profile.html", {"form": form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')