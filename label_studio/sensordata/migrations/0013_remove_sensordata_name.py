# Generated by Django 3.1.14 on 2023-11-08 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensordata', '0012_auto_20231026_2010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensordata',
            name='name',
        ),
    ]
