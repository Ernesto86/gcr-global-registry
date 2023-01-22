import datetime

from django import forms

from core.common.form.form_common import FormCommon
from students.models import StudentRegisters, Students
from system.models import SysCountries


class StudentRegistersForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_all_field(self.fields)

    class Meta:
        model = StudentRegisters
        fields = (
            'student',
            'type_register',
            'certificate',
            'country',
            'date_issue',
        )
        widgets = {
            'student': forms.Select(attrs={
                'readonly': True,
                'class': FormCommon.CLS_BACKGROUND_READONLY
            }),
            'type_register': forms.Select(
                attrs={
                    'required': True
                },
            ),
            'certificate': forms.TextInput(
                attrs={
                    'required': True
                }
            ),
            'country': forms.Select(
                attrs={
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
        }


class StudentRegistersSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
        FormCommon.update_all_field(self.fields)

    identification = forms.CharField(widget=forms.TextInput(), label='Identificación del estudiante', required=True)
    country = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': "select2", 'placeholder': 'Todos...'}),
        queryset=SysCountries.objects.all(),
        label='Pais',
        required=True,
    )
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
            'email': forms.EmailInput(
                attrs={
                    'required': True
                },
            )
        }
