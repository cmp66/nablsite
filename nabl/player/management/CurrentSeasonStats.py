from player.management import PlayerManager
from player.models import Players, Rosterassign, CardedPlayers
import csv

manager = PlayerManager(load_lahman=False)

assigned_players = Rosterassign.objects.all().filter(year=2023)
carded_players = CardedPlayers.objects.all().filter(season=2022)
unassigned_players = (
    Players.objects.all()
    .filter(
        id__in=CardedPlayers.objects.all()
        .filter(season=2022)
        .values_list("playerid", flat=True)
    )
    .exclude(
        id__in=Rosterassign.objects.all()
        .filter(year=2023)
        .values_list("playerid", flat=True)
    )
)

batting_data = {}
pitching_data = {}
filtered_batting_data = {}
filtered_pitching_data = {}
with open("files/stats/batting_2022.csv", encoding="utf-8-sig") as csvfile:
    csvReader = csv.DictReader(csvfile)
    for rows in csvReader:
        key = rows["Name"]
        batting_data[key] = rows

with open("files/stats/pitching_2022.csv", encoding="utf-8-sig") as csvfile:
    csvReader = csv.DictReader(csvfile)
    for rows in csvReader:
        key = rows["Name"]
        pitching_data[key] = rows

for player in unassigned_players:
    if player.displayname in batting_data:
        filtered_batting_data[player.displayname] = batting_data[player.displayname]
    elif f"{player.firstname} {player.lastname}" in batting_data:
        filtered_batting_data[f"{player.firstname} {player.lastname}"] = batting_data[
            f"{player.firstname} {player.lastname}"
        ]

    if player.displayname in pitching_data:
        filtered_pitching_data[player.displayname] = pitching_data[player.displayname]
    elif f"{player.firstname} {player.lastname}" in pitching_data:
        filtered_pitching_data[f"{player.firstname} {player.lastname}"] = pitching_data[
            f"{player.firstname} {player.lastname}"
        ]

with open(
    "files/stats/filtered_batting_2022.csv", "w", encoding="utf-8-sig"
) as csvfile:
    csvWriter = csv.DictWriter(
        csvfile, fieldnames=list(batting_data.values())[0].keys()
    )
    csvWriter.writeheader()

    for player in filtered_batting_data:
        csvWriter.writerow(filtered_batting_data[player])

with open(
    "files/stats/filtered_pitching_2022.csv", "w", encoding="utf-8-sig"
) as csvfile:
    csvWriter = csv.DictWriter(
        csvfile, fieldnames=list(pitching_data.values())[0].keys()
    )
    csvWriter.writeheader()

    for player in filtered_pitching_data:
        csvWriter.writerow(filtered_pitching_data[player])
