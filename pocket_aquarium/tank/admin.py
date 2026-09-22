from django.contrib import admin

from .models import Fish


@admin.register(Fish)
class FishAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "size", "speed", "meals", "created_at")
