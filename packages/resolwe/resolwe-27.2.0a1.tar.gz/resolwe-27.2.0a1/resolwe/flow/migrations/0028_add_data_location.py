# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-26 04:06
from __future__ import unicode_literals

import os

from django.conf import settings
from django.db import connection, migrations, models, transaction
import django.db.models.deletion


def set_data_location(apps, schema_editor):
    """Create DataLocation for each Data."""
    Data = apps.get_model("flow", "Data")
    DataLocation = apps.get_model("flow", "DataLocation")

    for data in Data.objects.all():
        if os.path.isdir(
            os.path.join(settings.FLOW_EXECUTOR["DATA_DIR"], str(data.id))
        ):
            with transaction.atomic():
                # Manually set DataLocation id to preserve data directory.
                data_location = DataLocation.objects.create(
                    id=data.id, subpath=str(data.id)
                )
                data_location.data.add(data)

    # Increment DataLocation id's sequence
    if DataLocation.objects.exists():
        max_id = DataLocation.objects.order_by("id").last().id
        with connection.cursor() as cursor:
            cursor.execute(
                "ALTER SEQUENCE flow_datalocation_id_seq RESTART WITH {};".format(
                    max_id + 1
                )
            )


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0027_data_purged"),
    ]

    operations = [
        migrations.CreateModel(
            name="DataLocation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subpath", models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="data",
            name="location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="data",
                to="flow.DataLocation",
            ),
        ),
        migrations.RunPython(set_data_location, reverse_code=migrations.RunPython.noop),
    ]
