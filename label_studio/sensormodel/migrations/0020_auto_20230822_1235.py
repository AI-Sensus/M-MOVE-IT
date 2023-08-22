# Generated by Django 3.2.19 on 2023-08-22 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_projectimport'),
        ('sensormodel', '0019_deployment_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
        migrations.AddField(
            model_name='subject',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
    ]
