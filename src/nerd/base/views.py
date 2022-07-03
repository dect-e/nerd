from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from verify_email.email_handler import send_verification_email

from .forms import UserCreationForm
from .models import *

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
    fields = ['name', 'number']
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

def export(request):
    event = get_object_or_404(Event, pk=request.GET.get('event'))
    extensions = {}
    for ext in Extension.objects.filter(event=event):
        extension = {
            'name': ext.name,
            'type': ext.extension_type,
            'dialout_allowed': ext.dialout_allowed,
            'trunk': ext.trunk
        }

        if ext.outgoing_extension != '':
            extension['outgoing_extension'] = ext.outgoing_extension

        if ext.extension_type == ExtensionType.CALLGROUP:
            extension['callgroup_members'] = [membership.extension.number for membership in CallgroupMembership.objects.filter(callgroup=ext, paused=False, accepted=True)]
        elif ext.extension_type == ExtensionType.DECT:
            if ext.dect_handset is not None:
                extension['dect_ipei'] = ext.dect_handset.ipei
            else:
                extension['dect_claim_token'] = ext.dect_claim_token
        elif ext.extension_type == ExtensionType.SIP:
            extension['sip_password'] = ext.sip_password
        elif ext.extension_type == ExtensionType.STATIC:
            extension['static_target'] = ext.static_target

        extensions[ext.number] = extension

    return JsonResponse({
        "extensions": extensions
    })
