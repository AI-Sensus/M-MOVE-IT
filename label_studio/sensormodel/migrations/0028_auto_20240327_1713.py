# Generated by Django 3.1.14 on 2024-03-27 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensormodel', '0027_remove_sensortype_timezone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='extra_info',
            field=models.TextField(blank=True),
        ),
    ]
