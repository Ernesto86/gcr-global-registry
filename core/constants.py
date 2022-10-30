from django.db import models
from django.utils.translation import gettext_lazy as _

TYPE_LIST = (
    ('GRUPO', 'GRUPO'),
    ('ITEM', 'ITEM'),
)

class Gender(models.TextChoices):
    MALE = "Male", _("Masculino")
    FEMALE = "Female", _("Femenino")
    OTHER = "Other", _("Otro")

class Sex(models.TextChoices):
    MALE = "Men", _("Hombre")
    FEMALE = "Woman", _("Mujer")
    OTHER = "Other", _("Otro")


class TypeDocument(models.TextChoices):
    MALE = "Identification", _("Cedula")
    FEMALE = "Passport", _("Pasaporte")
    OTHER = "Other", _("Otro")


# ESTADO_CIVIL = (
#     (1, 'SOLTERO(A)'),
#     (2, 'CASADO(A)'),
#     (3, 'DIVORCIADO(A)'),
#     (4, 'UNIÓN LIBRE'),
#     (5, 'VIUDO(A)'),
#     (6, 'SIN ESPECIFICAR/')
# )

# NACIONALIDAD = (
#     (1, 'ECUATORIANA'),
#     (2, 'COLOMBIANA'),
#     (3, 'CHILENO'),
#     (4, 'CUBANO'),
#     (5, 'PERUANO'),
#     (6, 'VENEZOLANA'),
#     (7, 'ARGENTINO'),
#     (8, 'BRASILEÑO'),
#     (9, 'MEXICANO'),
#     (10, 'PARAGUAYO'),
#     (11, 'OTROS'),
# )

# CELULAR_OPERADORES = (
#     (1, 'CLARO'),
#     (2, 'MOVISTAR'),
#     (3, 'CNT'),
#     (4, 'OTROS'),
# )

# TIPO_DISCAPACIDAD = (
#     (1, 'INTELECTUAL'),
#     (2, 'FÍSICA'),
#     (3, 'VISUAL'),
#     (4, 'AUDITIVA'),
#     (5, 'MENTAL'),
#     (6, 'OTRA'),
#     (7, 'NO APLICA')
# )

# NIVEL_FORMACION = (
#     (1, 'NIVEL TÉCNICO'),
#     (2, 'NIVEL TECNOLÓGICO'),
#     (3, 'TERCER NIVEL'),
#     (4, 'ESPECIALIDAD'),
#     (5, 'ESPECIALIDAD MÉDICA U ODONTOLÓGICA'),
#     (6, 'MAESTRÍA'),
#     (7, 'PHD'),
#     (8, 'NO APLICA'),
# )

# MESES  = (
#     (1,"ENERO"),
#     (2,"FEBRERO"),
#     (3,"MARZO"),
#     (4,"ABRIL"),
#     (5,"MAYO"),
#     (6,"JUNIO"),
#     (7,"JULIO"),
#     (8,"AGOSTO"),
#     (9,"SEPTIEMBRE"),
#     (10,"OCTUBRE"),
#     (11,"NOVIEMBRE"),
#     (12,"DICIEMBRE")
# )

SYSTEM_LOGO = 'fas fa-globe-americas fa-2x'
SYSTEM_NAME = 'Global | Registry '
SISTEMA_AUTOR = 'Ing. Ernesto Guamán U.'
SYSTEM_WEB = 'www.globalregistry.com'
