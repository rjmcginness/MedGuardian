from django.views.generic.edit import FormView
from .forms import RegistrationForm

class RegistrationView(FormView):

    template_name = 'registration/register.html'
    form_class = RegistrationForm
