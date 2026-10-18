import logging
import argparse
from player.management import PlayerManager
from player.models import Players


def update_player(player, player_data):
    player.endyear = player_data["end_year"]
    player.startyear = player_data["start_year"]
    player.firstname = player_data["first_name"]
    player.lastname = player_data["last_name"]
    player.bbrefid = player_data["bbrefid"]
    player.fangraphsid = player_data["fangraphsid"]
    player.rotowireid = player_data["rotowireid"]
    player.position = player_data["position"]
    player.bbreflink = player_data["full_bbref"]
    print(
        f"Updating {player.displayname} with {player_data['first_name']} {player_data['last_name']} {player_data['start_year']}-{player_data['end_year']} {player_data['position']} {player_data['bbrefid']} {player_data['fangraphsid']} {player_data['rotowireid']}"
    )
    player.save()


manager = PlayerManager()

players = Players.objects.filter(displayname="Riley Greene")
# players = Players.objects.all()


def process_players(minstartyear: int):
    for player in players:
        # print(f"Looking player {player.firstname} {player.lastname}...")
        # player_info = manager.get_player_info(player.firstname, player.lastname)

        if player.startyear <= minstartyear:
            continue

        player_data = manager.check_for_player_sync(
            player, player.lastname, player.bbrefid
        )

        if not player_data:
            player_data = manager.check_for_player_sync(
                player, player.displayname.split(maxsplit=3)[-1], player.bbrefid
            )

        if not player_data:
            player_data = manager.check_for_player_sync(
                player,
                f"{player.displayname.split(maxsplit=2)[-2]} {player.displayname.split(maxsplit=2)[-1]}",
                player.bbrefid,
            )

        if not player_data:
            print(
                f"No player found for {player.firstname} {player.lastname} {player.bbreflink}"
            )
        else:
            update_player(player, player_data)


def main():
    logging.basicConfig(level=logging.ERROR)

    parser = argparse.ArgumentParser(description="Update Player metadata")
    parser.add_argument(
        "--minstartyear", "-ms", required=True, help="the minimul start year to update"
    )
    args = parser.parse_args()
    process_players(int(args.minstartyear))


if __name__ == "__main__":
    main()
