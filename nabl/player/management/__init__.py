from math import floor, isnan
from unidecode import unidecode

import logging
import os
import string
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nabl.settings")
django.setup()

from django.db.models import Count, Sum
from pybaseball import playerid_lookup, batting_stats
from pybaseball import lahman

from player.models import Players
from stats.models import Statrecords

player_shorthands = ["jr.", "sr.", "ii", "iii", "iv", "Jr.", "Sr.", "II", "III", "IV"]


class PlayerManager:
    def __init__(self, load_lahman=False):
        # self.lahman_data = lahman.download_lahman() if load_lahman else None
        # people = lahman.people()
        # people.to_csv('people.csv')
        self.fielding = lahman.fielding()
        # fielding.to_csv('fielding.csv')

    def get_player_info(self, lastname, firstname=None, target_year=None):
        """Get the player ID from the name."""

        player_ids = (
            playerid_lookup(lastname)
            if firstname is None
            else playerid_lookup(lastname, firstname)
        )
        if player_ids.empty:
            player_ids = (
                playerid_lookup(self.get_modified_lastname(lastname))
                if firstname is None
                else playerid_lookup(self.get_modified_lastname(lastname), firstname)
            )

        if player_ids.empty:
            return None

        player_info = []
        for index, row in player_ids.iterrows():
            if row["key_bbref"] == "0" or isnan(float(row["mlb_played_first"])):
                continue

            mlb_played_first = floor(float(row["mlb_played_first"]))
            mlb_played_last = floor(float(row["mlb_played_last"]))
            if target_year is not None and (
                target_year < mlb_played_first or target_year > mlb_played_last
            ):
                continue

            player_info.append(
                {
                    "key_fangraphs": row["key_fangraphs"],
                    "key_mlbam": row["key_mlbam"],
                    "key_bbref": row["key_bbref"],
                    "key_lahman": row["key_bbref"],
                    "key_fangraphs": row["key_fangraphs"],
                    "name_first": row["name_first"],
                    "name_last": row["name_last"],
                    "mlb_played_first": floor(float(row["mlb_played_first"])),
                    "mlb_played_last": floor(float(row["mlb_played_last"])),
                    "position": self.get_player_position(row["key_bbref"]),
                }
            )

        return player_info

    def get_player_position(self, lahman_id):
        """Get the player's position from the Lahman database."""
        # if self.lahman_data is None:
        #    return None

        player = self.fielding.query(f'playerID == "{lahman_id}"')
        if player.empty:
            return None

        return player["POS"].iloc[0]

    def get_modified_lastname(self, name):
        """Get the player's last name."""
        name = name.lower()
        for shorthand in player_shorthands:
            name = name.replace(shorthand, "")
        return name.strip()

    def create_player_from_info(self, player_info, max_endyear=None):
        player = Players()
        player.firstname = string.capwords(player_info["name_first"])
        player.lastname = string.capwords(player_info["name_last"])
        player.displayname = (
            f"{unidecode(player.firstname)} {unidecode(player.lastname)}"
        )
        player.startyear = player_info["mlb_played_first"]

        if max_endyear is not None and player_info["mlb_played_last"] > int(
            max_endyear
        ):
            player.endyear = int(max_endyear)
        else:
            player.endyear = player_info["mlb_played_last"]

        player.bbrefid = player_info["key_bbref"]
        player.fangraphsid = player_info["key_fangraphs"]
        player.position = player_info["position"]

        player.save()

        logging.info(f"Created player {player.displayname} ({player.bbrefid})")
        return player

    def check_for_player_sync(self, player, target_name):
        player_info = self.get_player_info(target_name)
        result = None
        if player_info:
            for possible_player in player_info:
                if possible_player["key_bbref"] == player.bbrefid:
                    result = {}
                    result[
                        "full_bbref"
                    ] = f'https://www.baseball-reference.com/players/{possible_player["key_bbref"][0]}/{possible_player["key_bbref"]}.shtml'
                    result["start_year"] = possible_player["mlb_played_first"]
                    result["end_year"] = possible_player["mlb_played_last"]
                    result["first_name"] = string.capwords(
                        possible_player["name_first"]
                    )
                    result["last_name"] = string.capwords(possible_player["name_last"])
                    result["bbrefid"] = possible_player["key_bbref"]
                    result["fangraphsid"] = possible_player["key_fangraphs"]
                    result["rotowireid"] = possible_player["key_fangraphs"]
                    result["position"] = self.get_player_position(
                        possible_player["key_lahman"]
                    )

                    # print (f'Found player {result["first_name"]} {result["last_name"]} {result["position"]}...')
                    player_found = True
                    break
        return result

    def process_batting_statsrecords(self, stat_records):
        batting_records = []

        for record in stat_records:

            if (record["bat_ab"] + record["bat_walks"] + record["bat_hbp"]) == 0:
                continue

            record["AVG"] = (
                f'{(record["bat_hits"] / record["bat_ab"]):.3f}'
                if record["bat_ab"] > 0
                else "0.000"
            )
            record[
                "OBP"
            ] = f'{((record["bat_hits"] + record["bat_walks"] + record["bat_hbp"]) / (record["bat_ab"] + record["bat_walks"] + record["bat_hbp"])):.3f}'
            record["SLUG"] = (
                f'{(record["bat_hits"] + record["bat_doubles"] + (record["bat_triples"] * 2) + (record["bat_hr"] * 3)) / record["bat_ab"]:.3f}'
                if record["bat_ab"] > 0
                else "0.000"
            )

            batting_records.append(record)

        return batting_records
    
    def process_pitching_statsrecords(self, stat_records):
        pitching_records = []

        for record in stat_records:
            if record["pitch_ipfull"]  == 0:
                continue

            record["ERA"] = (
                f'{( (record["pitch_er"]*9) / record["pitch_ipfull"]):.2f}'
                if record["pitch_ipfull"] > 0
                else "0.00"
            )
 
            pitching_records.append(record)

        return pitching_records

    def get_all_batting_seasons(self, max_season=9999):
        stat_records = (
            Statrecords.objects.all()
            .filter(season__lte=max_season)
            .order_by("playerid__lastname", "playerid__firstname", "season")
            .select_related("players")
            .select_related("teams")
            .values(
                "playerid__lastname",
                "playerid__firstname",
                "season",
                "teamid__city",
                "games",
                "bat_ab",
                "bat_hits",
                "bat_rbi",
                "bat_runs",
                "bat_doubles",
                "bat_triples",
                "bat_hr",
                "bat_walks",
                "bat_strikeouts",
                "bat_sb",
                "bat_cs",
                "errors",
                "bat_hbp",
            )
        )

        return self.process_batting_statsrecords(stat_records)

    def get_all_batting_careers(self, max_season=9999):
        stat_records = (
            Players.objects.filter(statrecords__games__gt=0)
            .filter(statrecords__season__lte=max_season)
            .annotate(
                games=Sum("statrecords__games", distinct=True),
                bat_ab=Sum("statrecords__bat_ab", distinct=True),
                bat_hits=Sum("statrecords__bat_hits", distinct=True),
                bat_rbi=Sum("statrecords__bat_rbi", distinct=True),
                bat_runs=Sum("statrecords__bat_runs",  distinct=True),
                bat_doubles=Sum("statrecords__bat_doubles", distinct=True),
                bat_triples=Sum("statrecords__bat_triples", distinct=True),
                bat_hr=Sum("statrecords__bat_hr", distinct=True),
                bat_walks=Sum("statrecords__bat_walks", distinct=True),
                bat_strikeouts=Sum("statrecords__bat_strikeouts", distinct=True),
                bat_sb=Sum("statrecords__bat_sb", distinct=True),
                bat_cs=Sum("statrecords__bat_cs", distinct=True),
                errors=Sum("statrecords__errors", distinct=True),
                bat_hbp=Sum("statrecords__bat_hbp", distinct=True),
            )
            .values(
                "lastname",
                "firstname",
                "games",
                "bat_ab",
                "bat_hits",
                "bat_rbi",
                "bat_runs",
                "bat_doubles",
                "bat_triples",
                "bat_hr",
                "bat_walks",
                "bat_strikeouts",
                "bat_sb",
                "bat_cs",
                "errors",
                "bat_hbp",
            )
            .order_by("lastname", "firstname")
        )

        return self.process_batting_statsrecords(stat_records)
    
    def get_all_pitching_seasons(self, max_season=9999):
        stat_records = (
            Statrecords.objects.all()
            .filter(season__lte=max_season)
            .order_by("playerid__lastname", "playerid__firstname", "season")
            .select_related("players")
            .select_related("teams")
            .values(
                "playerid__lastname",
                "playerid__firstname",
                "season",
                "teamid__city",
                "pitch_gp",
                "pitch_gs",
                "pitch_cg",
                "pitch_sho",
                "pitch_wins",
                "pitch_loss",
                "pitch_save",
                "pitch_ipfull",
                "pitch_ipfract",
                "pitch_hits",
                "pitch_runs",
                "pitch_er",
                "pitch_hr",
                "pitch_walks",
                "pitch_strikeouts", 
            )
        )

        return self.process_pitching_statsrecords(stat_records)
    
    def get_all_pitching_careers(self, max_season=9999):
        stat_records = (
            Players.objects.filter(statrecords__pitch_gp__gt=0)
            .filter(statrecords__season__lte=max_season)
            .annotate(
                pitch_gp=Sum("statrecords__pitch_gp", distinct=True),
                pitch_gs=Sum("statrecords__pitch_gs",distinct=True ),
                pitch_cg=Sum("statrecords__pitch_cg", distinct=True),
                pitch_sho=Sum("statrecords__pitch_sho", distinct=True),
                pitch_wins=Sum("statrecords__pitch_wins", distinct=True),
                pitch_loss=Sum("statrecords__pitch_loss", distinct=True),
                pitch_save=Sum("statrecords__pitch_save", distinct=True),
                pitch_ipfull=Sum("statrecords__pitch_ipfull", distinct=True),
                pitch_ipfract=Sum("statrecords__pitch_ipfract", distinct=True),
                pitch_hits=Sum("statrecords__pitch_hits", distinct=True),
                pitch_runs=Sum("statrecords__pitch_runs", distinct=True),
                pitch_er=Sum("statrecords__pitch_er", distinct=True),
                pitch_hr=Sum("statrecords__pitch_hr", distinct=True),
                pitch_walks=Sum("statrecords__pitch_walks", distinct=True),
                pitch_strikeouts=Sum("statrecords__pitch_strikeouts", distinct=True),
            )
            .values(
                "lastname",
                "firstname",
                "pitch_gp",
                "pitch_gs",
                "pitch_cg",
                "pitch_sho",
                "pitch_wins",
                "pitch_loss",
                "pitch_save",
                "pitch_ipfull",
                "pitch_ipfract",
                "pitch_hits",
                "pitch_runs",
                "pitch_er",
                "pitch_hr",
                "pitch_walks",
                "pitch_strikeouts", 
            )
            .order_by("lastname", "firstname")
        )

        return self.process_pitching_statsrecords(stat_records)
