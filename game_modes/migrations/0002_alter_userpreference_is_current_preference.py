# Generated by Django 3.2.13 on 2022-05-27 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game_modes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userpreference",
            name="is_current_preference",
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
