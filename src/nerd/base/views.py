from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from verify_email.email_handler import send_verification_email

from .forms import UserCreationForm
from .models import Extension

class IndexView(TemplateView):
    template_name = 'base/index.html'

class ExtensionsView(LoginRequiredMixin, ListView):
    template_name = 'base/extensions.html'
    context_object_name = 'user_extensions'
    # TODO: link to edit view
    # TODO: allow to add/delete extensions

    def get_queryset(self):
        return Extension.objects.filter(owner=self.request.user)

class ExtensionEditView(LoginRequiredMixin, UpdateView):
    model = Extension
    template_name_suffix = '_edit'
    fields = ['name']
    success_url = reverse_lazy('extensions')
    # TODO: validation

    def get_queryset(self):
        return Extension.objects.filter(owner=self.request.user)

class PhonebookView(ListView):
    template_name = 'base/phonebook.html'
    context_object_name = 'extensions'
    paginate_by = 20
    ordering = ['number'] # TODO: set in gui

    def get_queryset(self):
        # TODO: search
        # form = PhonebookSearchForm(self.request.GET)
        # if form.is_valid()
        #     param = form.cleaned_data['search']
        #     return Extension.objects.filter(public=True).filter(Q(name__icontains=param) | Q(number__icontains=param)).order_by(*self.ordering)
        # return all objects if search form is invalid (e.g. empty)
        return Extension.objects.filter(public=True).order_by(*self.ordering)

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
