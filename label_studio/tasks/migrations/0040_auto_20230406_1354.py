# Generated by Django 3.2.16 on 2023-04-06 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0039_merge_0029_auto_20221005_1620_0038_auto_20230209_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='last_action',
            field=models.CharField(choices=[('prediction', 'Created from prediction'), ('propagated_annotation', 'Created from another annotation'), ('imported', 'Imported'), ('submitted', 'Submitted'), ('updated', 'Updated'), ('skipped', 'Skipped'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('fixed_and_accepted', 'Fixed and accepted'), ('deleted_review', 'Deleted review')], default=None, help_text='Action which was performed in the last annotation history item', max_length=128, null=True, verbose_name='last action'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='last_created_by',
            field=models.ForeignKey(default=None, help_text='User who created the last annotation history item', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='last created by'),
        ),
        migrations.AddIndex(
            model_name='annotation',
            index=models.Index(fields=['last_action'], name='task_comple_last_ac_777e69_idx'),
        ),
    ]
