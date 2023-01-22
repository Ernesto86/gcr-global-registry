from django.contrib import admin
from .models import *

class StudentsAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'names',
        'dni',
        'gender',
        'country',
        'telephone',
        'created_at',
        'status'
    )
    list_per_page = 20
    ordering = ('-created_at',)
    search_fields = ('code','dni', 'name')
    list_filter = (
        'country',
        'gender',
        'deleted'
    )

    def status(self, obj):
        return not obj.deleted
    status.boolean = True

admin.site.register(Students,StudentsAdmin)
admin.site.register(Certificates)


class StudentRegistersAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'student',
        'type_register',
        'country',
        'date_issue',
        'created_at',
        'status'
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
    def status(self, obj):
        return not obj.deleted
    status.boolean = True

admin.site.register(StudentRegisters,StudentRegistersAdmin)
