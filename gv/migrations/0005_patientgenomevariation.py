# Generated by Django 2.1.1 on 2019-01-13 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gv', '0004_auto_20181229_2132'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientGenomeVariation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variation_data', models.TextField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gv.Patient')),
            ],
        ),
    ]
