# Generated by Django 4.2 on 2023-04-26 00:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stats", "0003_delete_nabladminstatrecords_gameresults_homepitcher_and_more"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="teamresults",
            constraint=models.UniqueConstraint(
                fields=("teamid", "year"), name="unique_team_year"
            ),
        ),
    ]
