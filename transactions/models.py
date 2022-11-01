from django.db import models
from core.models import ModelBaseAudited, ModelBase
from django.db.models import Sum
from core.util_functions import util_null_to_decimal

class OrderInstitutionQuotas(ModelBaseAudited):
    institution = models.ForeignKey(
        "institutions.Institutions",
         on_delete=models.CASCADE,
         verbose_name="Institución"
    )
    number = models.CharField(max_length=10, blank=True, null=True, editable=False)
    date_issue = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Emision")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Subtotal", blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Descuento %", blank=True, null=True)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Descuento", blank=True, null=True)
    subtotal_with_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Subtotal", blank=True, null=True)
    taxes = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Impuesto", blank=True, null=True)
    taxes_percentage = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Impuesto porcentaje", blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total", blank=True, null=True)

    class Meta:
        verbose_name = "Orden institucion cupo"
        verbose_name_plural = "Orden institucion cupos"
        ordering = ('number',)

    def __str__(self):
        return '{}'.format(self.number)


    def get_discount_decimal(self):
        return self.discount_percentage / 100

    def calculate(self):
        self.subtotal = util_null_to_decimal(self.orderinstitutionquotadetails_set.all().aggregate(sum=Sum('subtotal'))['sum'])
        self.discount = util_null_to_decimal(self.get_discount_decimal() * self.subtotal)
        self.subtotal_with_discount = util_null_to_decimal(self.subtotal - self.discount)
        # TODO: INCLUDE AND DETERMINATE THE IVA
        self.taxes = self.subtotal_with_discount * 0
        self.total = self.subtotal_with_discount + self.taxes
        self.save()

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
    values = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name="Valor", blank=True, null=True)
    values_discount = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name="Valor", blank=True, null=True)
    total_item = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name="Total", blank=True, null=True)

    class Meta:
        verbose_name = "Orden institucion cupo detalle"
        verbose_name_plural = "Orden institucion cupo detalles"
        ordering = ('order_institution_quota',)

    def __str__(self):
        return '{}'.format(self.detail)

class InstitutionQuotesTypeRegister(ModelBase):
    institution = models.ForeignKey(
        "institutions.Institutions",
        on_delete=models.CASCADE,
        verbose_name="Institución"
    )
    type_register = models.ForeignKey(
        "institutions.InsTypeRegistries",
        on_delete=models.CASCADE,
        verbose_name="Tipo de registro",
        blank=True, null=True
    )
    quotas = models.IntegerField(default=0, verbose_name="Cupos", blank=True, null=True)
    quotas_balance = models.IntegerField(default=0, verbose_name="Cupos saldo", blank=True, null=True)

    class Meta:
        verbose_name = "Institucion cupo saldo"
        verbose_name_plural = "Institucion cupos saldos"
        ordering = ('created_at',)
