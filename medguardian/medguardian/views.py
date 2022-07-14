from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.http import HttpRequest
from django.views import View
from rest_framework import viewsets
from django.shortcuts import render
from .forms import RegistrationForm
from .serializers import PatientSerializer
from src.user_model import Patient


class ProfileViewSet(viewsets.ViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

class FrontPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'medguardian.html')


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

class LogoutView(TemplateView):
    template_name = 'registration/logged_out.html'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logout(request)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
