# Generated by Django 3.2.19 on 2023-08-09 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0022_projectimport'),
        ('sensormodel', '0019_deployment_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorOffset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offset', models.IntegerField(blank=True, null=True)),
                ('offset_Date', models.DateTimeField(blank=True, null=True)),
                ('camera', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Camera_offsets', to='sensormodel.sensor')),
                ('imu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Imu_offsets', to='sensormodel.sensor')),
            ],
        ),
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('begin_datetime', models.DateTimeField(blank=True, null=True)),
                ('end_datetime', models.DateTimeField(blank=True, null=True)),
                ('file_hash', models.CharField(blank=True, max_length=10, null=True)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('sensor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sensormodel.sensor')),
            ],
        ),
    ]
