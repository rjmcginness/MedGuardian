from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from .models import MedicationProductDetails
from .models import Medication
from .serializers import MedicationProductDetailsSerializer
from .serializers import MedicationSerializer


def index(request):
    name = request.GET.get('name') or ''

    return render(request, 'base.html', {'name': name})


def medication_search(request):
    search_words = request.GET.getlist('q')

    return render(request, 'medication-search.html', {'search_words': search_words})


class MedicationProductDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationProductDetailsSerializer
    queryset = MedicationProductDetails.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class MedicationViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationSerializer
    queryset = Medication.objects.all()
    permission_classes = [permissions.IsAuthenticated]
