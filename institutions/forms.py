from django import forms
from institutions.models import Institutions


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institutions
        exclude = ('detail','created_at', 'created_by', 'deleted', 'deleted_at', 'deleted_by', 'deleted_reason')
        widgets = {
            'adviser': forms.Select(attrs={
                'class': 'select2-design',
                'required': False
            }),
            'type_registration': forms.Select(attrs={
                'class': 'select2-design',
                'required': False
            }),
            'logo': forms.FileInput(attrs={
                'class': 'custom-file-input',
                'accept': '.png'
            }),
        }
