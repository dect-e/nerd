from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True, template_name='base/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
