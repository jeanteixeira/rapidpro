# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-09 13:36
from __future__ import unicode_literals

import itertools

from django.db import migrations

from temba.values.constants import Value


def contact_field_generator(apps):
    Org = apps.get_model("orgs.Org")
    ContactField = apps.get_model("contacts.ContactField")

    for org in Org.objects.all():
        field_id = ContactField(
            org_id=org.id,
            label="ID",
            key="id",
            value_type=Value.TYPE_NUMBER,
            show_in_table=False,
            created_by=org.created_by,
            modified_by=org.modified_by,
            field_type="S",
        )
        yield field_id


def add_system_contact_fields(apps, schema_editor):
    ContactField = apps.get_model("contacts.ContactField")
    all_contact_fields = contact_field_generator(apps)

    # https://docs.djangoproject.com/en/2.0/ref/models/querysets/#bulk-create
    batch_size = 1000
    while True:
        batch = list(itertools.islice(all_contact_fields, batch_size))

        if len(batch) == 0:
            break

        ContactField.all_fields.bulk_create(batch, batch_size)


class Migration(migrations.Migration):

    dependencies = [("contacts", "0089_auto_20180723_1347")]

    operations = [migrations.RunPython(add_system_contact_fields)]