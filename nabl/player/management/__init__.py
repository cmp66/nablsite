from math import floor, isnan
from unidecode import unidecode
from pybaseball import playerid_lookup
from pybaseball import lahman
import logging
import os
import string
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nabl.settings")
django.setup()

from django.db.models import F  # noqa: E402
from django.db import connection  # noqa: E402
from player.models import Players  # noqa: E402
from stats.models import Statrecords  # noqa: E402

player_shorthands = ["jr.", "sr.", "ii", "iii", "iv", "Jr.", "Sr.", "II", "III", "IV"]


class PlayerManager:
    def __init__(self, load_lahman=False):
        self.lahman_data = lahman.download_lahman() if load_lahman else None
        self.people = lahman.people() if load_lahman else None
        self.batting = lahman.batting() if load_lahman else None
        self.fielding = lahman.fielding() if load_lahman else None

        if load_lahman:
            self.batting.to_csv("temp/batting.csv")
            # people.to_csv('temp/people.csv')
            # fielding.to_csv('temp/fielding.csv')

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

    def get_player_batting(self, lahman_id):
        if self.lahman_data is None:
            return None
        player = self.batting.query(f'playerID == "{lahman_id}"')
        if player.empty:
            return None

        return player

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

                    # pprint (f'Found player {result["first_name"]} {result["last_name"]} {result["position"]}...')
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
            if record["stat_pitch_ipfull"] == 0:
                continue

            record["ERA"] = (
                f'{( (record["stat_pitch_er"]*9) / record["stat_pitch_ipfull"]):.2f}'
                if record["stat_pitch_ipfull"] > 0
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
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    players.lastname as playerid__lastname,
                    players.firstname as playerid__firstname,
                    statrecords.games,
                    statrecords.bat_ab,
                    statrecords.bat_hits,
                    statrecords.bat_rbi,
                    statrecords.bat_runs,
                    statrecords.bat_doubles,
                    statrecords.bat_triples,
                    statrecords.bat_hr,
                    statrecords.bat_walks,
                    statrecords.bat_strikeouts,
                    statrecords.bat_sb,
                    statrecords.bat_cs,
                    statrecords.errors,
                    statrecords.bat_hbp
                FROM players
                INNER JOIN (
                    SELECT
                        playerid,
                        SUM(games) AS games,
                        SUM(bat_ab) AS bat_ab,
                        SUM(bat_hits) AS bat_hits,
                        SUM(bat_rbi) AS bat_rbi,
                        SUM(bat_runs) AS bat_runs,
                        SUM(bat_doubles) AS bat_doubles,
                        SUM(bat_triples) AS bat_triples,
                        SUM(bat_hr) AS bat_hr,
                        SUM(bat_walks) AS bat_walks,
                        SUM(bat_strikeouts) AS bat_strikeouts,
                        SUM(bat_sb) AS bat_sb,
                        SUM(bat_cs) AS bat_cs,
                        SUM(errors) AS errors,
                        SUM(bat_hbp) AS bat_hbp
                    FROM
                        statrecords
                    WHERE
                        season <= %s
                    GROUP BY
                        statrecords.playerid) statrecords
                ON statrecords.playerid = players.id
                ORDER BY
                    players.lastname, players.firstname
                """,
                [max_season],
            )

            stat_records = self.dictfetchall(cursor)

        return self.process_batting_statsrecords(stat_records)

    def get_all_pitching_seasons(self, max_season=9999):
        stat_records = (
            Statrecords.objects.all()
            .filter(season__lte=max_season)
            .order_by("playerid__lastname", "playerid__firstname", "season")
            .select_related("players")
            .select_related("teams")
            .annotate(
                stat_pitch_gp=F("pitch_gp"),
                stat_pitch_gs=F("pitch_gs"),
                stat_pitch_cg=F("pitch_cg"),
                stat_pitch_sho=F("pitch_sho"),
                stat_pitch_wins=F("pitch_wins"),
                stat_pitch_loss=F("pitch_loss"),
                stat_pitch_save=F("pitch_save"),
                stat_pitch_ipfull=F("pitch_ipfull"),
                stat_pitch_ipfract=F("pitch_ipfract"),
                stat_pitch_hits=F("pitch_hits"),
                stat_pitch_runs=F("pitch_runs"),
                stat_pitch_er=F("pitch_er"),
                stat_pitch_hr=F("pitch_hr"),
                stat_pitch_walks=F("pitch_walks"),
                stat_pitch_strikeouts=F("pitch_strikeouts"),
            )
            .values(
                "playerid__lastname",
                "playerid__firstname",
                "season",
                "teamid__city",
                "stat_pitch_gp",
                "stat_pitch_gs",
                "stat_pitch_cg",
                "stat_pitch_sho",
                "stat_pitch_wins",
                "stat_pitch_loss",
                "stat_pitch_save",
                "stat_pitch_ipfull",
                "stat_pitch_ipfract",
                "stat_pitch_hits",
                "stat_pitch_runs",
                "stat_pitch_er",
                "stat_pitch_hr",
                "stat_pitch_walks",
                "stat_pitch_strikeouts",
            )
        )

        return self.process_pitching_statsrecords(stat_records)

    def dictfetchall(self, cursor):
        """
        Return all rows from a cursor as a dict.
        Assume the column names are unique.
        """
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_all_pitching_careers(self, max_season=9999):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    players.lastname as playerid__lastname,
                    players.firstname as playerid__firstname,
                    statrecords.stat_pitch_gp,
                    statrecords.stat_pitch_gs,
                    statrecords.stat_pitch_cg,
                    statrecords.stat_pitch_sho,
                    statrecords.stat_pitch_wins,
                    statrecords.stat_pitch_loss,
                    statrecords.stat_pitch_save,
                    statrecords.stat_pitch_ipfull,
                    statrecords.stat_pitch_ipfract,
                    statrecords.stat_pitch_hits,
                    statrecords.stat_pitch_runs,
                    statrecords.stat_pitch_er,
                    statrecords.stat_pitch_hr,
                    statrecords.stat_pitch_walks,
                    statrecords.stat_pitch_strikeouts
                FROM players
                INNER JOIN (
                    SELECT
                        playerid,
                        SUM(pitch_gp) AS stat_pitch_gp,
                        SUM(pitch_gs) AS stat_pitch_gs,
                        SUM(pitch_cg) AS stat_pitch_cg,
                        SUM(pitch_sho) AS stat_pitch_sho,
                        SUM(pitch_wins) AS stat_pitch_wins,
                        SUM(pitch_loss) AS stat_pitch_loss,
                        SUM(pitch_save) AS stat_pitch_save,
                        SUM(pitch_ipfull) AS stat_pitch_ipfull,
                        SUM(pitch_ipfract) AS stat_pitch_ipfract,
                        SUM(pitch_hits) AS stat_pitch_hits,
                        SUM(pitch_runs) AS stat_pitch_runs,
                        SUM(pitch_er) AS stat_pitch_er,
                        SUM(pitch_hr) AS stat_pitch_hr,
                        SUM(pitch_walks) AS stat_pitch_walks,
                        SUM(pitch_strikeouts) AS stat_pitch_strikeouts
                    FROM
                        statrecords
                    WHERE
                        pitch_gp > 0 AND season <= %s
                    GROUP BY
                        statrecords.playerid) statrecords
                ON statrecords.playerid = players.id
                ORDER BY
                    players.lastname, players.firstname
                """,
                [max_season],
            )

            stat_records = self.dictfetchall(cursor)

        return self.process_pitching_statsrecords(stat_records)
