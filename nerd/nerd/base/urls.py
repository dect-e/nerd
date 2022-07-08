from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('extensions', views.ExtensionsView.as_view(), name='extensions'),
    path('extension/<int:pk>/', views.ExtensionEditView.as_view(), name='extension_edit'),
    path('phonebook', views.PhonebookView.as_view(), name='phonebook'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register, name='register'),
    path('verification/', include('verify_email.urls')),
]
