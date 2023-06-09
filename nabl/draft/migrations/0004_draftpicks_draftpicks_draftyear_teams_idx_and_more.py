# Generated by Django 4.2 on 2023-04-28 02:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("draft", "0003_draftpicks_ownerteam_draftpicks_playerid_and_more"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="draftpicks",
            index=models.Index(
                fields=["draftyear", "slotteam", "ownerteam"],
                name="draftpicks_draftyear_teams_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="draftpicks",
            index=models.Index(fields=["playerid"], name="draftpicks_playerid_idx"),
        ),
    ]
