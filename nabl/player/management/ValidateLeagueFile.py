import xlrd
import logging
import argparse
from league.models import Teams
from player.models import Players
from player.models import Rosterassign
from player.models import CardedPlayers

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def getTeamByCity(cityName):
    return Teams.objects.get(city__exact=cityName)


def getPlayerByDisplayName(displayName, yearactive):
    return Players.objects.get(displayname__exact=displayName, endyear__gte=yearactive)


def getPlayerByFullName(firstname, lastname, yearactive):
    return Players.objects.get(
        firstname__exact=firstname, lastname__exact=lastname, endyear__gte=yearactive
    )


def getRosterAssignment(player, season):
    return Rosterassign.objects.get(playerid=player.id, year=season)


def getCardedPlayer(name, cardedyear):
    return CardedPlayers.objects.get(playername=name, season=cardedyear)


def loadMasterFile(filename):
    return xlrd.open_workbook(filename)


def getTeamList(xl_file):
    sh = xl_file.sheet_by_name("Rosters and available players")
    teams = {}

    for rownum in range(3, sh.nrows):
        row = sh.row_values(rownum)
        teamname = row[4]

        # logging.info(f"getting team {teamname}")

        if teamname and "zz" not in teamname.lower():
            try:
                nablTeam = getTeamByCity(teamname)
                if nablTeam:
                    teams[teamname] = nablTeam
                else:
                    logging.info(f"cannot find team for {teamname}")
            except ObjectDoesNotExist:
                logging.error(f"cannot find team for {teamname}")

    return teams


def getPlayer(firstname, lastname, minYear):
    player = None
    try:
        player = getPlayerByDisplayName(firstname + " " + lastname, minYear)
        return player
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        try:
            player = getPlayerByFullName(firstname, lastname, minYear)
            return player
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            return None


def validatePlayersInFile(xl_file, rosterYear, cardedYear, minYear):
    count = 0
    sh = xl_file.sheet_by_name("Rosters and available players")
    teams = getTeamList(xl_file)

    for rownum in range(3, 1001):
        row = sh.row_values(rownum)

        lastname = row[1].strip()
        firstname = row[2].strip()
        mlbteam = row[3].strip()
        team = row[4].strip()

        if firstname == "" or lastname == "":
            continue

        logging.info(f"Validating player {firstname} {lastname}")
        player = getPlayer(firstname, lastname, minYear)

        if player:
            count = count + 1

            # make sure that he site has the same assignment as the sheet
            if team and team in teams:
                try:
                    assignment = getRosterAssignment(player, rosterYear)
                    if assignment.teamid.id != teams[team].id:
                        logging.error(
                            f"{firstname} {lastname} assigned to {team} in file but on site is {assignment.teamid.city}"
                        )
                except ObjectDoesNotExist:
                    logging.error(
                        f"{firstname} {lastname} assigned to {team} in file is not assigned on site"
                    )
                except MultipleObjectsReturned:
                    logging.error(
                        f"{firstname} {lastname} assigned to multiple teams on site"
                    )
            # make sure the site also does not have this player assigned
            else:
                try:
                    assignment = getRosterAssignment(player, rosterYear)
                    logging.error(
                        f"{firstname} {lastname} not assigned in file is assigned on site to {assignment.teamid.city}"
                    )
                except ObjectDoesNotExist:
                    pass

            if mlbteam != "unc":
                try:
                    getCardedPlayer(player.displayname, cardedYear)
                except ObjectDoesNotExist:
                    logging.error(
                        f'cannot find card for  player: {firstname}"# #{lastname}#'
                    )
            else:
                try:
                    getCardedPlayer(f"{player.firstname} {player.lastname}", cardedYear)
                    logging.info(
                        f"showing card for unc  player: #{firstname}# #{lastname}#"
                    )
                except ObjectDoesNotExist:
                    pass

        else:
            logging.error(f"cannot find player: #{firstname}# #{lastname}#")

    logging.info(f"successful count: {str(count)}")


def main():
    logging.basicConfig(level=logging.ERROR)

    parser = argparse.ArgumentParser(
        description="Validate database against league excel file"
    )
    parser.add_argument("--filename", "-f", required=True, help="The master excel file")
    parser.add_argument(
        "--season", "-s", required=True, help="The NABL season to validate"
    )
    parser.add_argument(
        "--cardedseason", "-c", required=True, help="The APBA carded season to use"
    )
    parser.add_argument(
        "--minseason",
        "-m",
        required=True,
        help="The earliest MLB season to use for players",
    )

    args = parser.parse_args()
    xl_file = loadMasterFile(args.filename)
    validatePlayersInFile(xl_file, args.season, args.cardedseason, args.minseason)


if __name__ == "__main__":
    main()
