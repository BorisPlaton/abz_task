from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import CustomUserCreationForm


class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form': CustomUserCreationForm(),
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('employees:home')

        return redirect('accounts:login')
