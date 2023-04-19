from django.db import models
from django.contrib import admin
from league.models import Teams


class Transactions(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.IntegerField()
    transdate = models.DateTimeField()
    team1 = models.IntegerField()
    team2 = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'transactions'
        verbose_name_plural = 'Transactions'
        verbose_name = 'Transaction'

    def __str__(self):
        return str(self.id)
    
class TransactionsAdmin(admin.ModelAdmin):
    fields = ['type', 'transdate', 'team1', 'team2']
    list_display = ('type', 'transdate', 'team1', 'team2')
    search_fields = ['type', 'team1']

class Players(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=32)
    lastname = models.CharField(max_length=32)
    displayname = models.CharField(max_length=32)
    startyear = models.IntegerField()
    endyear = models.IntegerField()
    bbreflink = models.CharField(max_length=128)
    rotowireid = models.CharField(max_length=16, blank=True, null=True)
    position = models.CharField(max_length=8)
    bats = models.CharField(max_length=8, blank=True, null=True)
    throwhand = models.CharField(max_length=8, blank=True, null=True)
    birthdate = models.CharField(max_length=24, blank=True, null=True)

    class Meta:
        db_table = 'players'
        verbose_name = 'Player'
        verbose_name_plural = 'Players'
        ordering = ['lastname', 'firstname']

    def __str__(self):
        return f'{self.displayname}'
        
class PlayersAdmin(admin.ModelAdmin):
    fields = ['firstname', 'lastname', 'displayname', 'startyear', 'endyear', 'bbreflink', 'position']
    list_display = ('id', 'firstname', 'lastname', 'displayname', 'startyear', 'endyear', 'bbreflink', 'position')
    search_fields = ['firstname', 'lastname', 'displayname', 'position', 'bbreflink']

# class Assignments(models.Model):
#     id = models.AutoField(primary_key=True)
#     playerid = models.ForeignKey(Players, models.CASCADE, db_column='playerid')
#     teamid = models.ForeignKey(Teams, models.CASCADE, db_column='teamid')
#     transactionid = models.ForeignKey(Transactions, models.CASCADE, db_column='transactionid')

#     class Meta:
#         db_table = 'assignments'

class CardedPlayers(models.Model):
    id = models.AutoField(primary_key=True)
    playername = models.CharField(max_length=64)
    season = models.IntegerField()
    playerid = models.ForeignKey(Players, models.CASCADE, db_column='playerid', blank=True, null=True)
    mlbteam = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'cardedplayers'
        unique_together = (('playerid', 'season'),)
        verbose_name = 'Carded Player'
        verbose_name_plural = 'Carded Players'

        def __str__(self):
            return f'{self.playername}'
        
class CardedPlayersAdmin(admin.ModelAdmin):
    fields = ['playername', 'season', 'mlbteam']
    list_display = ('id', 'playername', 'season', 'mlbteam')
    search_fields = ['season', 'playername', 'mlbteam']


class Playercuts(models.Model):
    playerid = models.OneToOneField(Players, models.CASCADE, primary_key=True, db_column='playerid')
    season = models.IntegerField()
    teamid = models.ForeignKey(Teams, models.CASCADE, db_column='teamid')

    class Meta:
        db_table = 'playercuts'


class Rosterassign(models.Model):
    id = models.AutoField(primary_key=True)
    playerid = models.ForeignKey(Players, models.CASCADE, db_column='playerid')
    teamid = models.ForeignKey(Teams, models.CASCADE, db_column='teamid')
    year = models.IntegerField()

    class Meta:
        db_table = 'rosterassign'
        unique_together = (('playerid', 'teamid', 'year'),)
        verbose_name = 'Roster Assignment'
        verbose_name_plural = 'Roster Assignments'

class RosterassignAdmin(admin.ModelAdmin):
    fields = ['playerid', 'teamid', 'year']
    list_filter = ('teamid',)
    list_display = ('id', 'playerid', 'teamid', 'year')
    search_fields = ['playerid__displayname', 'year']

class Rostermove(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField()
    teamid = models.ForeignKey(Teams, models.CASCADE, db_column='teamid')
    transactionid = models.ForeignKey(Transactions, models.CASCADE, db_column='transactionid')
    resourcetype = models.IntegerField()
    resourceid = models.IntegerField()


    class Meta:
        db_table = 'rostermove'
        verbose_name = 'Transaction Item'
        verbose_name_plural = 'Transaction Items'

class RostermoveAdmin(admin.ModelAdmin):
    fields = ['type', 'teamid', 'transactionid', 'resourcetype', 'resourceid']
    list_display = ('id', 'type', 'teamid', 'transactionid', 'resourcetype', 'resourceid')
    search_fields = ['type', 'teamid__name', 'transactionid__id']


class Rosters(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    season = models.IntegerField()
    teamid = models.ForeignKey(Teams, models.CASCADE, db_column='teamid')

    class Meta:
        db_table = 'rosters'


class Rosterslot(models.Model):
    rosterid = models.ForeignKey(Teams, models.CASCADE, db_column='rosterid')
    playerid = models.ForeignKey(Players, models.CASCADE, db_column='playerid')

    class Meta:
        db_table = 'rosterslot'

