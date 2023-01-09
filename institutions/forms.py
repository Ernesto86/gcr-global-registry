from django import forms

from core.common.form.form_common import FormCommon
from institutions.models import Institutions


class InstitutionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_all_field(self.fields)

    class Meta:
        model = Institutions
        exclude = ('detail','created_at', 'created_by', 'deleted', 'deleted_at', 'deleted_by', 'deleted_reason')
        widgets = {
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ingrese cuenta de correo electrónico',
                'type': 'email',
            }),
            'adviser': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Ingrese el código del Asesor'
            }),
            'type_registration': forms.Select(attrs={
                'class': 'select2-design',
                'required': True
            }),
            'file_constitution': forms.FileInput(attrs={
                'class': 'custom-file-input',
                'accept': '.pdf',
                'required': True
            }),
            'file_nomination': forms.FileInput(attrs={
                'class': 'custom-file-input',
                'accept': '.pdf',
                'required': True
            }),
            'file_title_academic': forms.FileInput(attrs={
                'class': 'custom-file-input',
                'accept': '.pdf',
                'required': True
            }),
            'representative_academic_level': forms.Select(attrs={
                'class': 'select2-design',
                'required': True
            }),
            'logo': forms.FileInput(attrs={
                'class': 'custom-file-input',
                'accept': 'image/png, image/jpeg',
                'required': True
            }),
        }
        labels = {
                'adviser': 'Asesor (Opcional)',
        }


class InstitutionDiscountForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_all_field(self.fields)
        FormCommon.update_required_field(self.fields)

    class Meta:
        model = Institutions
        fields = ('discount',)