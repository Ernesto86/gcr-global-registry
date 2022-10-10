from django.db import models
from core.models import ModelBase, ModelBaseAudited
from core.constants import Gender


class Certificates(ModelBase):
    code = models.CharField(max_length=10, verbose_name="Código", blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.CharField(max_length=250, verbose_name="Descripción", blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.upper()

        if self.name:
            self.name = self.name.upper()

        if self.description:
            self.description = self.description.upper()

        super(Certificates, self).save(*args, **kwargs)

class Students(ModelBaseAudited):
    country = models.ForeignKey("system.SysCountries", verbose_name="Pais", on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=20, verbose_name="Código", blank=True, null=True)
    number = models.CharField(max_length=10, blank=True, null=True,editable=False)
    names = models.CharField(max_length=100, verbose_name="Apellidos y nombres", blank=True, null=True, editable=False)
    last_name = models.CharField(max_length=100, verbose_name="Apellidos")
    first_name = models.CharField(max_length=100, verbose_name="Nombres")
    gender = models.CharField(
        verbose_name="Genero",
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=10,
    )
    dni = models.CharField(max_length=20, blank=True, null=True)
    nationality = models.ForeignKey("system.SysNationality", verbose_name="Nacionalidad", on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=1024, verbose_name="Dirección", blank=True, null=True)
    code_postal = models.CharField(max_length=10, verbose_name="Cod. postal", blank=True, null=True)
    telephone = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, null=True)
    cell_phone = models.CharField(max_length=20, verbose_name="Celular", blank=True, null=True)
    email = models.CharField(max_length=150, verbose_name="Email", blank=True, null=True)
    email_alternate = models.CharField(max_length=150, verbose_name="Email alterno", blank=True, null=True)

    def __str__(self):
        return "{}".format(self.names)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ('names',)

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

        super(Students, self).save(*args, **kwargs)

        self.number = str(self.id).zfill(10)
        super(Students, self).save(*args, **kwargs)

class StudentRegisters(ModelBaseAudited):
    institution = models.ForeignKey(
        "institutions.Institutions",
        on_delete=models.CASCADE,
        verbose_name='Institución',
        blank=True, null=True
    )
    student = models.ForeignKey(
        Students,
        on_delete=models.CASCADE,
        verbose_name='Estudiante',
        blank=True, null=True
    )
    type_register = models.ForeignKey(
        "institutions.InsTypeRegistries",
        on_delete=models.CASCADE,
        verbose_name="Tipo de registro",
        blank=True, null=True
    )
    certificate = models.ForeignKey(
        Certificates,
        on_delete=models.CASCADE,
        verbose_name='Certificado',
        blank=True, null=True
    )
    country = models.ForeignKey(
        "system.SysCountries",
        on_delete=models.CASCADE,
        verbose_name='Pais',
        blank=True, null=True
    )
    number = models.CharField(max_length=10, blank=True, null=True, editable=False)
    date_issue = models.DateTimeField(blank=True, null=True)
    code_international_register = models.CharField(
        max_length=100,
        verbose_name='Código Internacional de Registro',
        blank=True, null=True
    )

    class Meta:
        verbose_name = "Estudiante Registro"
        verbose_name_plural = "Estudiante Registros"
        ordering = ('created_at',)

    def __str__(self):
        return '{}'.format(self.detail)


    def save(self, *args, **kwargs):
        super(StudentRegisters, self).save(*args, **kwargs)
        self.number = str(self.id).zfill(10)
        super(StudentRegisters, self).save(*args, **kwargs)
