# Generated by Django 3.2.5 on 2021-08-11 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('person_manage', '0019_auto_20210811_0951'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detailedtestresult',
            options={'verbose_name_plural': 'Детальные результаты тестов'},
        ),
        migrations.AddField(
            model_name='testresults',
            name='test_number',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='person_manage.detailedtestresult', verbose_name='Номер теста'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='detailedtestresult',
            name='test_number',
            field=models.IntegerField(verbose_name='Оценка'),
        ),
    ]
