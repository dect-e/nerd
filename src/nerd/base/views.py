from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import render, redirect

from verify_email.email_handler import send_verification_email

from .forms import UserCreationForm

class IndexView(TemplateView):
    template_name = "base/index.html"

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            messages.success(request, 'Account created successfully. A verification email has been sent')
            return redirect('register')

    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
