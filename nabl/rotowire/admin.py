from django.contrib import admin
from .models import Rotowire, Rotowiremissing, RotowireAdmin, RotowiremissingAdmin

admin.site.register(Rotowire, RotowireAdmin)
admin.site.register(Rotowiremissing, RotowiremissingAdmin)
