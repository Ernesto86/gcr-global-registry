from django.forms import ModelForm
from institutions.models import Institutions


class InstitutionForm(ModelForm):
    class Meta:
        model = Institutions
        exclude = ('detail','created_at', 'created_by', 'deleted', 'deleted_at', 'deleted_by', 'deleted_reason')
