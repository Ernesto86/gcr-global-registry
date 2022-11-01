from django.db import models
from core.models import ModelBaseAudited
from core.constants import TypePost
class Advisers(ModelBaseAudited):
    country = models.ForeignKey("system.SysCountries", verbose_name="Pais", on_delete=models.CASCADE, blank=True, null=True)
    user = models.OneToOneField("security.User", verbose_name="Usuario", on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=20, verbose_name="Código", blank=True, null=True)
    number = models.CharField(max_length=10,blank=True, null=True,editable=False)
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
        ordering = ('number',)

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

class AdvisersCommissions(ModelBaseAudited):
    institution = models.ForeignKey(
        "institutions.Institutions",
        on_delete=models.CASCADE,
        verbose_name="Institución"
    )
    adviser = models.ForeignKey(
        Advisers,
        on_delete=models.CASCADE,
        verbose_name="Asesor"
    )
    number = models.CharField(max_length=10, blank=True, null=True, editable=False)
    date_current = models.DateTimeField(blank=True, null=True, verbose_name="Fecha")
    date_issue = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Emisión")
    date_expiration = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Vencimiento")
    commission = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Comisión", blank=True, null=True)

    class Meta:
        verbose_name = 'Asesor Comisión'
        verbose_name_plural = 'Asesor Comisiones'
        ordering = ('number',)

    def __str__(self):
        return '{}'.format(self.number)


    def save(self, *args, **kwargs):
        super(AdvisersCommissions, self).save(*args, **kwargs)
        self.number = str(self.id).zfill(10)
        super(AdvisersCommissions, self).save(*args, **kwargs)

class PaymentAdviserCommissions(ModelBaseAudited):
    adviser = models.ForeignKey(Advisers, on_delete=models.CASCADE, verbose_name="Asesor")
    number = models.CharField(max_length=10, blank=True, null=True, editable=False)
    date_payment = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Pago")
    year = models.IntegerField(blank=True, null=True, verbose_name="Año")
    month = models.IntegerField(blank=True, null=True, verbose_name="Mes")
    values = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor", blank=True, null=True)

    class Meta:
        verbose_name = 'Pago Asesor Comisión'
        verbose_name_plural = 'Pago Asesor Comisiones'
        ordering = ('number',)

    def __str__(self):
        return '{}'.format(self.number)

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
    order_institution_quota = models.ForeignKey(
        "transactions.OrderInstitutionQuotas",
        on_delete=models.CASCADE,
        verbose_name="Orden institucion Cupo"
    )
    type_register = models.ForeignKey(
        "institutions.InsTypeRegistries",
        on_delete=models.CASCADE,
        verbose_name="Tipo de registro",
        blank=True, null=True
    )
    commission = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Comisión", blank=True, null=True)
    value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor", blank=True, null=True)

    class Meta:
        verbose_name = 'Pago Asesor Comisión Detalle'
        verbose_name_plural = 'Pago Asesor Comisión Detalles'

    def __str__(self):
        return '{}'.format(self.value)

class Functionary(ModelBaseAudited):
    country = models.ForeignKey("system.SysCountries", verbose_name="Pais", on_delete=models.CASCADE, blank=True, null=True)
    user = models.OneToOneField("security.User", verbose_name="Usuario", on_delete=models.CASCADE, blank=True, null=True)
    type_post = models.CharField(
        verbose_name="Tipo Cargo",
        choices=TypePost.choices,
        max_length=15,
    )
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
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'
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
