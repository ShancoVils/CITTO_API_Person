# Generated by Django 3.2.5 on 2021-08-06 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person_manage', '0006_auto_20210806_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(blank=True, max_length=30, verbose_name='Имя'),
        ),
    ]
