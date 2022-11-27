import datetime

from django import forms

from core.common.form.form_common import FormCommon
from students.models import StudentRegisters, Students


class StudentRegistersForm(forms.ModelForm):
    class Meta:
        model = StudentRegisters
        fields = (
            'student',
            'type_register',
            'certificate',
            'country',
            'date_issue',
            'code_international_register'
        )
        widgets = {
            'student': forms.Select(attrs={
                'readonly': True
            }),
            'type_register': forms.Select(
                attrs={
                    'class': 'select2-design',
                    'required': True
                },
            ),
            'certificate': forms.Select(
                attrs={
                    'class': 'select2-design',
                    'required': True
                }
            ),
            'country': forms.Select(
                attrs={
                    'class': 'select2-design',
                    'required': True
                }
            ),
            'date_issue': forms.DateInput(
                attrs={
                    'class': 'date-piker',
                    'type': 'date',
                    'required': True,
                    'value': datetime.datetime.now().date()
                }
            ),
            'code_international_register': forms.TextInput(attrs={
                'readonly': True,
            }),
        }


class StudentRegistersSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
        FormCommon.update_all_field(self.fields)

    identification = forms.CharField(widget=forms.TextInput(), label='Identificación del estudiante', required=True)
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'readonly': True
            }
        ),
        label='Nombre del estudiante'
    )


class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = (
            'dni',
            'first_name',
            'last_name',
            'country',
            'gender',
            'email'
        )
        widgets = {
            'country': forms.Select(
                attrs={
                    'class': 'select2-design',
                    'required': True
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'required': True
                },
            )
        }
