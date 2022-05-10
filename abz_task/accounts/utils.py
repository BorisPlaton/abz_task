from django.shortcuts import redirect
from django.views.generic import TemplateView


class NonAuthenticatedView(TemplateView):
    redirect_to = 'employees:home'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_to)
        return super(NonAuthenticatedView, self).dispatch(request, *args, **kwargs)
