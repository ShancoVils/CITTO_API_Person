# Generated by Django 3.2.5 on 2021-08-09 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person_manage', '0012_remove_customuser_fio'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='fio',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
