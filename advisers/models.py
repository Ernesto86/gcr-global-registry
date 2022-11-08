from decimal import Decimal

from django.db import models

from advisers.choices import TL_YEAR, TL_MONTH
from core.models import ModelBaseAudited
from django.db.models import Sum
from core.util_functions import util_null_to_decimal


class Advisers(ModelBaseAudited):
    country_origin = models.ForeignKey(
        "system.SysCountries",
        verbose_name="Pais de origin",
        on_delete=models.PROTECT,
        related_name='country_origin_advisers_set',
        blank=True, null=True
    )
    country_residence = models.ForeignKey(
        "system.SysCountries",
        verbose_name="Pais de residencia",
        on_delete=models.PROTECT,
        related_name='country_residence_advisers_set',
        blank=True, null=True
    )
    manager = models.ForeignKey(
        "advisers.Managers",
        verbose_name="Gerente",
        on_delete=models.PROTECT,
        blank=True, null=True
    )
    user = models.OneToOneField("security.User", verbose_name="Usuario", on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=20, verbose_name="Código", blank=True, null=True)
    names = models.CharField(max_length=100, verbose_name="Apellidos y nombres", blank=True, null=True, editable=False)
    last_name = models.CharField(max_length=100, verbose_name="Apellidos")
    first_name = models.CharField(max_length=100, verbose_name="Nombres")
    dni = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=1024, verbose_name="Dirección", blank=True, null=True)
    code_postal = models.CharField(max_length=10, verbose_name="Cod. postal", blank=True, null=True)
    telephone = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, null=True)
    cell_phone = models.CharField(max_length=20, verbose_name="Celular", blank=True, null=True)
    email = models.CharField(max_length=150, verbose_name="Email", blank=True, null=True)
    email_alternate = models.CharField(max_length=150, verbose_name="Email alterno", blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.names)

    class Meta:
        verbose_name = 'Asesor'
        verbose_name_plural = 'Asesores'
        ordering = ('code',)

    def save(self, *args, **kwargs):

        if self.code:
            self.code = self.code.upper()

        if self.last_name:
            self.last_name = self.last_name.upper()

        if self.first_name:
            self.first_name = self.first_name.upper()

        if self.address:
            self.address = self.address.upper()

        if self.email:
            self.email = self.email.lower()

        if self.email_alternate:
            self.email_alternate = self.email_alternate.lower()

        self.names = self.last_name + ' ' + self.first_name

        super(Advisers, self).save(*args, **kwargs)

        self.number = str(self.id).zfill(10)
        super(Advisers, self).save(*args, **kwargs)


class PaymentAdviserCommissions(ModelBaseAudited):
    TYPE_FUNCTIONARY = (
        (0, 'ASERSOR'),
        (1, 'GERENTE'),
    )
    number = models.CharField(max_length=10, blank=True, null=True, editable=False)
    date_payment = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Pago")
    year = models.IntegerField(blank=True, null=True, verbose_name="Año", choices=TL_YEAR, default=TL_YEAR[0][0])
    month = models.IntegerField(blank=True, null=True, verbose_name="Mes", choices=TL_MONTH, default=TL_MONTH[0][0])
    values_commission = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Comision asesor", blank=True, null=True)
    type_functionary = models.IntegerField(verbose_name="Tipo de funcionario", choices=TYPE_FUNCTIONARY, default=TYPE_FUNCTIONARY[0][0])
    pay_period = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Pago Asesor Comisión'
        verbose_name_plural = 'Pago Asesor Comisiones'
        ordering = ('number',)

    def __str__(self):
        return '{}'.format(self.number)

    def calculate(self):
        self.values_commission = util_null_to_decimal(self.paymentadvisercommissionsdetails_set.all().aggregate(sum=Sum('value_commission'))['sum'])
        self.save()

    def save(self, *args, **kwargs):
        super(PaymentAdviserCommissions, self).save(*args, **kwargs)
        self.number = str(self.id).zfill(10)
        super(PaymentAdviserCommissions, self).save(*args, **kwargs)


class PaymentAdviserCommissionsDetails(ModelBaseAudited):
    payment_adviser_commissions = models.ForeignKey(
        PaymentAdviserCommissions,
        on_delete=models.CASCADE,
        verbose_name="Pago Asesor Comisión"
    )
    adviser = models.ForeignKey("advisers.Advisers", verbose_name="Asesor", on_delete=models.CASCADE, blank=True, null=True)
    manager = models.ForeignKey(
        "advisers.Managers",
        verbose_name="Gerente",
        on_delete=models.PROTECT,
        blank=True, null=True
    )
    value_commission = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor asesor", blank=True, null=True)
    pay = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Pago Asesor Comisión Detalle'
        verbose_name_plural = 'Pago Asesor Comisión Detalles'

    def __str__(self):
        return '{}'.format(self.value_commission)


class Managers(ModelBaseAudited):
    country_origin = models.ForeignKey(
        "system.SysCountries",
        verbose_name="Pais de origin",
        on_delete=models.PROTECT
    )
    country_residence = models.ForeignKey(
        "system.SysCountries",
        verbose_name="Pais de residencia",
        on_delete=models.PROTECT,
        related_name='country_residence_advisers'
    )
    user = models.OneToOneField("security.User", verbose_name="Usuario", on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=20, verbose_name="Código", blank=True, null=True)
    names = models.CharField(max_length=100, verbose_name="Apellidos y nombres", blank=True, null=True, editable=False)
    last_name = models.CharField(max_length=100, verbose_name="Apellidos")
    first_name = models.CharField(max_length=100, verbose_name="Nombres")
    dni = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=1024, verbose_name="Dirección", blank=True, null=True)
    code_postal = models.CharField(max_length=10, verbose_name="Cod. postal", blank=True, null=True)
    telephone = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, null=True)
    cell_phone = models.CharField(max_length=20, verbose_name="Celular", blank=True, null=True)
    email = models.CharField(max_length=150, verbose_name="Email", blank=True, null=True)
    email_alternate = models.CharField(max_length=150, verbose_name="Email alterno", blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.names)

    class Meta:
        verbose_name = 'Gerente'
        verbose_name_plural = 'Gerentes'
        ordering = ('created_at',)

    def save(self, *args, **kwargs):

        if self.code:
            self.code = self.code.upper()

        if self.last_name:
            self.last_name = self.last_name.upper()

        if self.first_name:
            self.first_name = self.first_name.upper()

        if self.address:
            self.address = self.address.upper()

        if self.email:
            self.email = self.email.lower()

        if self.email_alternate:
            self.email_alternate = self.email_alternate.lower()

        self.names = self.last_name + ' ' + self.first_name

        ModelBaseAudited.save(self)


class PeriodCommissions(ModelBaseAudited):
    manager_percentage = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0), verbose_name='Porcentaje gerente %')
    advisers_percentage_period_1 = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0), verbose_name='Periodo 1 porcentaje asesor %')
    days_commissions_period_1 = models.IntegerField(default=0, verbose_name="Periodo 1 dias comision")
    advisers_percentage_max_period_1 = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0), verbose_name='Periodo 1 porcentaje asesor maximo %')
    advisers_percentage_period_2 = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0), verbose_name='Periodo 2 porcentaje asesor %')
    days_commissions_period_2 = models.IntegerField(default=0, verbose_name="Periodo 2 dias comision")
    advisers_percentage_max_period_2 = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0), verbose_name='Periodo 2 porcentaje asesor maximo %')
    advisers_percentage_period_3 = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0), verbose_name='Periodo 3 porcentaje asesor %')
    days_commissions_period_3 = models.IntegerField(default=0, verbose_name="Periodo 3 dias comision")
    advisers_percentage_max_period_3 = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0), verbose_name='Periodo 3 porcentaje asesor maximo %')
    manager_percentage_max = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0), verbose_name='Porcentaje gerente maximo %')

    def __str__(self):
        return 'id : {}'.format(self.id)

    class Meta:
        verbose_name = 'Perido comision'
        verbose_name_plural = 'Periodos comisiones'
        ordering = ('id',)


class AdvisersCommissions(ModelBaseAudited):
    period_commissions = models.ForeignKey(
        PeriodCommissions,
        on_delete=models.PROTECT,
        verbose_name="Periodo",
        blank=True, null=True
    )
    adviser = models.ForeignKey(
        Advisers,
        on_delete=models.CASCADE,
        verbose_name="Asesor"
    )
    commissions_period_1 = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0), verbose_name='Comision periodo 1 porcentaje %')
    commissions_period_2 = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0), verbose_name='Comision periodo 2 porcentaje %')
    commissions_period_3 = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0), verbose_name='Comision periodo 3 porcentaje %')
    is_exclude = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.adviser.__str__())

    class Meta:
        verbose_name = 'Asesor Comisión'
        verbose_name_plural = 'Asesor Comisiones'


class ManagersCommissions(ModelBaseAudited):
    manager = models.ForeignKey(
        Managers,
        on_delete=models.CASCADE,
        verbose_name="Manager"
    )
    value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0), verbose_name='Porcentaje %')
    is_exclude = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.value)

    class Meta:
        verbose_name = 'Gerente Comisión'
        verbose_name_plural = 'Gerente Comisiones'
