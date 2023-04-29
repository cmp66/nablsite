import logging
import argparse

from draft.management import DraftManager


def main():
    logging.basicConfig(level=logging.INFO)
    manager = DraftManager()

    parser = argparse.ArgumentParser(description="Migrate Draft Picks for a season")
    parser.add_argument(
        "--new-season", "-n", required=True, help="The new season to create"
    )
    parser.add_argument(
        "--existing-season", "-e", required=True, help="The new season to create"
    )

    args = parser.parse_args()

    logging.info(
        f"Migrating draft picks from {args.existing_season} to {args.new_season}"
    )
    manager.migration_draft_picks(int(args.new_season), int(args.existing_season))


if __name__ == "__main__":
    main()
