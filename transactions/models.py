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
    adviser = models.ForeignKey("advisers.Advisers", verbose_name="Asesor", on_delete=models.CASCADE, blank=True, null=True)
    manager = models.ForeignKey(
        "advisers.Managers",
        verbose_name="Gerente",
        on_delete=models.PROTECT,
        blank=True, null=True
    )
    number = models.CharField(max_length=10, blank=True, null=True, editable=False)
    date_issue = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Emision")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Subtotal", blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Descuento %", blank=True, null=True)
    # discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Descuento", blank=True, null=True)
    # subtotal_with_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Subtotal", blank=True, null=True)
    taxes = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Impuesto", blank=True, null=True)
    taxes_percentage = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Impuesto porcentaje", blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total", blank=True, null=True)
    commissions_advisers_percentage = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Comision asesor %", blank=True, null=True)
    commissions_advisers_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Comision asesor valor", blank=True, null=True)
    commissions_managers_percentage = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Comision gerente %", blank=True, null=True)
    commissions_managers_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Comision gerente valor", blank=True, null=True)
    commissions_admin_percentage = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Comision administrador %", blank=True, null=True)
    commissions_admin_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Comision administrador valor", blank=True, null=True)
    pay_adviser = models.BooleanField(default=False)
    pay_manager = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Orden institucion cupo"
        verbose_name_plural = "Orden institucion cupos"
        ordering = ('number',)

    def __str__(self):
        return '{}'.format(self.number)

    def get_commission_adviser_clear(self):
        return util_null_to_decimal(self.subtotal * (self.commissions_advisers_percentage / 100))

    def get_commission_adviser(self):
        return util_null_to_decimal(self.get_commission_adviser_clear() - self.get_commission_manager())

    # def get_commission_adviser(self):
    #     return util_null_to_decimal(self.get_commission_adviser_clear() - self.get_commission_manager() - self.get_commission_admin())

    def get_commission_manager(self):
        return util_null_to_decimal(self.get_commission_adviser_clear() * (self.commissions_managers_percentage / 100))

    # def get_commission_manager(self):
    #     return util_null_to_decimal(self.get_commission_adviser_clear() - self.get_commission_admin() * (self.commissions_managers_percentage / 100))

    def get_commission_admin(self):
        return util_null_to_decimal(self.get_commission_adviser_clear() * (self.commissions_managers_percentage / 100))

    def get_discount_decimal(self):
        return util_null_to_decimal(self.discount_percentage / 100)

    def get_taxes_decimal(self):
        return util_null_to_decimal(self.taxes_percentage / 100)

    def calculate(self):
        self.subtotal = util_null_to_decimal(self.orderinstitutionquotadetails_set.all().aggregate(sum=Sum('total_item'))['sum'])
        # TODO: INCLUDE AND DETERMINATE THE IVA
        self.taxes = util_null_to_decimal(self.subtotal * self.get_taxes_decimal())
        self.total = util_null_to_decimal(self.subtotal + self.taxes)
        self.commissions_advisers_value = self.get_commission_adviser()
        self.commissions_managers_value = self.get_commission_manager()
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
    quotas = models.IntegerField(default=0, verbose_name="cupos", blank=True, null=True)
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
