from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from src.user_model import Patient
from src.user_model import Address
from src.user_model import ContactInformation


def valid_number_given(home, mobile, fax) -> bool:
    no_home = not home or home == ''
    no_mobile = not mobile or mobile == ''
    no_fax = not fax or fax == ''

    return no_home and no_mobile and no_fax


class RegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'})
    )
    # password = forms.CharField(widget=forms.PasswordInput())
    # password_repeat = forms.CharField(label="Password (repeat)",
    #                                   widget=forms.PasswordInput())

    street = forms.CharField(max_length=256)
    street2 = forms.CharField(max_length=256, required=False)
    city = forms.CharField(max_length=80)
    state = forms.CharField(max_length=80)
    county = forms.CharField(max_length=80, required=False)
    zip_code = forms.CharField(max_length=10)

    preferred_contact = forms.ChoiceField(label='Preferred Contact Type',
                                          choices=[(-1, 'Choose Type'),
                                                   (1, 'Home Phone'),
                                                   (2, 'Mobile Phone'),
                                                   (3, 'Email'),
                                                   (4, 'Text Message'),
                                                   (5, 'Fax')],
                                          required=False)

    home_number = forms.CharField(max_length=15, required=False)
    mobile_number = forms.CharField(max_length=15, required=False)
    fax_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = Patient
        fields = ['username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2']

    def clean(self):
        super().clean()
        if not valid_number_given(self.home_number,
                                  self.mobile_number,
                                  self.fax_number):
            raise ValidationError('One contact number required')

    def save(self, commit=True) -> Patient:
        user = super().save(commit)

        address = Address()
        address.street = self.street
        address.street2 = self.street2
        address.city = self.city
        address.state_name = self.state
        address.county = self.county
        address.zip_code = self.zip_code

        contact = ContactInformation()
        contact.preferred_type = self.preferred_contact
        contact.home_phone = self.home_number
        contact.mobile_phone = self.mobile_number
        contact.fax_number = self.fax_number

        address.save()
        contact.save()

        patient = Patient()
        patient.pk = user.pk
        patient.birth_date = self.date_of_birth
        patient.address = address
        patient.contact_information = contact

        patient.save()

        return patient
