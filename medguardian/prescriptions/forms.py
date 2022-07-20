from django import forms
from .models import Prescriber
from .models import Prescription
from .models import PatientPrescribers
from src.user_model import Address
from src.user_model import ContactInformation
from src.utils import states_tuple




class PrescriberCreateForm(forms.ModelForm):
    street = forms.CharField(max_length=256)
    street2 = forms.CharField(max_length=256, required=False)
    city = forms.CharField(max_length=80)
    state = forms.CharField(max_length=80)
    county = forms.CharField(max_length=80, required=False)
    zip_code = forms.CharField(max_length=10)

    home_number = forms.CharField(max_length=15, label='Office Phone Number')
    mobile_number = forms.CharField(max_length=15, required=False)
    fax_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = Prescriber
        exclude = ('address', 'contact_information')

    def save(self, commit=True) -> Prescriber:
        data = self.cleaned_data

        address = Address(street=data['street'],
                          street2=data['street2'],
                          city=data['city'],
                          county=data['county'],
                          state_name=data['state'],
                          zip_code=data['zip_code']
                         )

        # home (office) phone number is required
        contact = ContactInformation(home_phone=data['home_number'],
                                     mobile_phone=data.get('mobile_number', None),
                                     fax_number=data.get('fax_number', None),
                                     preferred_type='office'
                                    )

        address.save()
        contact.save()

        prescriber = Prescriber(first_name=data['first_name'],
                                last_name=data['last_name'],
                                federal_dea=data['federal_dea'],
                                state_dea=data['state_dea'],
                                address=address,
                                contact_information=contact
                               )

        prescriber.save()

        return prescriber

class PrescriberSelectForm(forms.Form):
    prescriber_name = forms.CharField(max_length=80,
                                      help_text="Your doctor's last name"
                                     )
    city = forms.CharField(max_length=80,
                           help_text="Where is your doctor's office?"
                          )
    state = forms.ChoiceField(choices=states_tuple(),
                              help_text="State where your doctor practices")

class PrescriptionCreateForm(forms.ModelForm):

    # prescriber_name = forms.ChoiceField

    class Meta:
        model = Prescription
        exclude = ('id', 'patient_id', 'prescriber_id', 'is_active')

    # def save(self, commit=True):


class PatientPrescriberForm(forms.Form):
    patient_id = forms.IntegerField(widget=forms.HiddenInput())
    prescriber_id = forms.IntegerField(widget=forms.HiddenInput())

