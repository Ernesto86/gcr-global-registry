from crum import get_current_user
from django.db import models

from api.settings import MEDIA_URL
from core.common.form.ImageCommon import ImageCommon


# from django.utils.translation import ugettext_lazy as _

class ModelBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.CharField(max_length=100, blank=True, null=True, editable=False)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)
    deleted_by = models.CharField(max_length=100, blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        try:
            user = get_current_user()
            if self._state.adding:
                self.created_by = user.username
            else:
                self.update_by = user.username
        except:
            pass

        models.Model.save(self)

    class Meta:
        abstract = True

class ModelBaseAudited(models.Model):
    institution_id = models.IntegerField(verbose_name="Institución Code", blank=True, null=True, editable=False)
    detail = models.CharField(max_length=1024, verbose_name="Detalle", blank=True, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.CharField(max_length=100, blank=True, null=True, editable=False)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)
    deleted_by = models.CharField(max_length=100, blank=True, null=True, editable=False)
    deleted_reason = models.CharField(max_length=191, blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        try:
            user = get_current_user()
            if self._state.adding:
                self.created_by = user.username
            else:
                self.update_by = user.username
        except:
            pass

        models.Model.save(self)

    class Meta:
        abstract = True

# class ContentTypeRestrictedFileField(FileField):
#     """
#     Same as FileField, but you can specify:
#         * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
#         * max_upload_size - a number indicating the maximum file size allowed for upload.
#             2.5MB - 2621440
#             5MB - 5242880
#             10MB - 10485760
#             20MB - 20971520
#             50MB - 5242880
#             100MB 104857600
#             250MB - 214958080
#             500MB - 429916160
#     """
#
#     def __init__(self, *args, **kwargs):
#         self.content_types = kwargs.pop("content_types")
#         self.max_upload_size = kwargs.pop("max_upload_size")
#
#         super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)
#
#     def clean(self, *args, **kwargs):
#         data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
#
#         file = data.file
#         try:
#             content_type = file.content_type
#             if content_type in self.content_types:
#                 if file._size > self.max_upload_size:
#                     raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (
#                     filesizeformat(self.max_upload_size), filesizeformat(file._size)))
#             else:
#                 raise forms.ValidationError(_('Filetype not supported.'))
#         except AttributeError:
#             pass
#
#         return data


class CommissionPorcentage(ModelBaseAudited):
    values = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor", blank=True, null=True)

    def __str__(self):
        return '{} (/{})'.format(self.name, self.url)

    class Meta:
        verbose_name = 'Comiison porcentaje'
        verbose_name_plural = 'Comiisones porcentaje'
        ordering = ['created_at',]


class SystemSettings(models.Model):
    signature = models.ImageField(
        upload_to='systemsettings/logo/%Y/%m/%d',
        max_length=1024,
        null=True,
        verbose_name="Firma"
    )

    def get_signature_image(self):
        return ImageCommon.get_image(self.signature)

    def get_logo_url(self):
        return self.logo.url

    class Meta:
        verbose_name = 'Configuracion del sistema'
        verbose_name_plural = 'Configuraciones del sistema'

