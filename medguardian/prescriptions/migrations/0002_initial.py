# Generated by Django 4.0.5 on 2022-07-18 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prescriptions', '0001_initial'),
        ('src', '0001_initial'),
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
            model_name='administration',
            name='prescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.prescription'),
        ),
    ]
