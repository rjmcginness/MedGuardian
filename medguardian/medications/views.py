from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework import permissions

from .models import MedicationProductDetails
from .models import Medication
from .serializers import MedicationProductDetailsSerializer
from .serializers import MedicationSerializer
from .forms import MedicationCreateForm


def index(request):
    name = request.GET.get('name') or ''

    return render(request, '../medguardian/templates/base.html', {'name': name})


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


class MedicationProductDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationProductDetailsSerializer
    queryset = MedicationProductDetails.objects.all()
    # permission_classes = [permissions.IsAuthenticated]


class MedicationViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationSerializer
    queryset = Medication.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
