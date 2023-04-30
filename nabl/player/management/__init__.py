from math import floor, isnan
from unidecode import unidecode

import logging
import os
import string
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nabl.settings")
django.setup()


from pybaseball import playerid_lookup, batting_stats
from pybaseball import lahman

from player.models import Players

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

    def search_for_player_by_fullname(self, fullname, target_year=2000):
        # first search for the player in our database
        players = (
            Players.objects.filter(displayname=fullname)
            .filter(start_year__lte=target_year)
            .filter(end_year__gte=target_year)
        )

        if players.count() > 0:
            return players[0]

        player_data = self.check_for_player(player, player.lastname)

        if not player_data:
            player_data = self.check_for_player(
                player, player.displayname.split(maxsplit=3)[-1]
            )

        if not player_data:
            player_data = self.check_for_player(
                player,
                f"{player.displayname.split(maxsplit=2)[-2]} {player.displayname.split(maxsplit=2)[-1]}",
            )

        return player_data
