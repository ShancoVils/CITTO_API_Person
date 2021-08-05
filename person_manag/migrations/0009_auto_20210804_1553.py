# Generated by Django 3.2.5 on 2021-08-04 12:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('person_manag', '0008_alter_customuser_person_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='data_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='customuser',
            name='data_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
