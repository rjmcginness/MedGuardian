from django import forms
from django.contrib.auth import models


class RegistrationForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'})
    )
    password = forms.CharField(widget=forms.PasswordInput())
    password_repeat = forms.CharField(label="Password (repeat)",
                                      widget=forms.PasswordInput())

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email']
