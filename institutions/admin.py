from django.contrib import admin
from .models import *

class InsTypeRegistriesAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'created_at',
        'deleted_at'
    )
    list_per_page = 20
    ordering = ('-created_at',)
    search_fields = ('code','name')
    list_filter = (
        'type',
        'deleted',
    )

admin.site.register(InsTypeRegistries,InsTypeRegistriesAdmin)

class InstitutionsAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'name',
        'identification',
        'representative',
        'country',
        'type_registration',
        'telephone',
        'created_at',
        'deleted_at'
    )
    list_per_page = 20
    ordering = ('-created_at',)
    search_fields = ('identification', 'name')
    list_filter = (
        'country',
        'type_registration',
        'adviser',
        'deleted'
    )

admin.site.register(Institutions,InstitutionsAdmin)
