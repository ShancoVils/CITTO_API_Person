# Generated by Django 3.2.5 on 2021-08-09 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person_manage', '0014_auto_20210809_1311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questionspull',
            options={'verbose_name_plural': 'Вопросы'},
        ),
        migrations.AddField(
            model_name='questionspull',
            name='factor',
            field=models.IntegerField(default=1, verbose_name='Коэффициент'),
            preserve_default=False,
        ),
    ]