from django.views.generic.edit import FormView
from django.http import HttpRequest
from django.views import View
from django.shortcuts import render
from .forms import RegistrationForm

class RegistrationView(FormView):

    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = '/account_created'

    def form_valid(self, form) -> HttpRequest:

        form.save()
        return super().form_valid(form)

class RegistrationSuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/registration-success.html')