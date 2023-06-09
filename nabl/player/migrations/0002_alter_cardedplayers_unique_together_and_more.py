# Generated by Django 4.2 on 2023-04-21 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("player", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="cardedplayers",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="cardedplayers",
            name="playerid",
            field=models.ForeignKey(
                blank=True,
                db_column="playerid",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="player.players",
            ),
        ),
    ]
