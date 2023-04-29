import argparse
import logging

from league.management import LeagueManager



def main():

    logging.basicConfig(level=logging.INFO)
    manager = LeagueManager()

    parser = argparse.ArgumentParser(description='Import carded players')
    parser.add_argument('--new-season', '-n', required=True, help='The new season to create')
    parser.add_argument('--existing-season', '-e', required=True, help='The new season to create')
    

    args = parser.parse_args()

    manager.migrate_team_results(args.new_season, args.existing_season)
    manager.migrate_rosters_assigns(args.new_season, args.existing_season)
    manager.migrate_schedules(args.new_season, args.existing_season)



if __name__ == "__main__":
    main()