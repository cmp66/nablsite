from django.contrib import admin
from .models import Transactions, Players, TransactionsAdmin, PlayersAdmin
from .models import Rosterassign, Rostermove, RosterassignAdmin, RostermoveAdmin
from .models import CardedPlayers, CardedPlayersAdmin

admin.site.register(Transactions, TransactionsAdmin)
admin.site.register(Players, PlayersAdmin)
admin.site.register(Rosterassign, RosterassignAdmin)
admin.site.register(Rostermove, RostermoveAdmin)
admin.site.register(CardedPlayers, CardedPlayersAdmin)

