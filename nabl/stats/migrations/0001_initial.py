# Generated by Django 4.2 on 2023-04-19 02:24

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Gameresults",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("gamenumber", models.IntegerField()),
                ("homeruns", models.IntegerField()),
                ("visitruns", models.IntegerField()),
                ("comment", models.CharField(max_length=8000)),
            ],
            options={
                "db_table": "gameresults",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="NabladminStatrecords",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("season", models.IntegerField()),
            ],
            options={
                "db_table": "nabladmin_statrecords",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="SeriesStatRecords",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("season", models.IntegerField()),
                ("games", models.IntegerField(blank=True, null=True)),
                ("bat_ab", models.IntegerField(blank=True, null=True)),
                ("bat_runs", models.IntegerField(blank=True, null=True)),
                ("bat_hits", models.IntegerField(blank=True, null=True)),
                ("bat_rbi", models.IntegerField(blank=True, null=True)),
                ("bat_hr", models.IntegerField(blank=True, null=True)),
                ("bat_doubles", models.IntegerField(blank=True, null=True)),
                ("bat_triples", models.IntegerField(blank=True, null=True)),
                ("bat_walks", models.IntegerField(blank=True, null=True)),
                ("bat_strikeouts", models.IntegerField(blank=True, null=True)),
                ("bat_sb", models.IntegerField(blank=True, null=True)),
                ("bat_cs", models.IntegerField(blank=True, null=True)),
                ("errors", models.IntegerField(blank=True, null=True)),
                ("pitch_gs", models.IntegerField(blank=True, null=True)),
                ("pitch_cg", models.IntegerField(blank=True, null=True)),
                ("pitch_sho", models.IntegerField(blank=True, null=True)),
                ("pitch_wins", models.IntegerField(blank=True, null=True)),
                ("pitch_loss", models.IntegerField(blank=True, null=True)),
                ("pitch_save", models.IntegerField(blank=True, null=True)),
                ("pitch_ip", models.IntegerField(blank=True, null=True)),
                ("pitch_hits", models.IntegerField(blank=True, null=True)),
                ("pitch_er", models.IntegerField(blank=True, null=True)),
                ("pitch_walks", models.IntegerField(blank=True, null=True)),
                ("pitch_strikeouts", models.IntegerField(blank=True, null=True)),
                ("pitch_hr", models.IntegerField(blank=True, null=True)),
                ("pitch_ipfull", models.IntegerField(blank=True, null=True)),
                ("pitch_ipfract", models.IntegerField(blank=True, null=True)),
                ("bat_hbp", models.IntegerField(blank=True, null=True)),
                ("pitch_gp", models.IntegerField(blank=True, null=True)),
                ("pitch_runs", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "seriesstatrecords",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Statrecords",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("season", models.IntegerField()),
                ("games", models.IntegerField(blank=True, null=True)),
                ("bat_ab", models.IntegerField(blank=True, null=True)),
                ("bat_runs", models.IntegerField(blank=True, null=True)),
                ("bat_hits", models.IntegerField(blank=True, null=True)),
                ("bat_rbi", models.IntegerField(blank=True, null=True)),
                ("bat_hr", models.IntegerField(blank=True, null=True)),
                ("bat_doubles", models.IntegerField(blank=True, null=True)),
                ("bat_triples", models.IntegerField(blank=True, null=True)),
                ("bat_walks", models.IntegerField(blank=True, null=True)),
                ("bat_strikeouts", models.IntegerField(blank=True, null=True)),
                ("bat_sb", models.IntegerField(blank=True, null=True)),
                ("bat_cs", models.IntegerField(blank=True, null=True)),
                ("errors", models.IntegerField(blank=True, null=True)),
                ("pitch_gs", models.IntegerField(blank=True, null=True)),
                ("pitch_cg", models.IntegerField(blank=True, null=True)),
                ("pitch_sho", models.IntegerField(blank=True, null=True)),
                ("pitch_wins", models.IntegerField(blank=True, null=True)),
                ("pitch_loss", models.IntegerField(blank=True, null=True)),
                ("pitch_save", models.IntegerField(blank=True, null=True)),
                ("pitch_ip", models.IntegerField(blank=True, null=True)),
                ("pitch_hits", models.IntegerField(blank=True, null=True)),
                ("pitch_er", models.IntegerField(blank=True, null=True)),
                ("pitch_walks", models.IntegerField(blank=True, null=True)),
                ("pitch_strikeouts", models.IntegerField(blank=True, null=True)),
                ("pitch_hr", models.IntegerField(blank=True, null=True)),
                ("pitch_ipfull", models.IntegerField(blank=True, null=True)),
                ("pitch_ipfract", models.IntegerField(blank=True, null=True)),
                ("bat_hbp", models.IntegerField(blank=True, null=True)),
                ("pitch_gp", models.IntegerField(blank=True, null=True)),
                ("pitch_runs", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "statrecords",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Teamresults",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("year", models.IntegerField()),
                ("won", models.IntegerField()),
                ("lost", models.IntegerField()),
                ("divisionwin", models.IntegerField()),
                ("divisionloss", models.IntegerField()),
                ("divisiontitle", models.IntegerField()),
                ("worldseriesapp", models.IntegerField()),
                ("worldserieswin", models.IntegerField()),
            ],
            options={
                "verbose_name_plural": "Team Results",
                "db_table": "teamresults",
                "managed": False,
            },
        ),
    ]
