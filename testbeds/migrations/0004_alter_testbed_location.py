# Generated by Django 4.2.9 on 2024-01-19 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testbeds', '0003_testbed_notes_alter_testbed_date_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testbed',
            name='location',
            field=models.TextField(default='notfree'),
        ),
    ]
