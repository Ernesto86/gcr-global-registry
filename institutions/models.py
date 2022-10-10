from django.db import models
from core.models import ModelBase, ModelBaseAudited
from core.constants import TYPE_LIST

class InsTypeRegistries(ModelBase):
    parent = models.ForeignKey('self', verbose_name="Principal", on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=50, verbose_name="Código", blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    detail = models.CharField(max_length=100, verbose_name="Detalle", blank=True, null=True)
    type = models.CharField(max_length=10, verbose_name="Tipo", blank=True, null=True, choices=TYPE_LIST)
    route = models.CharField(max_length=1024, blank=True, null=True, editable=False)
    order = models.CharField(max_length=1024, blank=True, null=True, editable=False)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Tipo de Registro'
        verbose_name_plural = 'Tipo de Registros'
        ordering = ('created_at',)

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.upper()

        if self.name:
            self.name = self.name.upper()

        super(InsTypeRegistries, self).save(*args, **kwargs)

        codid = str(self.id).zfill(6)

        if self.code is None:
            self.codid = codid

        if not self.parent is None:
            self.route = self.parent.route + '/' + codid
            self.order = self.parent.order + '/' + str(self.name)
        else:
            self.route = 'ROOT/' + codid
            self.order = 'General/' + str(self.name)

        super(InsTypeRegistries, self).save(*args, **kwargs)


class Institutions(ModelBaseAudited):
    adviser = models.ForeignKey("advisers.Advisers", verbose_name="Asesor", on_delete=models.CASCADE, blank=True, null=True)
    type_registration = models.ForeignKey(InsTypeRegistries, verbose_name="Tipo de registro", on_delete=models.CASCADE, blank=True, null=True)
    country = models.ForeignKey("system.SysCountries", verbose_name="Pais", on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=3, verbose_name="Código", blank=True, null=True)
    number = models.CharField(max_length=10, blank=True, null=True, editable=False)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    alias = models.CharField(max_length=20, verbose_name="Alias", blank=True, null=True)
    representative = models.CharField(max_length=200, verbose_name="Representante", blank=True, null=True)
    identification = models.CharField(max_length=20, verbose_name="Identificación", blank=True, null=True)
    address = models.CharField(max_length=1024, verbose_name="Dirección", blank=True, null=True)
    code_postal = models.CharField(max_length=10, verbose_name="Cod. postal", blank=True, null=True)
    telephone = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, null=True)
    email = models.CharField(max_length=150, verbose_name="Email", blank=True, null=True)
    email_alternate = models.CharField(max_length=150, verbose_name="Email alterno", blank=True, null=True)
    web = models.CharField(max_length=200, verbose_name="Web", blank=True, null=True)
    file_constitution = models.FileField(upload_to='institutions/constitution/%Y/%m/%d', verbose_name="Archivo constitución", max_length=1024, blank=True, null=True)
    file_nomination = models.FileField(upload_to='institutions/nomination/%Y/%m/%d', verbose_name="Archivo Nominación", max_length=1024, blank=True, null=True)
    file_title_academic = models.FileField(upload_to='institutions/title_academic/%Y/%m/%d', verbose_name="Titulo académico", max_length=1024, blank=True, null=True)
    logo = models.ImageField(upload_to='institutions/logo/%Y/%m/%d', max_length=1024, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'
        ordering = ('created_at',)

    def save(self, *args, **kwargs):

        if self.code:
            self.code = self.code.upper()

        if self.name:
            self.name = self.name.upper()

        if self.alias:
            self.alias = self.alias.upper()

        if self.representative:
            self.representative = self.representative.upper()

        if self.address:
            self.address = self.address.upper()

        if self.email:
            self.email = self.email.lower()

        if self.email_alternate:
            self.email_alternate = self.email_alternate.lower()

        if self.web:
            self.web = self.web.lower()

        super(Institutions, self).save(*args, **kwargs)

        self.number = str(self.id).zfill(10)
        super(Institutions, self).save(*args, **kwargs)
