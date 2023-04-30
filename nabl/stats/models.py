from django.db import models
from django.contrib import admin
from league.models import Schedules, Teams, Divisions, Leagues
from player.models import Players


class Gameresults(models.Model):
    id = models.AutoField(primary_key=True)
    scheduleid = models.ForeignKey(
        Schedules, models.CASCADE, db_column="scheduleid", default=0
    )
    gamenumber = models.IntegerField()
    homepitcher = models.ForeignKey(
        Players,
        models.CASCADE,
        db_column="homepitcher",
        related_name="gameresults_homepitcher",
        blank=True,
        null=True,
    )
    visitpitcher = models.ForeignKey(
        Players,
        models.CASCADE,
        db_column="visitpitcher",
        related_name="gameresults_visitpitcher",
        blank=True,
        null=True,
    )
    homeruns = models.IntegerField()
    visitruns = models.IntegerField()
    comment = models.CharField(max_length=8000)

    class Meta:
        db_table = "gameresults"
        unique_together = (("scheduleid", "gamenumber"),)


class GameresultsAdmin(admin.ModelAdmin):
    fields = [
        "scheduleid",
        "gamenumber",
        "homepitcher",
        "visitpitcher",
        "homeruns",
        "visitruns",
        "comment",
    ]
    list_display = (
        "scheduleid",
        "gamenumber",
        "homepitcher",
        "visitpitcher",
        "homeruns",
        "visitruns",
    )
    search_fields = [
        "scheduleid",
        "gamenumber",
        "homepitcher",
        "visitpitcher",
        "homeruns",
        "visitruns",
    ]


class SeriesStatRecords(models.Model):
    id = models.AutoField(primary_key=True)
    series = models.ForeignKey(Schedules, models.CASCADE, db_column="series", default=0)
    season = models.IntegerField()
    reportingteamid = models.ForeignKey(
        Teams,
        models.CASCADE,
        db_column="reportingteamid",
        related_name="reportteam",
        default=0,
    )
    statsteamid = models.ForeignKey(
        Teams,
        models.CASCADE,
        db_column="statsteamid",
        related_name="statsteam",
        default=0,
    )
    playerid = models.ForeignKey(
        Players, models.CASCADE, db_column="playerid", default=0
    )
    games = models.IntegerField(blank=True, null=True)
    bat_ab = models.IntegerField(blank=True, null=True)
    bat_runs = models.IntegerField(blank=True, null=True)
    bat_hits = models.IntegerField(blank=True, null=True)
    bat_rbi = models.IntegerField(blank=True, null=True)
    bat_hr = models.IntegerField(blank=True, null=True)
    bat_doubles = models.IntegerField(blank=True, null=True)
    bat_triples = models.IntegerField(blank=True, null=True)
    bat_walks = models.IntegerField(blank=True, null=True)
    bat_strikeouts = models.IntegerField(blank=True, null=True)
    bat_sb = models.IntegerField(blank=True, null=True)
    bat_cs = models.IntegerField(blank=True, null=True)
    errors = models.IntegerField(blank=True, null=True)
    pitch_gs = models.IntegerField(blank=True, null=True)
    pitch_cg = models.IntegerField(blank=True, null=True)
    pitch_sho = models.IntegerField(blank=True, null=True)
    pitch_wins = models.IntegerField(blank=True, null=True)
    pitch_loss = models.IntegerField(blank=True, null=True)
    pitch_save = models.IntegerField(blank=True, null=True)
    pitch_ip = models.IntegerField(blank=True, null=True)
    pitch_hits = models.IntegerField(blank=True, null=True)
    pitch_er = models.IntegerField(blank=True, null=True)
    pitch_walks = models.IntegerField(blank=True, null=True)
    pitch_strikeouts = models.IntegerField(blank=True, null=True)
    pitch_hr = models.IntegerField(blank=True, null=True)
    pitch_ipfull = models.IntegerField(blank=True, null=True)
    pitch_ipfract = models.IntegerField(blank=True, null=True)
    bat_hbp = models.IntegerField(blank=True, null=True)
    pitch_gp = models.IntegerField(blank=True, null=True)
    pitch_runs = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "seriesstatrecords"
        unique_together = (
            ("series", "reportingteamid", "statsteamid", "season", "playerid"),
        )


class Statrecords(models.Model):
    id = models.AutoField(primary_key=True)
    playerid = models.ForeignKey(
        Players, models.CASCADE, db_column="playerid", default=0
    )
    season = models.IntegerField()
    teamid = models.ForeignKey(Teams, models.CASCADE, db_column="teamid", default=0)
    games = models.IntegerField(blank=True, null=True)
    bat_ab = models.IntegerField(blank=True, null=True)
    bat_runs = models.IntegerField(blank=True, null=True)
    bat_hits = models.IntegerField(blank=True, null=True)
    bat_rbi = models.IntegerField(blank=True, null=True)
    bat_hr = models.IntegerField(blank=True, null=True)
    bat_doubles = models.IntegerField(blank=True, null=True)
    bat_triples = models.IntegerField(blank=True, null=True)
    bat_walks = models.IntegerField(blank=True, null=True)
    bat_strikeouts = models.IntegerField(blank=True, null=True)
    bat_sb = models.IntegerField(blank=True, null=True)
    bat_cs = models.IntegerField(blank=True, null=True)
    errors = models.IntegerField(blank=True, null=True)
    pitch_gs = models.IntegerField(blank=True, null=True)
    pitch_cg = models.IntegerField(blank=True, null=True)
    pitch_sho = models.IntegerField(blank=True, null=True)
    pitch_wins = models.IntegerField(blank=True, null=True)
    pitch_loss = models.IntegerField(blank=True, null=True)
    pitch_save = models.IntegerField(blank=True, null=True)
    pitch_ip = models.IntegerField(blank=True, null=True)
    pitch_hits = models.IntegerField(blank=True, null=True)
    pitch_er = models.IntegerField(blank=True, null=True)
    pitch_walks = models.IntegerField(blank=True, null=True)
    pitch_strikeouts = models.IntegerField(blank=True, null=True)
    pitch_hr = models.IntegerField(blank=True, null=True)
    pitch_ipfull = models.IntegerField(blank=True, null=True)
    pitch_ipfract = models.IntegerField(blank=True, null=True)
    bat_hbp = models.IntegerField(blank=True, null=True)
    pitch_gp = models.IntegerField(blank=True, null=True)
    pitch_runs = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "statrecords"
        unique_together = (("playerid", "season", "teamid"),)


class Teamresults(models.Model):
    id = models.AutoField(primary_key=True)
    teamid = models.ForeignKey(Teams, models.CASCADE, db_column="teamid", default=0)
    divisionid = models.ForeignKey(
        Divisions, models.CASCADE, db_column="divisionid", default=0
    )
    year = models.IntegerField()
    leagueid = models.ForeignKey(
        Leagues, models.CASCADE, db_column="leagueid", default=0
    )
    won = models.IntegerField()
    lost = models.IntegerField()
    divisionwin = models.IntegerField(default=0)
    divisionloss = models.IntegerField(default=0)
    divisiontitle = models.IntegerField(default=0)
    worldseriesapp = models.IntegerField(default=0)
    worldserieswin = models.IntegerField(default=0)

    class Meta:
        db_table = "teamresults"
        unique_together = (("teamid", "year"),)
        verbose_name_plural = "Team Results"
        constraints = [
            models.UniqueConstraint(fields=["teamid", "year"], name="unique_team_year"),
        ]

    def __str__(self):
        return f"{self.teamid} {self.year}"


class TeamresultsAdmin(admin.ModelAdmin):
    fields = ["teamid", "divisionid", "year", "leagueid", "won", "lost"]
    list_display = ("teamid", "divisionid", "year", "leagueid", "won", "lost")
    search_fields = [
        "teamid__nickname",
        "divisionid__name",
        "year",
    ]
