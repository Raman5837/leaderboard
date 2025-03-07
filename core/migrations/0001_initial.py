# Generated by Django 5.1.7 on 2025-03-06 16:35

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
            name="GameSession",
            fields=[
                ("is_deleted", models.BooleanField(default=False)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "id",
                    models.BigAutoField(
                        db_index=True, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("score", models.BigIntegerField(db_index=True, default=0)),
                ("timestamp", models.BigIntegerField()),
                (
                    "mode",
                    models.CharField(
                        choices=[
                            ("SINGLE", "Single"),
                            ("MULTI_PLAYER", "Multi Player"),
                        ],
                        max_length=64,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="games",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
                "indexes": [
                    models.Index(
                        fields=["created_at", "is_deleted"],
                        name="core_gamese_created_4d42ae_idx",
                    )
                ],
            },
        ),
    ]
