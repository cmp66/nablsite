# Generated by Django 4.2 on 2023-04-19 02:24

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Rotowire",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("mlbteam", models.CharField(max_length=32)),
                ("reportdate", models.DateTimeField(blank=True, null=True)),
                ("news", models.CharField(max_length=2048)),
                ("comment", models.CharField(max_length=2048)),
            ],
            options={
                "verbose_name": "Rotowire Record",
                "verbose_name_plural": "Rotowire Records",
                "db_table": "rotowire",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Rotowiremissing",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("playername", models.CharField(max_length=128)),
                ("mlbteam", models.CharField(max_length=32)),
                ("reportdate", models.DateTimeField(blank=True, null=True)),
                ("news", models.CharField(max_length=2048)),
                ("comment", models.CharField(max_length=2048)),
                ("active_mlb", models.IntegerField()),
            ],
            options={
                "verbose_name": "Rotowire Missing Record",
                "verbose_name_plural": "Rotowire Missing Records",
                "db_table": "rotowiremissing",
                "managed": False,
            },
        ),
    ]
