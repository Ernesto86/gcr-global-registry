from django.contrib import admin
from .models import *

class StudentsAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'code',
        'names',
        'dni',
        'gender',
        'country',
        'telephone',
        'created_at',
        'estado'
    )
    list_per_page = 20
    ordering = ('-created_at',)
    search_fields = ('code','dni', 'name')
    list_filter = (
        'country',
        'gender',
        'deleted'
    )

    def estado(self, obj):
        return not obj.deleted
    estado.boolean = True


admin.site.register(Students,StudentsAdmin)
admin.site.register(Certificates)


class StudentRegistersAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'student',
        'type_register',
        'country',
        'date_issue',
        'code_international_register',
        'created_at',
        'deleted_at'
    )
    list_per_page = 20
    ordering = ('-created_at',)
    search_fields = ('number', 'student')
    list_filter = (
        'institution',
        'country',
        'type_register',
        'deleted'
    )


admin.site.register(StudentRegisters,StudentRegistersAdmin)
