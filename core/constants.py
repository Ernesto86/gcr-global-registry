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
