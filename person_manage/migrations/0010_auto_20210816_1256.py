# Generated by Django 3.2.5 on 2021-08-16 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person_manage', '0009_auto_20210816_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresults',
            name='test_answers',
            field=models.JSONField(blank=True, max_length=255, null=True, verbose_name='Ответы'),
        ),
        migrations.AlterField(
            model_name='testresults',
            name='test_result',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Итог'),
        ),
        migrations.AlterField(
            model_name='testresults',
            name='test_sum_factor',
            field=models.IntegerField(blank=True, null=True, verbose_name='Результат'),
        ),
    ]
