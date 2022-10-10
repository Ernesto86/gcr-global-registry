from django.contrib import admin
from .models import *


class AdvisersAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'code',
        'dni',
        'country',
        'names',
        'telephone',
        'email',
        'created_at',
        'estado'
    )
    list_per_page = 20
    ordering = ('-created_at',)
    search_fields = ('number', 'code', 'dni', 'names')
    list_filter = (
        'country',
        'deleted'
    )

    def estado(self, obj):
        return not obj.deleted
    estado.boolean = True


admin.site.register(Advisers, AdvisersAdmin)


class AdvisersCommissionsAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'adviser',
        'date_current',
        'date_issue',
        'date_expiration',
        'commission',
        'created_at',
        'estado'
    )
    list_per_page = 20
    ordering = ('-created_at',)
    search_fields = ('number', 'adviser')
    list_filter = (
        'institution',
        'deleted'
    )

    def estado(self, obj):
        return not obj.deleted
    estado.boolean = True


admin.site.register(AdvisersCommissions, AdvisersCommissionsAdmin)

class ItemPaymentAdviserCommissionsDetailsInline(admin.TabularInline):
    model = PaymentAdviserCommissionsDetails
    extra = 0


class PaymentAdviserCommissionsAdmin(admin.ModelAdmin):
    inlines = (ItemPaymentAdviserCommissionsDetailsInline, )
    list_display = (
        'number',
        'adviser',
        'date_payment',
        'year',
        'month',
        'values',
        'estado',
    )
    list_per_page = 20
    ordering = ('-created_at',)
    search_fields = ('numero', 'adviser__names',)
    list_filter = (
        'deleted',
    )

    def estado(self, obj):
        return not obj.deleted

    estado.boolean = True


admin.site.register(PaymentAdviserCommissions, PaymentAdviserCommissionsAdmin)
