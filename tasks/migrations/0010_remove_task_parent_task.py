# Generated by Django 5.1.2 on 2024-11-11 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_task_parent_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='parent_task',
        ),
    ]
