# Generated by Django 3.2 on 2021-04-09 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0023_alter_table_array_tables"),
    ]

    operations = [
        migrations.RenameField(
            model_name="dataselection",
            old_name="column_headings",
            new_name="headings_type",
        ),
        migrations.RenameField(
            model_name="table",
            old_name="columns",
            new_name="column_headings",
        ),
        migrations.RenameField(
            model_name="table",
            old_name="flatten_name",
            new_name="heading",
        ),
    ]
