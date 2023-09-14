# Generated by Django 3.2.16 on 2023-07-26 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sensormodel', '0019_deployment_project'),
        ('sensordata', '0009_auto_20230721_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensoroffset',
            name='sensor_A',
        ),
        migrations.RemoveField(
            model_name='sensoroffset',
            name='sensor_B',
        ),
        migrations.AddField(
            model_name='sensoroffset',
            name='camera',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='camera_offsets', to='sensormodel.sensor'),
        ),
        migrations.AddField(
            model_name='sensoroffset',
            name='imu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imu_offsets', to='sensormodel.sensor'),
        ),
    ]
