from django import forms
from django.contrib.auth import models


class RegistrationForm(forms.ModelForm):

    date_of_birth = forms.DateField(widget=forms.DateInput(
                                        attrs={'type': 'date'})
                                   )
    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email']
