from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetConfirmView, 
    PasswordResetDoneView)
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from hrm.users import forms

User = get_user_model()

class SignUp(generic.CreateView):
    form_class = forms.UserCreationForm
    success_url = reverse_lazy('users:signin')
    template_name = 'registration/signup.html'