# Generated by Django 1.11.2 on 2017-06-22 15:32

from django.db import migrations
from uuid import uuid4


def populate_flow_start_uuid(FlowStart):
    start_ids = list(FlowStart.objects.values_list('id', flat=True))
    if not start_ids:
        return

    print("Fetched %d flow start ids that need UUIDs..." % len(start_ids))
    num_updated = 0

    for start_id in start_ids:
        FlowStart.objects.filter(id=start_id).update(uuid=uuid4())
        num_updated += 1

        if num_updated % 1000 == 0:
            print(" > Updated %d of %d flow starts" % (num_updated, len(start_ids)))


def apply_manual():
    from temba.flows.models import FlowStart
    populate_flow_start_uuid(FlowStart)


def apply_as_migration(apps, schema_editor):
    FlowStart = apps.get_model('flows', 'FlowStart')
    populate_flow_start_uuid(FlowStart)


class Migration(migrations.Migration):

    dependencies = [
        ('flows', '0104_flowstart_uuid'),
    ]

    operations = [
        migrations.RunPython(apply_as_migration)
    ]
