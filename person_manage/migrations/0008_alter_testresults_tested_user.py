# Generated by Django 3.2.5 on 2021-08-16 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('person_manage', '0007_auto_20210813_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresults',
            name='tested_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
