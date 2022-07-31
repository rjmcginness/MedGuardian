# Generated by Django 4.0.5 on 2022-07-31 23:15

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_administered', models.FloatField(help_text='Quantity administered')),
                ('date_time_taken', models.DateTimeField(default=datetime.datetime(2022, 7, 31, 23, 15, 17, 290879, tzinfo=utc), help_text='Date and time taken')),
                ('description', models.CharField(help_text='Details about this administration of medication', max_length=256)),
                ('outcome', models.TextField(help_text='Outcome of this administration of medication')),
            ],
        ),
        migrations.CreateModel(
            name='AdministrationFrequency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of administration frequency', max_length=80, unique=True)),
                ('abbreviation', models.CharField(help_text='Abbreviation for administration frequency', max_length=12)),
                ('description', models.CharField(help_text='Description of administration frequency', max_length=256)),
                ('is_continuous', models.BooleanField(default=False, help_text='Is this a continuous administration')),
                ('value', models.FloatField(default=1, help_text='Number of times administered per unit')),
                ('units', models.CharField(help_text='Units for frequency: hour, day, etc', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='AdministrationTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TimeField()),
                ('description', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactTimes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instances', models.PositiveIntegerField(blank=True, default=1)),
            ],
        ),
        migrations.CreateModel(
            name='PatientPrescribers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Pharmacist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text="Pharmacist's first name", max_length=30)),
                ('last_name', models.CharField(help_text="Pharmacist's last name", max_length=30)),
                ('license_number', models.CharField(help_text='State Pharmacist license number', max_length=20)),
                ('license_state', models.CharField(help_text="State of pharmacist's license", max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PharmacistTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Pharmacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Pharmacy name', max_length=128)),
                ('federal_dea', models.CharField(help_text='Federal DEA number', max_length=9)),
                ('state_license', models.CharField(help_text='State license number', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PharmacyPharmacist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Prescriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text="Prescriber's first name", max_length=30)),
                ('last_name', models.CharField(help_text="Prescriber's last name", max_length=30)),
                ('federal_dea', models.CharField(help_text='DEA Number', max_length=9)),
                ('state_dea', models.CharField(help_text='State controlled substance license number', max_length=20)),
                ('credentials', models.CharField(blank=True, max_length=20, null=True)),
                ('specialty', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_per_dose', models.FloatField(default=1, help_text='Quantity to be administered for each dose')),
                ('dose_units', models.CharField(help_text='Units of quantity per dose', max_length=20)),
                ('is_prn', models.BooleanField(blank=True, default=False, help_text='Is this an "as needed" medication')),
                ('prn_reason', models.CharField(blank=True, help_text='Reason for "as needed" use', max_length=128, null=True)),
                ('instructions', models.TextField(verbose_name='SIG: how is the medication to be used')),
                ('quantity', models.FloatField(blank=True, help_text='Amount of medication purchased or prescribed', null=True)),
                ('duration_of_therapy', models.PositiveIntegerField(blank=True, help_text='How long to take this medication', null=True)),
                ('duration_units', models.CharField(blank=True, help_text='Units for duration: days, hours, etc', max_length=40, null=True)),
                ('refills', models.PositiveSmallIntegerField(blank=True, help_text='Refills authorized', null=True)),
                ('signature', models.BinaryField(blank=True, help_text='Signature image', null=True)),
                ('date_written', models.DateField(blank=True, help_text='Date Written', null=True)),
                ('expiration_date', models.DateField(blank=True, help_text='Expiration date', null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Is this prescription still active')),
            ],
        ),
        migrations.CreateModel(
            name='PrescriptionCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text="Customer's first name", max_length=30)),
                ('last_name', models.CharField(help_text="Customer's last name", max_length=30)),
                ('license_number', models.CharField(help_text="Customer's id number", max_length=20)),
                ('license_state', models.CharField(help_text="State of customer's id", max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='RouteOfAdministration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of route of administration', max_length=80, unique=True)),
                ('abbreviation', models.CharField(help_text='Route of administration abbreviation', max_length=12)),
                ('description', models.CharField(blank=True, help_text='Description of route of administration', max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of transaction type', max_length=80)),
                ('code', models.PositiveSmallIntegerField(help_text='Transaction code')),
            ],
        ),
        migrations.CreateModel(
            name='PrescriptionTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(help_text='Status of prescription', max_length=20)),
                ('transaction_date_time', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prescriptions.prescriptioncustomer')),
                ('pharmacists', models.ManyToManyField(through='prescriptions.PharmacistTransaction', to='prescriptions.pharmacist')),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.prescription')),
            ],
        ),
        migrations.CreateModel(
            name='PrescriptionRoute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('administration_route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.routeofadministration')),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.prescription')),
            ],
        ),
        migrations.CreateModel(
            name='PrescriptionMedication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medications.medication')),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.prescription')),
            ],
        ),
        migrations.CreateModel(
            name='PrescriptionFrequency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.administrationfrequency')),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.prescription')),
            ],
        ),
        migrations.CreateModel(
            name='PrescriptionAdminTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('administration_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.administrationtime')),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescriptions.prescription')),
            ],
        ),
        migrations.AddField(
            model_name='prescription',
            name='administration_times',
            field=models.ManyToManyField(through='prescriptions.PrescriptionAdminTime', to='prescriptions.administrationtime'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='frequencies',
            field=models.ManyToManyField(through='prescriptions.PrescriptionFrequency', to='prescriptions.administrationfrequency'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='medications',
            field=models.ManyToManyField(through='prescriptions.PrescriptionMedication', to='medications.medication'),
        ),
    ]
