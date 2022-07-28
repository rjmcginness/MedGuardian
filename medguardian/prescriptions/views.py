from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.http import HttpResponse
from django.http import FileResponse
from http import HTTPStatus
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import permissions
from reportlab.pdfgen import canvas
from typing import List
import json

from .forms import PrescriberSelectForm
from .forms import PrescriptionCreateForm
from .forms import PatientPrescriberForm
from .forms import PrescriberCreateForm
from .forms import PrescriptionEditForm

from .models import Prescriber
from .models import PatientPrescribers
from .models import Prescription
from .models import PrescriptionAdminTime
from .models import AdministrationTime
from .models import ContactTimes
from .serializers import PrescriberSerializer
from .serializers import PrescriptionSerializer
from src.user_model import Patient


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
            'prescriber_id': self.kwargs['prescriber_id']
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


class PrescribersListView(LoginRequiredMixin, UserPassesTestMixin, generics.ListAPIView):
    serializer_class = PrescriberSerializer
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [permissions.IsAuthenticated,]

    def test_func(self) -> bool:
        return self.request.user.id == self.kwargs['pk']

    def list(self, request, *args, **kwargs):
        prescribers = Prescriber.objects.filter(patients__id=request.user.id)
        serializer = self.serializer_class(prescribers, many=True)
        return Response({'prescribers': serializer.data},
                        template_name='prescriber_list.html')

    # model = Prescriber
    # template_name = 'prescriber_list.html'
    # paginate_by = 10



    # ######WORKING HERE: FINISH
    # def get_queryset(self):
    #     print('>>>>>>>>>', Prescriber.objects.filter(patients__id=self.request.user.id).order_by('last_name').count())
    #     return Prescriber.objects.filter(patients__id=self.request.user.id).order_by('last_name')
    #
    # def get_context_object_name(self, object_list):
    #     return 'prescribers'





class PrescriptionCreateView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = PrescriptionCreateForm
    template_name = 'prescription-create.html'
    success_url = '/medications'

    def test_func(self) -> bool:
        return self.request.user.id == self.kwargs['pk']

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PrescriptionCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['pk'] = self.request.user.id
        return kwargs

    # def get(self, request, *arg, **kwargs):
    #     context = super(PrescriptionCreateView, self).get_context_data(**kwargs)
    #
    #     context.update({'pk': request.user.id})
    #
    #     return self.render_to_response(context)

    def form_valid(self, form):
        # form.set_patient_id(self.request.user.id)
        if self.request.method == 'POST':
            form.save()

        context = {
                    'pk': self.request.user.id
                  }

        ####### MAY WANT TO CHANGE THIS
        return redirect(to=reverse('medications', kwargs=context))


class ActiveMedProfileViewSet(LoginRequiredMixin, UserPassesTestMixin, generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [permissions.IsAuthenticated,]

    def test_func(self) -> bool:
        return self.request.user.id == self.kwargs['pk']

    def list(self, request, *args, **kwargs):
        rx_list = Prescription.objects.filter(
                    patient_id=request.user.id, is_active=True)
        # queryset = [rx.medication_set for rx in rx_list]
        serializer = self.serializer_class(rx_list, many=True)
        return Response({'prescriptions': serializer.data},
                        template_name='active-medications.html')


class PrescriptionRDView(LoginRequiredMixin, UserPassesTestMixin, generics.RetrieveDestroyAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def test_func(self) -> bool:
        return self.request.user.id == self.kwargs['pk']

    def get_object(self, pk):
        try:
            return Prescription.objects.get(id=pk)
        except Prescription.DoesNotExist:
            raise Http404()

    def get(self, request, *args, **kwargs):
        prescription = self.get_object(kwargs.get('rx_id', None))

        serializer = self.get_serializer(prescription)

        return Response({'prescription': serializer.data},
                        template_name='prescription.html')

    def delete(self, request, *args, **kwargs):
        prescription = self.get_object(kwargs.get('rx_id', None))

        prescription.delete()

        context = {
            'pk': request.user.id
        }

        return redirect(to=reverse('prescriptions', kwargs=context))


class AdministrationTimeListView(LoginRequiredMixin, UserPassesTestMixin, generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    renderer_classes = [TemplateHTMLRenderer,]
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        return get_object_or_404(klass=Prescription, id=self.kwargs.get('rx_id'))

    def list(self, request, *args, **kwargs):
        prescription = self.get_queryset()
        serializer = self.get_serializer(prescription)

        return Response({'prescription': serializer.data},
                        template_name='administration-times.html')

    def test_func(self)-> bool:
        return self.request.user.id == self.kwargs['pk']


class PrescriptionUpdateAPIView(LoginRequiredMixin, UserPassesTestMixin, generics.mixins.UpdateModelMixin, FormView):
    permission_classes = [permissions.IsAuthenticated,]
    form_class = PrescriptionEditForm
    template_name = 'administration-times-edit.html'

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        context.update({'rx_id': kwargs.get('rx_id')})

        return render(request, template_name=self.template_name, context=context)

    def test_func(self)-> bool:
        return self.request.user.id == self.kwargs['pk']

    def form_valid(self, form):
        raise Http404()

    def get_object(self):
        return Prescription.objects.get(id=self.kwargs.get('rx_id'))

    def get_serializer(self):
        return None

    def patch(self, request, *args, **kwargs):
        '''
            In essence a patch on prescription, wherein the administration
            times are changed (created, modified, deleted).  However, the
            action is on the association table PrescriptionAdminTimes.

            This also maintains the proper accosicatuons between the contact
            and administration times through the prescriptions_contacttimes
            table.  Because multiple prescriptions could have particular
            administration times, there is an incrementor field, called
            instances.  When first created this is set to 1.  When decremented
            to zero, the association is deleted.
        '''

        admin_times = json.loads(self.request.body).get('administration_times', None)

        # if there are admin times sent, make sure they are different,
        # then delete old associations and create new ones
        if admin_times:
            # get a list of current administration time ids (if any)
            current_admin_time_ids = self.get_object().administration_times.values_list('id')
            current_admin_time_ids = [time_tup[0] for time_tup in current_admin_time_ids]

            # get ids for new administration times
            admin_time_ids = AdministrationTime.objects.filter(value__in=admin_times).values_list('id')
            admin_time_ids = [time_tup[0] for time_tup in admin_time_ids]

            # only do something if new and old admin times are not the same
            if sorted(current_admin_time_ids) != sorted(admin_time_ids):

                # delete associations with old ids
                PrescriptionAdminTime.objects.filter(administration_time_id__in=current_admin_time_ids,
                                                     prescription_id=kwargs.get('rx_id')).delete()

                # create list on new association models objects
                new_rx_time_associations = [PrescriptionAdminTime(prescription_id=self.kwargs.get('rx_id'),
                                                                  administration_time_id=time_id) for \
                                                                  time_id in admin_time_ids]

                # create (in bulk) new associations
                PrescriptionAdminTime.objects.bulk_create(new_rx_time_associations)

                # get contact info id for patient
                self.resolve_contact_times(request.user.id, current_admin_time_ids, admin_time_ids)

        return HttpResponse(status=HTTPStatus.ACCEPTED)

    def resolve_contact_times(self, patient_id: int, old_time_ids: List[int], new_time_ids: List[int]):
        '''
            Remove contact times that are no longer associated with this patient.
            Make new associations, as appropriate for the new contact times
        '''
        contact_id = Patient.objects.get(id=patient_id).contact_information.id

        # get all the old contact times associated with the patient,
        # but exclude the new times
        contact_times = ContactTimes.objects.filter(contact_id=contact_id,
                                                    id__in=old_time_ids).exclude(id__in=new_time_ids)

        # decrement instances column for each removed contact time
        # if zero, add id to list to delete
        # ids_to_delete = []
        for time in contact_times:
            time.instances -= 1
            # if time.instances == 0:
            #     ids_to_delete.append(time.pk)

        # delete contact times with zero instances
        contact_times.filter(instances=0).delete()

        # update decremented contact times
        ContactTimes.objects.bulk_update(contact_times, ['instances',])

        # make new contact times if not already existing
        new_contact_times = [ContactTimes(contact_id=contact_id, administration_time_id=time_id) for \
                             time_id in new_time_ids if time_id not in old_time_ids]

        # store new association in database
        ContactTimes.objects.bulk_create(new_contact_times)


class TodaysMedicationsListView(LoginRequiredMixin, UserPassesTestMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    renderer_classes = [TemplateHTMLRenderer,]
    serializer_class = PrescriptionSerializer

    def test_func(self)-> bool:
        return self.request.user.id == self.kwargs['pk']

    def get_queryset(self):
        return Prescription.objects.filter(patient_id=self.request.user.id, is_active=True)

    def list(self, request, *args, **kwargs):
        prescriptions = self.get_queryset()
        serializer = self.serializer_class(prescriptions, many=True)

        return Response({'prescriptions': serializer.data},
                        template_name='prescriptions-today.html')

def verify_user(request):
    return request.user.id == request.session.get('pk')

@login_required()
@user_passes_test(test_func=verify_user)
def download_todays_meds(request) -> HttpResponse:


    return HttpResponse("Hello", content_type='application/pdf,text/plain')