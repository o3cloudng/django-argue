# Generated by Django 4.1.2 on 2022-11-05 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_settings", "0005_airlab_aviationstack_aircrafttype_is_active_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="airport",
            name="timezone",
            field=models.DateTimeField(blank=True, max_length=32),
        ),
    ]
