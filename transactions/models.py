from decimal import Decimal
from django.db import models
from core.models import ModelBaseAudited

# Create your models here.

#orden institucion cupo
class OrderInstitutionQuotas(ModelBaseAudited):
    institution = models.ForeignKey(
        "institutions.Institutions",
         on_delete=models.CASCADE,
         verbose_name="Institución"
    )
    number = models.CharField(max_length=10, blank=True, null=True, editable=False)
    date_issue = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Emision")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0,verbose_name="Subtotal", blank=True, null=True)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Descuento", blank=True, null=True)
    taxes = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Impuesto", blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total", blank=True, null=True)

    class Meta:
        verbose_name = "Orden institucion cupo"
        verbose_name_plural = "Orden institucion cupos"
        ordering = ('number',)

    def __str__(self):
        return '{}'.format(self.number)

    def save(self, *args, **kwargs):
        super(OrderInstitutionQuotas, self).save(*args, **kwargs)
        self.number = str(self.id).zfill(10)
        super(OrderInstitutionQuotas, self).save(*args, **kwargs)


class OrderInstitutionQuotaDetails(ModelBaseAudited):
    order_institution_quota = models.ForeignKey(
        OrderInstitutionQuotas,
        on_delete=models.CASCADE,
        verbose_name="Orden institucion cupo"
    )
    type_register = models.ForeignKey(
        "institutions.InsTypeRegistries",
        on_delete=models.CASCADE,
        verbose_name="Tipo de registro",
        blank=True, null=True
    )
    quotas = models.IntegerField(default=0, verbose_name="cupos" ,blank=True, null=True)
    values = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor", blank=True, null=True)
    quota_balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Cupo Saldo", blank=True, null=True)


    class Meta:
        verbose_name = "Orden institucion cupo detalle"
        verbose_name_plural = "Orden institucion cupo detalles"
        ordering = ('order_institution_quota',)

    def __str__(self):
        return '{}'.format(self.detail)
