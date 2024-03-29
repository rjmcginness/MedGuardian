import rest_framework.serializers
from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from django.views.generic import DetailView
from django.views.generic import TemplateView
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
from reportlab.lib.pagesizes import letter
from typing import List
from datetime import datetime
from datetime import time as tm
import json
import io


from .forms import PrescriberSelectForm
from .forms import PrescriptionCreateForm
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


class MedGuardianSecureViewMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user.id == self.kwargs['pk']



class PrescriberCreateView(MedGuardianSecureViewMixin, FormView):
    form_class = PrescriberCreateForm
    template_name = 'prescriber-create.html'
    success_url = '/accounts/<int:pk>/prescribers/success'

    # def get_form_kwargs(self):
    #     kwargs = super(PrescriberCreateView, self).get_form_kwargs()
    #     kwargs['pk'] = self.request.user.id
    #     return kwargs

    def form_valid(self, form):
        form.set_patient_id(self.request.user.id)
        prescriber = form.save()
        kwargs = {
            'pk': self.request.user.id,
            'prescriber_id': prescriber.id
        }

        context = {
            'prescriber': prescriber
        }


        return render(self.request, template_name='prescriber-added.html', context=context)


class PrescriberSelectView(MedGuardianSecureViewMixin, FormView):
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
        data = form.cleaned_data
        patient_id = data.get('pk')
        prescriber_id = data.get('prescriber_id')
        if not PatientPrescribers.objects.filter(patient_id=patient_id, prescriber_id=prescriber_id).exists():
            patient_prescribers = PatientPrescribers.objects.create(patient_id=patient_id, prescriber_id=prescriber_id)

        kwargs = {
            'pk': self.request.user.id,
        }
        return render(self.request, reverse('prescribers', kwargs=kwargs))

class PrescriberChosenView(MedGuardianSecureViewMixin, TemplateView):
    template_name = 'prescriber.html'

    def dispatch(self, request, *args, **kwargs):
        patient_id = kwargs.get('pk')
        prescriber_id = kwargs.get('prescriber_id')

        if not PatientPrescribers.objects.filter(patient_id=patient_id, prescriber_id=prescriber_id).exists():
            PatientPrescribers.objects.create(patient_id=patient_id, prescriber_id=prescriber_id)
        
        context = {
            'prescriber': Prescriber.objects.get(id=prescriber_id)
        }

        return render(self.request, template_name='prescriber-added.html', context=context)


class PrescribersListView(MedGuardianSecureViewMixin, generics.ListAPIView):
    serializer_class = PrescriberSerializer
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [permissions.IsAuthenticated,]

    def list(self, request, *args, **kwargs):
        prescribers = Prescriber.objects.filter(patients__id=request.user.id)
        serializer = self.serializer_class(prescribers, many=True)
        print(serializer.data)
        return Response({'prescribers': serializer.data},
                        template_name='prescriber_list.html')


class PrescriberRDAPIView(MedGuardianSecureViewMixin, generics.RetrieveDestroyAPIView):

    def get(self, request, *args, **kwargs):
        prescriber = get_object_or_404(Prescriber, id=kwargs.get('prescriber_id'))

        context = {
                    'prescriber': prescriber
                  }

        return render(request, template_name='prescriber.html', context=context)


class PrescriberDeleteAPIView(MedGuardianSecureViewMixin, generics.DestroyAPIView):
    renderer_classes = [TemplateHTMLRenderer,]
    permission_classes = [permissions.IsAuthenticated,]

    def delete(self, request, *args, **kwargs):
        patient_prescriber = get_object_or_404(PatientPrescribers,
                                               patient_id=request.user.id,
                                               prescriber_id=kwargs.get('prescriber_id'))

        patient_prescriber.delete()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)


class PrescriptionCreateView(MedGuardianSecureViewMixin, FormView):
    form_class = PrescriptionCreateForm
    template_name = 'prescription-create.html'
    success_url = '/medications'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PrescriptionCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['pk'] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        # form.set_patient_id(self.request.user.id)
        if self.request.method == 'POST':
            form.save()

        context = {
                    'pk': self.request.user.id
                  }

        ####### MAY WANT TO CHANGE THIS
        return redirect(to=reverse('medications', kwargs=context))


class ActiveMedProfileViewSet(MedGuardianSecureViewMixin, generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [permissions.IsAuthenticated,]

    def list(self, request, *args, **kwargs):
        rx_list = Prescription.objects.filter(
                    patient_id=request.user.id, is_active=True)
        # queryset = [rx.medication_set for rx in rx_list]
        serializer = self.serializer_class(rx_list, many=True)
        return Response({'prescriptions': serializer.data},
                        template_name='active-medications.html')


class PrescriptionRDView(MedGuardianSecureViewMixin, generics.RetrieveDestroyAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

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


class AdministrationTimeListView(MedGuardianSecureViewMixin, generics.ListAPIView):
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


class PrescriptionUpdateAPIView(MedGuardianSecureViewMixin, generics.mixins.UpdateModelMixin, FormView):
    permission_classes = [permissions.IsAuthenticated,]
    form_class = PrescriptionEditForm
    template_name = 'administration-times-edit.html'

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        context.update({'rx_id': kwargs.get('rx_id')})

        return render(request, template_name=self.template_name, context=context)

    def form_valid(self, form):
        '''Prevent Post'''
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


class TodaysMedicationsListView(MedGuardianSecureViewMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    renderer_classes = [TemplateHTMLRenderer,]
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        return Prescription.objects.filter(patient_id=self.request.user.id, is_active=True)

    def list(self, request, *args, **kwargs):
        prescriptions = self.get_queryset()
        serializer = self.serializer_class(prescriptions, many=True)

        return Response({'prescriptions': serializer.data},
                        template_name='prescriptions-today.html')

def verify_user(request):
    return request.is_authenticated

def check_new_page(offset) -> bool:
    return offset <= 0

def rx_data_to_output_str(rx_list: rest_framework.serializers.ReturnList,
                          c: canvas.Canvas,
                          offset: int,
                          font_height: int) -> None:
    width, height = letter
    page_width = width - 30

    for rx in rx_list:
        if check_new_page(offset):
            c.showPage()
            offset = height - 20

        c.setFont('Courier-Bold', font_height)
        c.drawString(14, offset, 'RX')
        c.setFont('Times-Roman', font_height)
        offset -= font_height + 2
        meds = rx.get('medications')
        med_strings = (med.get('generic_name') + ' (' + med.get('brand_name') + ') ' + med.get('strength_text') +\
                       ' ' + med.get('dosage_form') for med in meds)
        for med_str in med_strings:
            if check_new_page(offset):
                c.showPage()
                offset = height - 20

            cuts = (30 + c.stringWidth(med_str))//page_width
            if cuts > 1:
                cuts = int(cuts) + 1
                shift = len(med_str)//cuts
                for _ in range(cuts):
                    c.drawString(16, offset, med_str[:shift])
                    med_str = med_str[shift:]
                    offset -= font_height + 1
            else:
                c.drawString(16, offset, med_str)
                offset -= font_height + 1

        offset -= 1
        if check_new_page(offset):
            c.showPage()
            offset = height - 20

        routes = rx.get('routes')
        for route in routes:
            c.drawString(16, offset, route.get('name'))
            offset -= font_height + 1
            if check_new_page(offset):
                c.showPage()
                offset = height - 20

        offset -= 1
        if check_new_page(offset):
            c.showPage()
            offset = height - 20

        if instructions := rx.get('instructions'):
            c.drawString(16, offset, instructions)
            offset -= font_height + 1

        if check_new_page(offset):
            c.showPage()
            offset = height - 20

        c.drawString(16, offset, "Take at: ")
        admin_times = (tm.fromisoformat(admin_time.get('value')).strftime('%I:%M %p') \
                       for admin_time in rx.get('administration_times'))

        time_str = ', '.join(admin_times)
        c.drawString(16 + c.stringWidth('Take at: '), offset, time_str)
        offset -= font_height + 1

        if check_new_page(offset):
            c.showPage()
            offset = height - 20

        if rx.get('is_prn'):
            c.drawString(16, offset, 'Take as needed for ' + rx.get('prn_reason'))
            offset -= font_height + 1

        if check_new_page(offset):
            c.showPage()
            offset = height - 20
            
        prescriber = rx.get('prescriber')

        first_name = prescriber.get('last_name')
        last_name = prescriber.get('first_name')
        creds = prescriber.get('credentials')
        phone = prescriber.get('contact_information').get('home_phone')
        prescriber_str = 'Prescriber: ' + first_name + ', ' + last_name
        prescriber_str += ', ' + creds if creds else ''
        prescriber_str += ' phone: '
        prescriber_str += phone if phone else ''

        c.drawString(16, offset,  prescriber_str)

        offset -= font_height + 2

def generate_prescriptions_pdf(patient: Patient, active_only: bool=True):

    current_dt = datetime.now()
    buffer = io.BytesIO()
    title = patient.last_name + ', ' + patient.first_name + ' generated ' + current_dt.ctime()

    width, height = letter
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setTitle(title)
    c.setFont('Times-Roman', 18)
    offset = height - 20
    c.drawString(10, offset, "Medications to Take Today")
    offset -= 2
    c.setLineWidth(0.5)
    c.line(10, offset, width - 10, offset)

    font_height = 14
    c.setFont('Times-Roman', font_height)
    offset -= font_height + 1

    c.drawString(10, offset, title)
    offset -= font_height + 3
    font_height = 12

    prescriptions = None
    if active_only:
        prescriptions = Prescription.objects.filter(patient_id=patient.id, is_active=True)
    else:
        prescriptions = Prescription.objects.filter(patient_id=patient.id)

    # convert to list to avoid inadvertent db hits (get it all now)
    rx_list = PrescriptionSerializer(prescriptions, many=True).data

    rx_data_to_output_str(rx_list, c, offset, font_height)

    c.showPage()
    c.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=patient.last_name + "_" +\
                                                             patient.first_name + \
                                                             current_dt.date().strftime('%b_%d_%y') + '.pdf')

@login_required()
@user_passes_test(test_func=verify_user)
def download_todays_meds(request, pk) -> HttpResponse:

    return generate_prescriptions_pdf(Patient.objects.get(pk=request.user.id))
