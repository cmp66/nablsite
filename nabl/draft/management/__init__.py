import logging
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nabl.settings")
django.setup()
from draft.models import Draftpicks  # noqa: E402


class DraftManager:
    def migration_draft_picks(self, newseason, oldseason):
        old_draft_picks = Draftpicks.objects.filter(draftyear=oldseason)

        for old_draft_pick in old_draft_picks:
            existing_pick = Draftpicks.objects.filter(
                draftyear=newseason,
                slotteam=old_draft_pick.slotteam,
                ownerteam=old_draft_pick.slotteam,
                round=old_draft_pick.round,
            )

            if not existing_pick:
                new_draft_pick = Draftpicks()
                new_draft_pick.draftyear = newseason
                new_draft_pick.slotteam = old_draft_pick.slotteam
                new_draft_pick.ownerteam = old_draft_pick.slotteam
                new_draft_pick.playerid = None
                new_draft_pick.round = old_draft_pick.round
                new_draft_pick.save()
                logging.info(f"Migrated {new_draft_pick}")
            else:
                logging.info(f"Draft Pick exists: {existing_pick[0]}")
