# Generated by Django 3.0.8 on 2021-03-16 07:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pet_shop', '0005_auto_20210315_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='Enter Vaccine name', max_length=30)),
                ('description', models.CharField(default='', help_text='Enter description', max_length=300)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='pet',
            name='birth',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 16, 15, 46, 34, 46528), help_text='Enter pet birth'),
        ),
        migrations.CreateModel(
            name='Pet_Vaccine_Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', help_text='Enter description', max_length=300)),
                ('date', models.DateTimeField(help_text='Enter Date')),
                ('pet_id', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='pet_shop.Pet')),
                ('type', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='pet_shop.Vaccine')),
            ],
            options={
                'ordering': ['pet_id'],
            },
        ),
    ]
