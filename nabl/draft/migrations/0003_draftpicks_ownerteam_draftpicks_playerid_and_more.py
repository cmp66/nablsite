# Generated by Django 4.2 on 2023-04-26 00:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0006_players_unique_bbrefid'),
        ('league', '0001_initial'),
        ('draft', '0002_alter_draftorder_options_alter_draftpicks_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='draftpicks',
            name='ownerteam',
            field=models.ForeignKey(blank=True, db_column='ownerteam', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ownerteam', to='league.teams'),
        ),
        migrations.AddField(
            model_name='draftpicks',
            name='playerid',
            field=models.ForeignKey(blank=True, db_column='playerid', null=True, on_delete=django.db.models.deletion.CASCADE, to='player.players'),
        ),
        migrations.AddField(
            model_name='draftpicks',
            name='slotteam',
            field=models.ForeignKey(blank=True, db_column='slotteam', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slotteam', to='league.teams'),
        ),
    ]
