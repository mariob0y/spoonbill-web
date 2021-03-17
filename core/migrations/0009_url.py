# Generated by Django 3.1.7 on 2021-03-17 09:53

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_upload_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="Url",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("url", models.URLField()),
                ("filename", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("queued.download", "Queued download"),
                            ("downloading", "Downloading"),
                            ("queued.validation", "Queued validation"),
                            ("validation", "Validation"),
                        ],
                        default="queued.download",
                        max_length=32,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expired_at", models.DateTimeField(blank=True, null=True)),
                ("deleted", models.BooleanField(default=False)),
                ("downloaded", models.BooleanField(default=False)),
                (
                    "validation",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="core.validation"
                    ),
                ),
            ],
            options={
                "verbose_name": "Url",
                "verbose_name_plural": "Urls",
                "db_table": "urls",
            },
        ),
    ]
