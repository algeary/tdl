# Generated by Django 4.2.7 on 2023-11-29 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_task_due_time_alter_task_priority_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='due_time',
        ),
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority_level',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
