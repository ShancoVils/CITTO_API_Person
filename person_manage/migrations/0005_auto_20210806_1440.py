# Generated by Django 3.2.5 on 2021-08-06 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person_manage', '0004_remove_customuser_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='last_name',
        ),
    ]
