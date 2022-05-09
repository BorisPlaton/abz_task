from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect

from accounts.forms import CustomUserCreationForm
from accounts.utils import NonAuthenticatedView


class RegisterView(NonAuthenticatedView):
    template_name = 'registration/register.html'

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(self.redirect_to)

        return redirect('accounts:register')

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['form'] = CustomUserCreationForm()
        return context


class LoginView(NonAuthenticatedView):
    template_name = 'registration/login.html'

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(self.redirect_to)
        return redirect('employees:login')

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = AuthenticationForm()
        return context
