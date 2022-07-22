from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import routers
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import permissions

from .models import MedicationProductDetails
from .models import Medication
from .serializers import MedicationProductDetailsSerializer
from .serializers import MedicationSerializer
from .forms import MedicationCreateForm
from prescriptions.models import Prescription


def index(request):
    name = request.GET.get('name') or ''

    return render(request, 'base.html', {'name': name})


def medication_search(request):
    search_words = request.GET.getlist('q')

    return render(request, 'medication-search.html', {'search_words': search_words})


def medication_create(request):
    form = MedicationCreateForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=True)
            return redirect('/medications')
    return render(request, 'medication-create.html', {'form': form})


# class MedicationRouter(routers.SimpleRouter):
#     '''
#         Router for medication-related views and actions
#     '''
#     routes = [routers.Route(url=r'^/accounts/{lookup}/{prefix}$',
#                            mapping={'get': 'list'},
#                            name='{basename}-list',
#                            detail=False,
#                            initkwargs={'suffix':'List'}),]

class ActiveMedProfileViewSet(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = MedicationSerializer
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [permissions.IsAuthenticated,]

    def list(self, request, *args, **kwargs):
        rx_list = Prescription.objects.filter(
                    patient_id=request.user.id, is_active=True)
        # queryset = [rx.medication_set for rx in rx_list]
        serializer = self.serializer_class(rx_list, many=True)
        return Response({'prescriptions': serializer.data},
                        template_name='active-medications.html')

# class ActiveMedProfileViewSet(LoginRequiredMixin, viewsets.ViewSet):
#     serializer_class = MedicationSerializer
#     # queryset = Medication
#     renderer_classes = [TemplateHTMLRenderer]
#     permission_classes = [permissions.IsAuthenticated,]
#
#     def list(self, request, *args, **kwargs):
#         rx_list = Prescription.objects.filter(
#                     patient_id=request.user.id, is_active=True)
#         queryset = [rx.medication_set for rx in rx_list]
#         serializer = self.serializer_class(queryset, many=True)
#         return Response({'medications': serializer.data},
#                         template_name='active-medications.html')

class MedicationProductDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationProductDetailsSerializer
    queryset = MedicationProductDetails.objects.all()
    # permission_classes = [permissions.IsAuthenticated]


class MedicationViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationSerializer
    queryset = Medication.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
