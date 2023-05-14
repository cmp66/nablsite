import argparse
import csv
import logging
import pprint
from tabulate import tabulate
from player.management import PlayerManager
from player.models import Players, CardedPlayers

manager = PlayerManager(load_lahman=True)
action = "plan"


def check_for_displayname(display_name, season):
    player = (
        Players.objects.filter(displayname=display_name)
        .filter(startyear__lte=season)
        .filter(endyear__gte=season)
    )

    if player.count() == 1:
        return player[0]

    return None


def check_if_exists(plan):
    player = Players.objects.filter(bbrefid=plan["key_bbref"])
    if player.count() == 1:
        new
        return True

    return False


def process_row(team, display_name, carded_season, create_carded_player=False):
    player = (
        Players.objects.filter(displayname=display_name)
        .filter(startyear__lte=carded_season)
        .filter(endyear__gte=carded_season)
    )

    if player.count() == 1:
        if create_carded_player:
            existing_card = CardedPlayers.objects.filter(playerid=player[0]).filter(
                season=carded_season
            )
            if not existing_card:
                new_card = CardedPlayers()
                new_card.playername = player[0].displayname
                new_card.season = carded_season
                new_card.playerid = player[0]
                new_card.mlbteam = team
                new_card.save()
                logging.info(
                    f"Created carded player {new_card.playername} for {new_card.season}"
                )
        return

    player_info = manager.get_player_info(
        display_name.split(maxsplit=1)[1],
        firstname=display_name.split(maxsplit=1)[0],
        target_year=carded_season,
    )

    if player_info and len(player_info) == 1:
        return player_info[0]

    logging.info(f"No player found for {display_name} {carded_season}")

    return


def main():
    parser = argparse.ArgumentParser(description="Import carded players")
    parser.add_argument(
        "--filename", "-f", required=True, help="The carded players file"
    )
    parser.add_argument(
        "--season", "-s", required=True, help="The season the players were carded"
    )
    parser.add_argument(
        "--debug", "-d", action="store_true", help="Enable debug logging"
    )
    parser.add_argument(
        "--action",
        "-a",
        default="plan",
        choices=["plan", "create-new", "import", "validate"],
        help="Action to take (plan, update, etc.",
    )

    args = parser.parse_args()

    carded_filename = args.filename
    carded_season = int(args.season)
    debug = args.debug
    action = args.action

    logging.basicConfig(level=logging.INFO)

    logging.info(
        f"Processing carded players from {carded_filename} for season {carded_season}"
    )
    logging.info(f"Action: {action}")

    plans = []

    with open(carded_filename, "r") as cardfile:
        reader = csv.reader(cardfile)

        for row in reader:
            if action == "validate":
                carded_player = CardedPlayers.objects.filter(playername=row[1]).filter(
                    season=carded_season
                )
                if not carded_player:
                    logging.error(f"No carded player found for {row[1]}")
            else:
                create_carded_player = True if action == "import" else False
                plan = process_row(
                    row[0],
                    row[1],
                    carded_season,
                    create_carded_player=create_carded_player,
                )

                if plan:
                    if action == "plan":
                        plan["action"] = "FIX" if check_if_exists(plan) else "CREATE"
                        plans.append(plan)
                    elif action == "create-new":
                        if not check_if_exists(plan):
                            manager.create_player_from_info(plan, args.season)
                        else:
                            logging.error(
                                f'Player {plan["displayname"]} already exists'
                            )

    pprint(tabulate(plans, headers="keys", tablefmt="psql"))


if __name__ == "__main__":
    main()
