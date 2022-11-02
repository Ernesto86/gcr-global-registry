from django.contrib import admin
from .models import *

class ItemOrderInstitutionQuotaDetailsInline(admin.TabularInline):
    model = OrderInstitutionQuotaDetails
    extra = 0


class OrderInstitutionQuotasAdmin(admin.ModelAdmin):
    inlines = (ItemOrderInstitutionQuotaDetailsInline, )
    list_display = (
        'number',
        'institution',
        'date_issue',
        'subtotal',
        'taxes',
        'total',
        'created_at',
        'estado'
    )
    list_per_page = 20
    ordering = ('-created_at',)
    search_fields = ('number', 'date_issue')
    list_filter = (
        'institution',
        'deleted'
    )

    def estado(self, obj):
        return not obj.deleted

    estado.boolean = True


admin.site.register(OrderInstitutionQuotas, OrderInstitutionQuotasAdmin)
