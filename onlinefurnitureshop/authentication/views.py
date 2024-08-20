
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from about.models import Profile
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Create or update profile
            profile, created = Profile.objects.get_or_create(user=user)
            profile.address = form.cleaned_data['address']
            profile.city = form.cleaned_data['city']
            profile.save()

            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()  # Initialize an empty form for GET requests

    return render(request, 'registration/register.html', {'form': form})



