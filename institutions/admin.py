from django.contrib import admin
from .models import *

class InsTypeRegistriesAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'status'
    )
    list_per_page = 20
    ordering = ('-created_at',)
    search_fields = ('code','name')
    list_filter = (
        'deleted',
    )
    def status(self, obj):
        return not obj.deleted
    status.boolean = True

admin.site.register(InsTypeRegistries,InsTypeRegistriesAdmin)

class InstitutionsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'identification',
        'representative',
        'country',
        'type_registration',
        'telephone',
        'created_at',
        'status'
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
    def status(self, obj):
        return not obj.deleted
    status.boolean = True

admin.site.register(Institutions,InstitutionsAdmin)
