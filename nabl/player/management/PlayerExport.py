import argparse
import csv
import logging
from player.management import PlayerManager

manager = PlayerManager()

batter_stats_columns = {
    "games": "Games",
    "bat_ab": "AB",
    "bat_hits": "Hits",
    "bat_runs": "Runs",
    "bat_rbi": "RBI",
    "bat_runs": "Runs",
    "bat_doubles": "2B",
    "bat_triples": "3B",
    "bat_hr": "HR",
    "bat_walks": "BB",
    "bat_strikeouts": "SO",
    "bat_sb": "SB",
    "bat_cs": "CS",
    "errors": "Errors",
    "bat_hbp": "HBP",
    "AVG": "AVG",
    "OBP": "OBP",
    "SLUG": "SLG",
}

pitcher_stats_columns = {
                "pitch_gp" : "GP",
                "pitch_gs" : "GS",
                "pitch_cg" : "CG",
                "pitch_sho": "SHO",
                "pitch_wins" : "Win",
                "pitch_loss" : "Loss",
                "pitch_save" : "Save",
                "pitch_ipfull" : "IP",
                "pitch_hits" : "Hits",
                "pitch_runs" : "Runs",
                "pitch_er" : "ER",
                "pitch_hr" : "HR",
                "pitch_walks": "BB",
                "pitch_strikeouts": "SO",
                "ERA": "ERA",
}

batter_single_season_columns = {
    **{"playerid__lastname": "Lastname",
    "playerid__firstname": "Firstname",
    "season": "Year",
    "teamid__city": "Team"}, **batter_stats_columns
}

batter_career_columns = { **{
    "lastname": "Lastname",
    "firstname": "Firstname"}, **batter_stats_columns
}

pitcher_single_season_columns = {
    **{"playerid__lastname": "Lastname",
    "playerid__firstname": "Firstname",
    "season": "Year",
    "teamid__city" : "Team"}, **pitcher_stats_columns
}

pitcher_career_columns = { **{
    "lastname": "Lastname",
    "firstname": "Firstname"}, **pitcher_stats_columns
}

batter_base_ordered_columns = [
    "games",
    "bat_ab",
    "bat_hits",
    "bat_doubles",
    "bat_triples",
    "bat_hr",
    "bat_runs",
    "bat_rbi",
    "bat_walks",
    "bat_strikeouts",
    "bat_sb",
    "bat_cs",
    "errors",
    "bat_hbp",
    "AVG",
    "OBP",
    "SLUG",
]

pitcher_base_ordered_columns = [
    "pitch_gp",
    "pitch_gs",
    "pitch_cg",
    "pitch_sho",
    "pitch_wins",
    "pitch_loss",
    "pitch_save",
    "pitch_ipfull",
    "pitch_hits",
    "pitch_runs",
    "pitch_er",
    "pitch_hr",
    "pitch_walks",
    "pitch_strikeouts",
    "ERA"
]

batter_season_ordered_columns = ["playerid__lastname","playerid__firstname", "season", "teamid__city"] + batter_base_ordered_columns
batter_career_ordered_columns = ["lastname","firstname",] + batter_base_ordered_columns

pitcher_season_ordered_columns = ["playerid__lastname","playerid__firstname", "season", "teamid__city"] + pitcher_base_ordered_columns
pitcher_career_ordered_columns = ["lastname","firstname",] + pitcher_base_ordered_columns

batter_new_season_cols = [batter_single_season_columns.get(x, x) for x in batter_season_ordered_columns]
batter_new_career_cols = [batter_career_columns.get(x, x) for x in batter_career_ordered_columns]

pitcher_new_season_cols = [pitcher_single_season_columns.get(x, x) for x in pitcher_season_ordered_columns]
pitcher_new_career_cols = [pitcher_career_columns.get(x, x) for x in pitcher_career_ordered_columns]


def export_batting_seasons(directory, max_season):
    file = f"{directory}/batting_seasons.csv"
    with open(file, "w") as csvfile:
        batting_records = manager.get_all_batting_seasons(max_season=max_season)
        logging.info(f"writing {len(batting_records)} batting season records to {file}")
        fieldnames = batting_records[0].keys()
        writer = csv.writer(csvfile)
        writer.writerow(batter_new_season_cols)
        for record in batting_records:
            writer.writerow([record.get(x) for x in batter_season_ordered_columns])


def export_batting_careers(directory, max_season):
    file = f"{directory}/batting_careers.csv"
    with open(file, "w") as csvfile:
        batting_records = manager.get_all_batting_careers(max_season=max_season)
        logging.info(f"writing {len(batting_records)} batting career records to {file}")
        fieldnames = batting_records[0].keys()
        writer = csv.writer(csvfile)
        writer.writerow(batter_new_career_cols)
        for record in batting_records:
            writer.writerow([record.get(x) for x in batter_career_ordered_columns])

def export_pitching_seasons(directory, max_season):
    file = f"{directory}/pitching_seasons.csv"
    with open(file, "w") as csvfile:
        pitching_records = manager.get_all_pitching_seasons(max_season=max_season)
        logging.info(f"writing {len(pitching_records)} pitching season records to {file}")
        fieldnames = pitching_records[0].keys()
        writer = csv.writer(csvfile)
        writer.writerow(pitcher_new_season_cols)
        for record in pitching_records:
            writer.writerow([record.get(x) for x in pitcher_season_ordered_columns])


def export_pitching_careers(directory, max_season):
    file = f"{directory}/pitching_careers.csv"
    with open(file, "w") as csvfile:
        pitching_records = manager.get_all_pitching_careers(max_season=max_season)
        logging.info(f"writing {len(pitching_records)} pitching career records to {file}")
        fieldnames = pitching_records[0].keys()
        writer = csv.writer(csvfile)
        writer.writerow(pitcher_new_career_cols)
        for record in pitching_records:
            writer.writerow([record.get(x) for x in pitcher_career_ordered_columns])



def main():
    manager = PlayerManager()

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="Validate database against league excel file"
    )
    parser.add_argument("--directory", "-d", required=True, help="The directory to output files")
    parser.add_argument("--maxseason", "-m", required=False, default=9999, help="The maximum season to export")

    args = parser.parse_args()

    export_pitching_seasons(args.directory, args.maxseason)
    export_pitching_careers(args.directory, args.maxseason)
    export_batting_seasons(args.directory, args.maxseason)
    export_batting_careers(args.directory, args.maxseason)
    


if __name__ == "__main__":
    main()