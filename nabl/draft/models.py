from django.db import models
from django.contrib import admin
from league.models import Teams
from player.models import Players

class Draftorder(models.Model):
    teamlist = models.CharField(max_length=255, blank=True, null=True)
    draftyear = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'draftorder'


class Draftpicks(models.Model):
    pickid = models.AutoField(primary_key=True)
    draftyear = models.IntegerField()
    slotteam = models.ForeignKey(Teams, models.CASCADE, db_column='slotteam', related_name='slotteam')
    ownerteam = models.ForeignKey(Teams, models.CASCADE, db_column='ownerteam', related_name='ownerteam')
    playerid = models.ForeignKey(Players, models.CASCADE, db_column='playerid', blank=True, null=True)
    round = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'draftpicks'
        verbose_name = 'Draft Pick'
        verbose_name_plural = 'Draft Picks'

class DraftpicksAdmin(admin.ModelAdmin):
    fields = ['draftyear', 'slotteam', 'ownerteam', 'playerid', 'round']
    list_display = ('draftyear', 'slotteam', 'ownerteam', 'playerid', 'draftyear', 'round')
    search_fields = ['slotteam__city', 'ownerteam__city', 'round']
    list_filter = ('draftyear',)
