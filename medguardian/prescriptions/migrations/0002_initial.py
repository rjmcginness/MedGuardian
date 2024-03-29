# Generated by Django 4.0.5 on 2022-07-31 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('src', '0001_initial'),
        ('prescriptions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.patient'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='prescriber',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prescriptions.prescriber'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='routes',
            field=models.ManyToManyField(through='prescriptions.PrescriptionRoute', to='prescriptions.routeofadministration'),
        ),
        migrations.AddField(
            model_name='prescriber',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.address'),
        ),
        migrations.AddField(
            model_name='prescriber',
            name='contact_information',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.contactinformation'),
        ),
        migrations.AddField(
            model_name='prescriber',
            name='patients',
            field=models.ManyToManyField(through='prescriptions.PatientPrescribers', to='src.patient'),
        ),
        migrations.AddField(
            model_name='pharmacypharmacist',
            name='pharmacist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.pharmacist'),
        ),
        migrations.AddField(
            model_name='pharmacypharmacist',
            name='pharmacy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.pharmacy'),
        ),
        migrations.AddField(
            model_name='pharmacy',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.address'),
        ),
        migrations.AddField(
            model_name='pharmacy',
            name='contact_information',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.contactinformation'),
        ),
        migrations.AddField(
            model_name='pharmacy',
            name='pharmacists',
            field=models.ManyToManyField(through='prescriptions.PharmacyPharmacist', to='prescriptions.pharmacist'),
        ),
        migrations.AddField(
            model_name='pharmacisttransaction',
            name='pharmacist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.pharmacist'),
        ),
        migrations.AddField(
            model_name='pharmacisttransaction',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.prescriptiontransaction'),
        ),
        migrations.AddField(
            model_name='patientprescribers',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.patient'),
        ),
        migrations.AddField(
            model_name='patientprescribers',
            name='prescriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.prescriber'),
        ),
        migrations.AddField(
            model_name='contacttimes',
            name='administration_time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.administrationtime'),
        ),
        migrations.AddField(
            model_name='contacttimes',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.contactinformation'),
        ),
        migrations.AddField(
            model_name='administration',
            name='prescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.prescription'),
        ),
        migrations.AddConstraint(
            model_name='prescriptionroute',
            constraint=models.UniqueConstraint(fields=('prescription', 'administration_route'), name='rx_route_unique'),
        ),
        migrations.AddConstraint(
            model_name='prescriptionfrequency',
            constraint=models.UniqueConstraint(fields=('prescription', 'frequency'), name='rx_frequency_unique'),
        ),
        migrations.AddConstraint(
            model_name='prescriptionadmintime',
            constraint=models.UniqueConstraint(fields=('prescription', 'administration_time'), name='rx_admin_time_unique'),
        ),
        migrations.AddConstraint(
            model_name='prescription',
            constraint=models.UniqueConstraint(fields=('id', 'patient_id', 'prescriber_id'), name='rx_unique'),
        ),
        migrations.AddConstraint(
            model_name='prescriber',
            constraint=models.UniqueConstraint(fields=('federal_dea', 'address_id'), name='prescriber_address_unique'),
        ),
        migrations.AddConstraint(
            model_name='patientprescribers',
            constraint=models.UniqueConstraint(fields=('patient', 'prescriber'), name='patient_prescriber_unique'),
        ),
        migrations.AddConstraint(
            model_name='contacttimes',
            constraint=models.UniqueConstraint(fields=('contact_id', 'administration_time_id'), name='contact_time_unique'),
        ),
    ]
