# Generated by Django 4.0.5 on 2022-07-18 03:54

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(help_text='Street address 1', max_length=256)),
                ('street2', models.CharField(blank=True, help_text='Street address 2', max_length=256, null=True)),
                ('city', models.CharField(help_text='City', max_length=80)),
                ('state_name', models.CharField(help_text='State', max_length=80)),
                ('county', models.CharField(blank=True, help_text='State', max_length=80, null=True)),
                ('zip_code', models.CharField(help_text='Zip Code', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ContactInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferred_type', models.CharField(choices=[('home', 'Home'), ('mobile', 'Mobile'), ('email', 'Email'), ('text', 'Text'), ('fax', 'Fax')], help_text='Preferred contact type', max_length=6)),
                ('home_phone', models.CharField(blank=True, help_text='Home telephone number', max_length=15, null=True)),
                ('mobile_phone', models.CharField(blank=True, help_text='Mobile device number', max_length=15, null=True)),
                ('fax_number', models.CharField(blank=True, help_text='Fax number', max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birth_date', models.DateField()),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='src.address')),
                ('contact_information', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='src.contactinformation')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]