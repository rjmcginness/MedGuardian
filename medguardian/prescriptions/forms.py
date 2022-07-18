from django import forms
from .models import Prescription
# from django.contrib.auth.mixins import LoginRequiredMixin

class PrescriptionCreateForm(forms.ModelForm):

    # prescriber_name = forms.ChoiceField

    class Meta:
        model = Prescription
        exclude = ('id', 'patient_id', 'prescriber_id', 'is_active')

    # def save(self, commit=True):