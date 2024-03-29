# Generated by Django 4.2.6 on 2023-10-29 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_task_created_location_task_created_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='created_time',
        ),
        migrations.AddField(
            model_name='task',
            name='completed_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='due_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='priority_level',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
