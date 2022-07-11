from django import forms

from .models import Medication


class MedicationCreateForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = '__all__'
