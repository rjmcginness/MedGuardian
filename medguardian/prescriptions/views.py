from django.shortcuts import render
from django.shortcuts import reverse
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import PrescriberSelectForm
from .forms import PrescriptionCreateForm
from .forms import PatientPrescriberForm
from .forms import PrescriberCreateForm

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
    success_url = '/accounts/<int:pk>/prescribers/success'

    # def get_form_kwargs(self):
    #     kwargs = super(PrescriberCreateView, self).get_form_kwargs()
    #     kwargs['pk'] = self.request.user.id
    #     return kwargs

    def form_valid(self, form):
        form.set_patient_id(self.request.user.id)
        form.save()
        context = {
            'pk': self.request.user.id,
            'prescriber_id': self.kwargs.get('prescriber_id')
        }
        return render(self.request, reverse('prescriber_add_success'), context)


class PrescriberSelectView(MedGuardianViewMixin):
    form_class = PrescriberSelectForm
    template_name = 'prescriber-search.html'
    success_url = '/accounts/<int:pk>/prescribers/success'

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

        patient_prescribers.save()

        context = {
            'pk': self.request.user.id,
            'prescriber_id': self.kwargs.get('prescriber_id')
        }
        return render(self.request, reverse('prescriber_add_success'), context)

class PrescriberView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Prescriber
    template_name = 'prescriber.html'
    

class PrescriberAddSuccessView(MedGuardianViewMixin):
    form_class = PatientPrescriberForm
    template_name = 'prescriber-added.html'

    # def form_valid(self, form):
    #     data = form.cleaned_data
    #     pp_association = PatientPrescribers(patient_id=data['patient_id'],
    #                                         prescriber_id=data['prescriber_id'])
    #
    #     pp_association.save()
    #     return render(self.request, self.template_name)


class PrescribersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Prescriber
    template_name = 'prescriber_list.html'
    paginate_by = 10

    def test_func(self) -> bool:
        return self.request.user.id == self.kwargs['pk']

    ######WORKING HERE: FINISH
    def get_queryset(self):
        print('>>>>>>>>>', Prescriber.objects.filter(patients__id=self.request.user.id).order_by('last_name').count())
        return Prescriber.objects.filter(patients__id=self.request.user.id).order_by('last_name')

    def get_context_object_name(self, object_list):
        return 'prescribers'




class PrescriptionCreateView(MedGuardianViewMixin):
    form_class = PrescriptionCreateForm
    template_name = 'prescription-create.html'
    success_url = '/medications'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PrescriptionCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['pk'] = self.request.user.id
        return kwargs

    def get(self, request, *arg, **kwargs):
        context = super(PrescriptionCreateView, self).get_context_data(**kwargs)

        context.update({'pk': request.user.id})

        return self.render_to_response(context)

    def form_valid(self, form):
        form.set_patient_id(self.request.user.id)
        form.save()

        return super().form_valid(form)


