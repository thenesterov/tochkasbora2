from django.contrib import admin

from event.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
