# Generated by Django 3.2.5 on 2021-08-11 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('person_manage', '0022_auto_20210811_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailedtestresult',
            name='test_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_detail', to='person_manage.testresults', verbose_name='Номер теста'),
        ),
    ]