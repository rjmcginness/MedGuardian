from django import forms
from .models import Prescriber
from .models import Prescription
from .models import PatientPrescribers
from .models import RouteOfAdministration
from .models import AdministrationFrequency
from src.user_model import Address
from src.user_model import ContactInformation
from src.utils import states_tuple
from medications.models import Medication




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
        exclude = ('patients', 'address', 'contact_information')

    def __init__(self, *args, **kwargs) -> None:
        super(PrescriberCreateForm, self).__init__(*args, **kwargs)
        self.__patient_id = None

    def set_patient_id(self, patient_id: int):
        self.__patient_id = patient_id

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

        patient_prescribers = PatientPrescribers.objects.create(patient_id=self.__patient_id,
                                                                prescriber_id=prescriber.id)

        patient_prescribers.save()

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

class PrescriptionCreateForm(forms.ModelForm):
    prescriber = forms.ChoiceField(choices=[])
    route_of_admin = forms.ChoiceField(choices=[])
    frequency = forms.ChoiceField(choices=[])
    medication = forms.ChoiceField(choices=[])
    class Meta:
        model = Prescription
        exclude = ('patient',
                   'medications',
                   'signature',
                   'date_written',
                   'is_active')

    def __init__(self, *args, **kwargs) -> None:

        # Have to pop the pk out, before passing kwargs to super().__init__
        patient_id = kwargs.pop('pk')
        super(PrescriptionCreateForm, self).__init__(*args, **kwargs)
        
        # NEEDED TO CREATE A MANY TO MANY FIELD ON PATIENTS. OTHERWISE THIS CAUSES TOO MANY DB HITS
        prescribers = Prescriber.objects.filter(patients__id=patient_id).order_by('last_name')

        route_of_admins = RouteOfAdministration.objects.all()
        frequencies = AdministrationFrequency.objects.all()
        medications = Medication.objects.all()
        self.fields['prescriber'].choices = ((prescriber.id,
                                              prescriber.last_name + ' in ' + \
                                              prescriber.address.city) for prescriber in prescribers)
        self.fields['route_of_admin'].choices = ((route.id,
                                                           route.name) for route in route_of_admins)
        self.fields['frequency'].choices = ((freq.id, freq.name) for freq in frequencies)
        self.fields['medication'].choices = ((medications.id, medication.generic_name +\
                                               ' (' + medication.brand_name + ')') for medication in medications)

    def save(self, commit=True) -> Prescription:
        data = self.cleaned_data

        prescriber_id = data['prescriber']
        route = RouteOfAdministration.objects.get(id=data['route_of_admin'])
        frequency = AdministrationFrequency.objects.get(id=data['frequency'])



