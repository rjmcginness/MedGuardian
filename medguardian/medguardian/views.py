from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.contrib.auth import views
from django.http import HttpRequest
from django.http import HttpResponseForbidden
from django.views import View
from django.shortcuts import render
from django.shortcuts import resolve_url
from .forms import RegistrationForm
# from .serializers import PatientSerializer
from src.user_model import Patient


class ProfileView(DetailView):
    model = Patient
    template_name = 'account-profile.html'

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated or \
                kwargs.get('pk', None) is None or \
                request.user.pk != kwargs['pk']:
            return HttpResponseForbidden('Unauthorized access attempted')

        return super().dispatch(request, *args, **kwargs)

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


class LoginViewWrap(views.LoginView):
    ''' Highjacking LoginView to keep functionality, but to
        properly redirect patient (user) to non-admin
        functionality.  Thank you, Django!
    '''

    def get_success_url(self):
        ''' Overriding this to prevent redirect to admin site
            or, in other words, redirect to medguardian profile
            page.  This allows redirection based on pk.
        '''

        # set the session to expire in 5 minutes (= 60 * 5)
        self.request.session.set_expiry(300)

        return resolve_url('accounts/' + str(self.request.user.pk) + '/profile/')

class LogoutView(TemplateView):
    template_name = 'registration/logged_out.html'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logout(request)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
