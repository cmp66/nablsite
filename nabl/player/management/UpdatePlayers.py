from player.management import PlayerManager
from player.models import Players


def update_player(player, player_data):
    if player_data["end_year"] == 2023 and player_data["start_year"] <= 2022:
        player.endyear = 2022
    else:
        player.endyear = player_data["end_year"]
    player.startyear = player_data["start_year"]
    player.firstname = player_data["first_name"]
    player.lastname = player_data["last_name"]
    player.bbrefid = player_data["bbrefid"]
    player.fangraphsid = player_data["fangraphsid"]
    player.rotowireid = player_data["rotowireid"]
    player.position = player_data["position"]
    player.save()


manager = PlayerManager(load_lahman=True)

players = Players.objects.filter(displayname="Lourdes Gurriel Jr.")
# players = Players.objects.all()


for player in players:
    # print (f'Looking player {player.firstname} {player.lastname}...')
    # player_info = manager.get_player_info(player.firstname, player.lastname)

    player_data = manager.check_for_player_sync(player, player.lastname)

    if not player_data:
        player_data = manager.check_for_player_sync(
            player, player.displayname.split(maxsplit=3)[-1]
        )

    if not player_data:
        player_data = manager.check_for_player_sync(
            player,
            f"{player.displayname.split(maxsplit=2)[-2]} {player.displayname.split(maxsplit=2)[-1]}",
        )

    if not player_data:
        print(
            f"No player found for {player.firstname} {player.lastname} {player.bbreflink}"
        )
    else:
        update_player(player, player_data)
