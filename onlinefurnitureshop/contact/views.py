from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from about.models import Profile

@login_required
def contact(request):
    if request.method == 'POST':
        msg = request.POST.get('message')
        profile = Profile.objects.get(user=request.user)
        profile.msg = msg
        profile.save()
        messages.success(request, 'Your message has been updated successfully.')
        return redirect('contact')  # Redirect to the same page or another page after submission

    return render(request, 'contact.html')
