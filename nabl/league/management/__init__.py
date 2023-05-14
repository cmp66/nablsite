import logging
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nabl.settings")
django.setup()

from stats.models import Teamresults  # noqa: E402
from player.models import Rosterassign  # noqa: E402
from league.models import Schedules  # noqa: E402


class LeagueManager:
    def migrate_team_results(self, new_season, existing_season):
        team_results = Teamresults.objects.filter(year=existing_season)

        for team_result in team_results:
            existing_result = Teamresults.objects.filter(
                year=new_season, teamid=team_result.teamid
            )

            if not existing_result:
                new_result = Teamresults()
                new_result.teamid = team_result.teamid
                new_result.year = new_season
                new_result.won = 0
                new_result.lost = 0
                new_result.leagueid = team_result.leagueid
                new_result.divisionid = team_result.divisionid
                new_result.save()
                logging.info(f"Migrated {new_result}")
            else:
                logging.info(f"Team Result exists: {existing_result[0]}")

    def migrate_rosters_assigns(self, new_season, existing_season):
        roster_assigns = Rosterassign.objects.filter(year=existing_season)

        for roster_assign in roster_assigns:
            existing_assign = Rosterassign.objects.filter(
                year=new_season,
                playerid=roster_assign.playerid,
                teamid=roster_assign.teamid,
            )

            if not existing_assign:
                new_assign = Rosterassign()
                new_assign.year = new_season
                new_assign.playerid = roster_assign.playerid
                new_assign.teamid = roster_assign.teamid

                new_assign.save()
                logging.info(f"Migrated {new_assign}")
            else:
                logging.info(f"Roster Assign exists: {existing_assign[0]}")

    def migrate_schedules(self, new_season, existing_season):
        old_schedules = Schedules.objects.filter(year=existing_season)

        for old_schedule in old_schedules:
            existing_schedule = Schedules.objects.filter(
                year=new_season,
                hometeam=old_schedule.hometeam,
                visitteam=old_schedule.visitteam,
                playmonth=old_schedule.playmonth,
                monthidx=old_schedule.monthidx,
            )

            if not existing_schedule:
                new_schedule = Schedules()
                new_schedule.year = new_season
                new_schedule.hometeam = old_schedule.hometeam
                new_schedule.visitteam = old_schedule.visitteam
                new_schedule.homewins = 0
                new_schedule.visitwins = 0
                new_schedule.playmonth = old_schedule.playmonth
                new_schedule.monthidx = old_schedule.monthidx
                new_schedule.numgames = old_schedule.numgames
                new_schedule.save()
                logging.info(f"Migrated {new_schedule}")
            else:
                logging.info(f"Schedule exists: {existing_schedule[0]}")
