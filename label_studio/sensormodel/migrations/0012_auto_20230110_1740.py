# Generated by Django 3.2.14 on 2023-01-10 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sensormodel', '0011_auto_20221126_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensortype',
            name='col_names_row',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='sensortype',
            name='comment_style',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sensortype',
            name='date_row',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='sensortype',
            name='format_string',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sensortype',
            name='relative_absolute',
            field=models.CharField(default='relative', max_length=100),
        ),
        migrations.AddField(
            model_name='sensortype',
            name='sensor_id_column',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='sensortype',
            name='sensor_id_regex',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sensortype',
            name='sensor_id_row',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='sensortype',
            name='time_row',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='sensortype',
            name='timestamp_column',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='sensortype',
            name='timestamp_unit',
            field=models.CharField(default='seconds', max_length=100),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='sensortype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='sensormodel.sensortype'),
        ),
    ]