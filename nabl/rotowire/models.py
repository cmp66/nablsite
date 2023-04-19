from django.db import models
from django.contrib import admin
from player.models import Players

class Rotowire(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Players, models.CASCADE, db_column='player')
    mlbteam = models.CharField(max_length=32)
    reportdate = models.DateTimeField(blank=True, null=True)
    news = models.CharField(max_length=2048)
    comment = models.CharField(max_length=2048)

    class Meta:
        managed = False
        db_table = 'rotowire'
        verbose_name = 'Rotowire Record'
        verbose_name_plural = 'Rotowire Records'

class RotowireAdmin(admin.ModelAdmin):
    fields = ['player', 'mlbteam', 'reportdate', 'news', 'comment']
    list_display = ('player', 'mlbteam', 'reportdate',)
    search_fields = ['player__displayname', 'reportdate',]


class Rotowiremissing(models.Model):
    id = models.AutoField(primary_key=True)
    playername = models.CharField(max_length=128)
    mlbteam = models.CharField(max_length=32)
    reportdate = models.DateTimeField(blank=True, null=True)
    news = models.CharField(max_length=2048)
    comment = models.CharField(max_length=2048)
    active_mlb = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rotowiremissing'
        verbose_name = 'Rotowire Missing Record'
        verbose_name_plural = 'Rotowire Missing Records'

class RotowiremissingAdmin(admin.ModelAdmin):
    fields = ['playername', 'mlbteam', 'reportdate', 'news', 'comment']
    list_display = ('playername', 'mlbteam', 'reportdate',)
    search_fields = ['playername', 'reportdate',]
