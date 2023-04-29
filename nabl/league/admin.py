from django.contrib import admin
from .models import Members, Teams, Leagues, Divisions
from .models import  MembersAdmin, TeamsAdmin, LeaguesAdmin, DivisionsAdmin
from .models import Schedules, SchedulesAdmin
from .models import Idgen, IdgenAdmin

admin.site.register(Members, MembersAdmin)
admin.site.register(Teams, TeamsAdmin)
admin.site.register(Leagues, LeaguesAdmin)
admin.site.register(Divisions, DivisionsAdmin)
admin.site.register(Schedules, SchedulesAdmin)
admin.site.register(Idgen, IdgenAdmin)
