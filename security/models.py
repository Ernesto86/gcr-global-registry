from tabnanny import verbose
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.models import ModelBase
from .managers import CustomUserManager
class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(verbose_name=_("Username"), max_length=191, unique=True)
    first_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=50)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    foto = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        verbose_name='Archive Photo',
        max_length=1024,
        blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return '{}'.format(self.username)

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username

    def get_foto_url(self):
        return self.foto.url

class SecurityModule(ModelBase):
    TYPE_RESOURCE = (
        ('Mantenimientos', 'MANTENIMIENTOS'),
        ('Documentos', 'DOCUMENTOS'),
        ('Procesos', 'PROCESOS'),
        ('Informes', 'INFORMES'),
        ('Seguridad', 'SEGURIDAD'),
    )
    code = models.CharField(max_length=10, verbose_name="Código", blank=True, null=True)
    url = models.CharField(max_length=100, verbose_name="Enlace")
    name = models.CharField(max_length=100, verbose_name="Nombre")
    type_module = models.CharField(max_length=15, verbose_name="Tipo modulo", blank=True, null=True, choices=TYPE_RESOURCE)
    icon = models.CharField(max_length=100, verbose_name="Icono", blank=True, null=True)
    image = models.ImageField(upload_to='module/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    description = models.CharField(max_length=100, verbose_name="Descripción", blank=True, null=True)
    order = models.IntegerField(default=0, verbose_name="Orden", blank=True, null=True)
    permits = models.ManyToManyField(Permission, verbose_name='Permisos', blank=True, null=True)

    def __str__(self):
        return '{} (/{})'.format(self.name, self.url)

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['order']

    def save(self, force_insert=False, force_update=False, using=None, **kwargs):
        if self.code:
            self.code = self.code.upper()
        if self.name:
            self.name = self.name.upper()

        ModelBase.save(self)

class SecurityModuloGrupo(ModelBase):
    name = models.CharField(max_length=100, verbose_name="Nombre", blank=True, null=True)
    description = models.CharField(max_length=200, verbose_name="Descripción", blank=True, null=True)
    module = models.ManyToManyField(SecurityModule, verbose_name="Modulos")
    groups = models.ManyToManyField(Group, verbose_name="Grupos")
    priority = models.IntegerField(verbose_name="Prioridad", blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.priority)
    class Meta:
        verbose_name = 'Grupo de Módulos'
        verbose_name_plural = 'Grupos de Módulos'
        ordering = ['priority', 'name']

    def save(self, force_insert=False, force_update=False, using=None, **kwargs):
        if self.name:
            self.name = self.name.upper()

        ModelBase.save(self)
