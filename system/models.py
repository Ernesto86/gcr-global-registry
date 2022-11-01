from django.db import models
from core.models import ModelBase

class SysCountries(ModelBase):
    code = models.CharField(max_length=10, verbose_name="Código", blank=True, null=True)
    name = models.CharField(max_length=191, verbose_name="Nombre")
    name_short = models.CharField(max_length=50, verbose_name="Nombre corto", blank=True, null=True)
    nationality = models.CharField(max_length=50, verbose_name="Nacionalidad", blank=True, null=True)
    taxes = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Impuesto", blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.upper()

        if self.name:
            self.name = self.name.upper()

        if self.name_short:
            self.name_short = self.name_short.upper()

        if self.nationality:
            self.nationality = self.nationality.upper()

        ModelBase.save(self)

class SysParameters(ModelBase):
    code = models.CharField(max_length=50, verbose_name="Código", blank=True, null=True)
    name = models.CharField(max_length=200, verbose_name="Nombre")
    value = models.CharField(max_length=100, verbose_name="Valor", blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name="Estado")
    extra_data = models.CharField(max_length=1024, verbose_name="Extra datos", blank=True, null=True)
    extra_json = models.JSONField(verbose_name="Extra Json",blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Parametro'
        verbose_name_plural = 'Parametros'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.upper()
        if self.name:
            self.name = self.name.upper()

        ModelBase.save(self)
