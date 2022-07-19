from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import PrescriberCreateForm
from .forms import PrescriberSelectForm
from .forms import PrescriptionCreateForm

from .models import Prescriber
from .models import PatientPrescribers


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
    success_url = 'prescriber_add_success'

    def get(self, request, *args, **kwargs):
        querydict = request.GET.dict()
        if querydict.get('prescriber_name', '') != '':
            state = querydict['state']
            city = querydict['city']
            last_name = querydict['prescriber_name']
            prescribers = Prescriber.objects.filter(
                                    address__state_name=state,
                                    address__city=city,
                                    last_name=last_name)

            context = {'prescribers': list(prescribers)}
            return render(request,
                          self.template_name,
                          context)

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        patient_prescribers = PatientPrescribers.objects.create(patient_id=self.kwargs.get('pk'),
                                                                prescriber_id=self.kwargs.get('prescriber_id'))

        print('>>>>>>>>>', patient_prescribers.id)
        return render(request, reverse('prescriber_add_success'))

class PrescriberAddSuccessView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'prescriber-added.html'


class PrescriptionCreateView(MedGuardianViewMixin):
    form_class = PrescriptionCreateForm
    template_name = 'prescriptions/prescription-create.html'
    success_url = '/medications'
