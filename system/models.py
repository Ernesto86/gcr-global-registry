from django.db import models
from core.models import ModelBase, ModelBaseAudited

class SysNationality(ModelBase):
    code = models.CharField(max_length=10, verbose_name="Código", blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    name_short = models.CharField(max_length=50, verbose_name="Nombre corto", blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Nacionalidad'
        verbose_name_plural = 'Nacionalidades'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.upper()

        if self.name:
            self.name = self.name.upper()

        if self.name_short:
            self.name_short = self.name_short.upper()

        super(SysNationality, self).save(*args, **kwargs)

class SysCountries(ModelBase):
    code = models.CharField(max_length=10, verbose_name="Código", blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    name_short = models.CharField(max_length=50, verbose_name="Nombre corto", blank=True, null=True)

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

        super(SysCountries, self).save(*args, **kwargs)

class SysParameters(ModelBase):
    TYPE_PARAMETERS = (
        ('LIST','LIST'),
        ('LISTITEM','LISTITEM'),
        ('PARAMETER','PARAMETER'),
        ('TREE','TREE'),
        ('TREENODE','TREENODE')
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=50, verbose_name="Código", blank=True, null=True)
    name = models.CharField(max_length=200, verbose_name="Nombre")
    type_parameter = models.CharField(max_length=10,verbose_name="Tipo parametro", choices=TYPE_PARAMETERS)
    value = models.CharField(max_length=100, verbose_name="Valor", blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name="Estado")
    extra_data = models.CharField(max_length=1024, verbose_name="Extra datos", blank=True, null=True)
    route = models.CharField(max_length=1024, blank=True, null=True, editable=False)
    order = models.CharField(max_length=1024, blank=True, null=True, editable=False)

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

        super(SysParameters, self).save(*args, **kwargs)

        codid = str(self.id).zfill(6)

        if self.code is None:
            self.codid = codid

        if not self.parent is None:
            self.route = self.parent.route + '/' + codid
            self.order = self.parent.order + '/' + str(self.name)
        else:
            self.route = 'ROOT/' + codid
            self.order = 'General/' + str(self.name)

        super(SysParameters, self).save(*args, **kwargs)
