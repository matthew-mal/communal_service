# Generated by Django 5.0.7 on 2024-07-17 07:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Rent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("year", models.IntegerField()),
                ("month", models.IntegerField()),
                ("total_rent", models.FloatField()),
                (
                    "apartment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rents",
                        to="service.apartment",
                    ),
                ),
            ],
        ),
    ]
