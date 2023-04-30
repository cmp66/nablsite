from django.contrib import admin
from .models import Draftpicks, DraftpicksAdmin, DraftorderAdmin, Draftorder

admin.site.register(Draftpicks, DraftpicksAdmin)
admin.site.register(Draftorder, DraftorderAdmin)
