from django import forms
from .models import Prescriber
from .models import Prescription
from .models import PatientPrescribers
from .models import RouteOfAdministration
from .models import AdministrationFrequency
from .models import PrescriptionMedication
from .models import PrescriptionRoute
from .models import PrescriptionFrequency
from src.user_model import Address
from src.user_model import ContactInformation
from src.user_model import Patient
from src.utils import states_tuple
from medications.models import Medication
from prescriptions.models import AdministrationTime


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
                                credentials=data['credentials'],
                                specialty=data['specialty'],
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


class PatientPrescriberForm(forms.Form):
    patient_id = forms.IntegerField(widget=forms.HiddenInput())
    prescriber_id = forms.IntegerField(widget=forms.HiddenInput())

class PrescriptionCreateForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ('prescriber',
                  'medications',
                  'routes',
                  'frequencies',
                  'instructions',
                  'is_prn',
                  'prn_reason',
                  'quantity_per_dose',
                  'dose_units',
                 )

    def __init__(self, *args, **kwargs) -> None:

        # Have to pop the pk out, before passing kwargs to super().__init__
        self.__patient_id = kwargs.pop('pk')
        super(PrescriptionCreateForm, self).__init__(*args, **kwargs)
        
        # NEEDED TO CREATE A MANY-TO-MANY FIELD ON PATIENTS. OTHERWISE ,THIS CAUSES TOO MANY DB HITS
        prescribers = Prescriber.objects.filter(patients__id=self.__patient_id).order_by('last_name')

        route_of_admins = RouteOfAdministration.objects.all()
        frequencies = AdministrationFrequency.objects.all()
        medications = Medication.objects.all().distinct('generic_name',
                                                        'strength_text',
                                                        'dosage_form').order_by('generic_name')
        self.fields['prescriber'].choices = ((prescriber.id, prescriber) for prescriber in prescribers)
        self.fields['routes'].choices = ((route.id, route) for route in route_of_admins)
        self.fields['frequencies'].choices = ((freq.id, freq) for freq in frequencies)
        self.fields['medications'].choices = ((medication.id, medication) for medication in medications)

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data.get('is_prn', None) and cleaned_data.get('prn_reason', None):  # is_prn missing
            self.add_error('is_prn', "Did you mean to check the is prn button? If not, please delete the prn reason.")
        elif cleaned_data.get('is_prn', None) and not cleaned_data.get('prn_reason', None):  #prn reason missing
            self.add_error('prn_reason', "Did you mean to check the is prn button? If so, please enter the prn reason.")

    def save(self, commit=True) -> Prescription:
        data = self.cleaned_data

        prescriber = data['prescriber']
        route = data['routes'].first()
        frequency = data['frequencies'].first()
        medication = data['medications'].first()
        patient = Patient.objects.get(id=self.__patient_id)

        # create new prescription record
        prescription = Prescription.objects.create(patient=patient,
                                                   prescriber=prescriber,
                                                   instructions=data['instructions'],
                                                   is_prn=data['is_prn'],
                                                   prn_reason=data['prn_reason'],
                                                   quantity_per_dose=data['quantity_per_dose'],
                                                   dose_units=data['dose_units']
                                                  )

        # create new prescription/medication association
        prescription.medications.add(medication)

        # create new prescription/route association
        prescription.routes.add(route)

        # create new prescription/frequency association
        prescription.frequencies.add(frequency)

        return prescription


class AdministrationTimeMulipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.value

class PrescriptionEditForm(forms.Form):
    administration_times = AdministrationTimeMulipleChoiceField(queryset=AdministrationTime.objects.all(),
                                                                      to_field_name='value',
                                                                      label='Administration Times',
                                                                      help_text='Hold ctrl or cmnd and click multiple times to select')

