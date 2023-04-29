from django.contrib import admin
from .models import Teamresults, TeamresultsAdmin, Gameresults, GameresultsAdmin

admin.site.register(Teamresults, TeamresultsAdmin)
admin.site.register(Gameresults, GameresultsAdmin)
