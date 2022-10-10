from django.contrib import admin
from .models import *

admin.site.register(SysNationality)
admin.site.register(SysCountries)

class SysParametersAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'type_parameter',
        'value',
        'status',
        'created_at',
        'deleted_at'
    )
    list_per_page = 20
    ordering = ('-created_at',)
    search_fields = ('name','code')
    list_filter = (
        'type_parameter',
        'deleted_at',
    )

admin.site.register(SysParameters,SysParametersAdmin)
