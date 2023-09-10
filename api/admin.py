from django.contrib import admin
from .models import SafetyObject


class SafetyObjectAdmin(admin.ModelAdmin):
    list_display = (
        'naziv_objekta',
        'lucka_kapetanija',
        'lokacija'
    )

    ordering = ('naziv_objekta', )


admin.site.register(SafetyObject, SafetyObjectAdmin)
