from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from game_modes.models import AreaCode, GameMode, UserPreference


class UserPreferenceAdmin(admin.ModelAdmin):
    search_fields = ["gamer__username", "area_code__area_code", "game_mode__name"]
    list_display = ["gamer", "area_code", "game_mode", "is_current_preference"]
    list_filter = ["area_code", "game_mode", "is_current_preference"]
    autocomplete_fields = ["gamer", "area_code", "game_mode"]


class AreaCodeAdmin(admin.ModelAdmin):
    search_fields = ["area_code"]
    list_display = ["area_code"]


class GameModeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]


admin.site.register(AreaCode, AreaCodeAdmin)
admin.site.register(GameMode, GameModeAdmin)
admin.site.register(UserPreference, UserPreferenceAdmin)


admin.site.unregister(Group)
admin.site.unregister(TokenProxy)


AdminSite.site_header = "LILA Gaming Admin"
AdminSite.site_title = "LILA Gaming Admin"
AdminSite.site_url = None
AdminSite.index_title = "LILA Gaming Administration"
