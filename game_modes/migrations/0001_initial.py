# Generated by Django 3.2.13 on 2022-05-26 20:48

import uuid

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AreaCode",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "area_code",
                    models.PositiveSmallIntegerField(
                        help_text="3 digit Area Code",
                        unique=True,
                        validators=[
                            django.core.validators.MaxValueValidator(999),
                            django.core.validators.MinValueValidator(0),
                        ],
                    ),
                ),
            ],
            options={
                "verbose_name": "Area Code",
                "verbose_name_plural": "Area Codes",
                "db_table": "area_codes",
                "ordering": ["-created_at"],
                "get_latest_by": "created_at",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="GameMode",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(help_text="Game Mode Name", max_length=100)),
            ],
            options={
                "verbose_name": "Game Mode",
                "verbose_name_plural": "Game Modes",
                "db_table": "game_modes",
                "ordering": ["-created_at"],
                "get_latest_by": "created_at",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserPreference",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("area_code_mapped_at", models.DateTimeField()),
                ("game_mode_mapped_at", models.DateTimeField()),
                ("is_current_preference", models.BooleanField(default=True)),
                (
                    "area_code",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="game_modes.areacode",
                    ),
                ),
                (
                    "game_mode",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="game_modes.gamemode",
                    ),
                ),
                (
                    "gamer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "User Preference",
                "verbose_name_plural": "User Preferences",
                "db_table": "user_preferences",
                "ordering": ["-created_at"],
                "get_latest_by": "created_at",
                "abstract": False,
            },
        ),
    ]
