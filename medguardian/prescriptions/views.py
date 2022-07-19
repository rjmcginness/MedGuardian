from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import PrescriberCreateForm
from .forms import PrescriberSelectForm
from .forms import PrescriptionCreateForm

from .models import Prescriber


class MedGuardianViewMixin(LoginRequiredMixin, UserPassesTestMixin, FormView):
    def test_func(self) -> bool:
        return self.request.user.id == self.kwargs['pk']

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PrescriberCreateView(MedGuardianViewMixin):
    form_class = PrescriberCreateForm
    template_name = 'prescriber-create.html'
    success_url = '/prescribers'


class PrescriberSelectView(MedGuardianViewMixin):
    form_class = PrescriberSelectForm
    template_name = 'prescriber-search.html'
    success_url = '/add_prescriber'

    def get(self, request, *args, **kwargs):
        querydict = dict(request.GET)
        if querydict.get('prescriber_name', '') != '':
            prescribers = Prescriber.objects.filter(
                                    address__state_name=querydict['state']).filter(
                                    address__city=querydict['city']).filter(
                                    last_name=querydict['prescriber_name'])

            kwargs['prescribers'] = prescribers if prescribers else []

        return super().get(request, *args, **kwargs)



class PrescriptionCreateView(MedGuardianViewMixin):
    form_class = PrescriptionCreateForm
    template_name = 'prescriptions/prescription-create.html'
    success_url = '/medications'
