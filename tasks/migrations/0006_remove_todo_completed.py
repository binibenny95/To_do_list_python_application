# Generated by Django 5.1.2 on 2024-11-02 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_todo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='completed',
        ),
    ]