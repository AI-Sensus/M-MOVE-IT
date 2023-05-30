# Generated by Django 3.2.14 on 2022-10-18 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensormodel', '0005_auto_20221010_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='deployment',
            name='name',
            field=models.TextField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='position',
            field=models.TextField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='sensorlist',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='subjectlist',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='subject',
            name='extra_info',
            field=models.TextField(blank=True, max_length=100),
        ),
    ]