from django.contrib import admin
from f1web.championship.models import Championship, Race, Driver, Team, DriverTeamAssignment, RaceResult, RaceResultPosition

class RaceAdmin(admin.ModelAdmin):
    list_display = ('championship', 'code', 'name', 'date')

class DriverTeamAssignmentInline(admin.TabularInline):
    model = DriverTeamAssignment

class DriverAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    inlines = (DriverTeamAssignmentInline,)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

class RaceResultPositionInline(admin.TabularInline):
    model = RaceResultPosition
    extra = 10

class RaceResultAdmin(admin.ModelAdmin):
    inlines = (RaceResultPositionInline,)

admin.site.register(Championship)
admin.site.register(Race, RaceAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(RaceResult, RaceResultAdmin)
