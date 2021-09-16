# Generated by Django 3.2.7 on 2021-09-15 14:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_number', models.CharField(max_length=4, unique=True, validators=[django.core.validators.MinLengthValidator(limit_value=4), django.core.validators.MaxLengthValidator(limit_value=4)], verbose_name='Employee Number')),
                ('role', models.CharField(choices=[('ADMIN', 'Admin'), ('EMPLOYEE', 'Employee')], max_length=10, verbose_name='Role')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
