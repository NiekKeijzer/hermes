from django.contrib import admin

from .models import FormMailSettings


# Register your models here.
@admin.register(FormMailSettings)
class FormMailSettingsAdmin(admin.ModelAdmin):
    pass
