from django import forms

from core.common.form.form_common import FormCommon
from system.models import SysParameters


class SysParameterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_required_field(
            self.fields,
            excludes=('status', 'extra_data', 'extra_json')
        )
        FormCommon.update_all_field(self.fields)

    class Meta:
        model = SysParameters
        fields = '__all__'
        exclude = ('deleted',)
