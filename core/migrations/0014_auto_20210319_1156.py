# Generated by Django 3.1.7 on 2021-03-19 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_auto_20210318_1415"),
    ]

    operations = [
        migrations.RenameField(
            model_name="url",
            old_name="data_file",
            new_name="file",
        ),
    ]
