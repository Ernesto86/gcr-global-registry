from django.contrib import admin
from .models import *

admin.site.register(SysCountries)
admin.site.register(AcademicLevel)

class SysParametersAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'value',
        'status',
        'created_at',
        'deleted_at'
    )
    list_per_page = 20
    ordering = ('-created_at',)
    search_fields = ('name','code')
    list_filter = (
        'deleted_at',
    )

admin.site.register(SysParameters,SysParametersAdmin)
