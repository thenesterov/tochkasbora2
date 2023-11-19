from django.contrib import admin

from interest.models import Interest


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    pass
