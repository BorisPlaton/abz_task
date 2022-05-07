from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView

from accounts.models import User


class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form': UserCreationForm,
        }
        
        return render(request, self.template_name, context=context)
