# Generated by Django 4.2.7 on 2024-05-27 14:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("realowner", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="transferred_items_count",
            field=models.PositiveIntegerField(default=0),
        ),
    ]