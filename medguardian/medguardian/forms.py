from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from datetime import datetime

from src.user_model import Patient
from src.user_model import Address
from src.user_model import ContactInformation


def valid_number_given(home, mobile, fax) -> bool:
    no_home = not home or home == ''
    no_mobile = not mobile or mobile == ''
    no_fax = not fax or fax == ''

    return not(no_home and no_mobile and no_fax)


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
        cleaned_data = super().clean()
        if not valid_number_given(cleaned_data.get('home_number', None),
                                  cleaned_data.get('mobile_number', None),
                                  cleaned_data.get('fax_number', None)):
            raise ValidationError('At least one contact number is required')

    def save(self, commit=True) -> Patient:
        data = self.cleaned_data
        address = Address(street=data['street'],
                          street2=data['street2'],
                          city=data['city'],
                          county=data['county'],
                          state_name=data['state'],
                          zip_code=data['zip_code']
                         )

        # one of phone, mobile, or fax will have a value (form validation)
        contact = ContactInformation(home_phone=data.get('home_number', None),
                                     mobile_phone=data.get('mobile_number', None),
                                     fax_number=data.get('fax_number', None),
                                     preferred_type=data['preferred_contact']
                                    )

        address.save()
        contact.save()

        patient = Patient(username=data['username'],
                          first_name=data['first_name'],
                          last_name=data['last_name'],
                          email=data['email'],
                          is_staff=False,
                          is_superuser=False,
                          is_active=True,
                          date_joined=datetime.now(),
                          birth_date=data['date_of_birth'],
                          address=address,
                          contact_information=contact
                          )

        # patient.save()

        # call User.set_password to set the password (preforms hashing)
        patient.set_password(data['password1'])
        patient.save()

        return patient
