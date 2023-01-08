from django.db import models

from core.constants import SYS_PARAMETER_CODE, SYS_PARAMETER_DATE_EXPIRY_OF_REGISTER_CODE
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

class AcademicLevel(ModelBase):
    code = models.CharField(max_length=10, verbose_name="Código", blank=True, null=True)
    name = models.CharField(max_length=191, verbose_name="Nombre")
    name_short = models.CharField(max_length=50, verbose_name="Nombre corto", blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Nivel académico'
        verbose_name_plural = 'Niveles académicos'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.upper()

        if self.name:
            self.name = self.name.upper()

        if self.name_short:
            self.name_short = self.name_short.upper()

        ModelBase.save(self)

class SysParameters(ModelBase):
    code = models.CharField(max_length=50, verbose_name="Código", blank=True, null=True)
    name = models.CharField(max_length=200, verbose_name="Nombre")
    value = models.CharField(max_length=100, verbose_name="Valor", blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name="Estado")
    extra_data = models.CharField(max_length=1024, verbose_name="Extra datos", blank=True, null=True)
    extra_json = models.JSONField(verbose_name="Extra Json", blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

    @staticmethod
    def get_parameter_fer_value():
        return int(SysParameters.objects.get(code=SYS_PARAMETER_DATE_EXPIRY_OF_REGISTER_CODE).value)

    @staticmethod
    def get_parameter_next():
        return int(SysParameters.objects.get(code=SYS_PARAMETER_CODE).value) + 1

    @staticmethod
    def get_value_formate_next():
        sys_parameters = SysParameters.objects.get(code=SYS_PARAMETER_CODE)
        return {
            'code': sys_parameters.code,
            'value': sys_parameters.value,
            'next_value': int(sys_parameters.value) + 1,
            'format': f"{sys_parameters.code}-{int(sys_parameters.value) + 1}"
        }

    @staticmethod
    def update_value():
        sys_parameters = SysParameters.objects.get(code=SYS_PARAMETER_CODE)
        sys_parameters.value = int(sys_parameters.value) + 1
        sys_parameters.save()

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
