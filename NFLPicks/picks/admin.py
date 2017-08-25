from django.contrib import admin
from .models import *

class GameInline(admin.TabularInline):
    model = Game

class WeekAdmin(admin.ModelAdmin):
    model = Week
    list_display = ['year', 'week']
    inlines = [GameInline]

class TeamsAdmin(admin.ModelAdmin):
    model = Team
    list_display = ['team_name', 'team_abbrev']

class PlayerPicksAdmin(admin.ModelAdmin):
    model = PlayerPick
    list_display = ['user', 'game', 'pick']

# Register your models here.
admin.site.register(Week, WeekAdmin)
admin.site.register(Team, TeamsAdmin)
admin.site.register(PlayerPick, PlayerPicksAdmin)