from django.db import models
from django.contrib import admin
from league.models import Teams
from player.models import Players


class Draftorder(models.Model):
    teamlist = models.CharField(max_length=255, blank=True, null=True)
    draftyear = models.IntegerField(primary_key=True)

    class Meta:
        db_table = "draftorder"


class DraftorderAdmin(admin.ModelAdmin):
    fields = ["draftyear", "teamlist"]
    list_display = ("draftyear", "teamlist")
    search_fields = ["draftyear", "teamlist"]


class Draftpicks(models.Model):
    pickid = models.AutoField(primary_key=True)
    draftyear = models.IntegerField()
    slotteam = models.ForeignKey(
        Teams,
        models.CASCADE,
        db_column="slotteam",
        related_name="slotteam",
        blank=True,
        null=True,
    )
    ownerteam = models.ForeignKey(
        Teams,
        models.CASCADE,
        db_column="ownerteam",
        related_name="ownerteam",
        blank=True,
        null=True,
    )
    playerid = models.ForeignKey(
        Players, models.CASCADE, db_column="playerid", blank=True, null=True
    )
    round = models.IntegerField()

    class Meta:
        db_table = "draftpicks"
        verbose_name = "Draft Pick"
        verbose_name_plural = "Draft Picks"
        constraints = [
            models.UniqueConstraint(
                fields=["draftyear", "slotteam", "round"],
                name="unique_draftyear_slotteam",
            ),
        ]
        indexes = [
            models.Index(
                fields=["draftyear", "slotteam", "ownerteam"],
                name="draftpicks_draftyear_teams_idx",
            ),
            models.Index(fields=["playerid"], name="draftpicks_playerid_idx"),
            models.Index(fields=["draftyear"], name="draftpicks_draftyear_idx"),
        ]

    def __str__(self):
        return f"{self.draftyear} Slot:{self.slotteam} Owner:{self.ownerteam} Round:{self.round}"


class DraftpicksAdmin(admin.ModelAdmin):
    fields = ["draftyear", "slotteam", "ownerteam", "playerid", "round"]
    list_display = (
        "draftyear",
        "slotteam",
        "ownerteam",
        "playerid",
        "draftyear",
        "round",
    )
    search_fields = ["slotteam__city", "ownerteam__city", "round"]
    list_filter = ("draftyear",)
