from django import forms

from advisers.choices import TL_YEAR, TL_MONTH
from advisers.models import AdvisersCommissions, PeriodCommissions, Advisers, PaymentAdviserCommissions, ManagersCommissions, \
    Managers, PaymentMethod
from core.common.form.form_common import FormCommon


class AdvisersCommissionsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_required_field(self.fields)

    class Meta:
        model = AdvisersCommissions
        fields = '__all__'


class ManagersCommissionsForm(forms.ModelForm):
    class Meta:
        model = ManagersCommissions
        fields = '__all__'


class PeriodCommissionsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_all_field(self.fields)

    class Meta:
        model = PeriodCommissions
        fields = '__all__'
        exclude = ('manager_percentage', 'manager_percentage_max')
        widgets = {
            'days_commissions_period_1': forms.TextInput(attrs={
                'class': 'bg-light',
                'readonly': True
            }),
            'days_commissions_period_2': forms.TextInput(attrs={
                'class': 'bg-light',
                'readonly': True
            }),
            'days_commissions_period_3': forms.TextInput(attrs={
                'class': 'bg-light',
                'readonly': True
            }),
            'advisers_percentage_max_period_1': forms.TextInput(attrs={
                'class': 'bg-light',
                'readonly': True
            }),
            'advisers_percentage_max_period_2': forms.TextInput(attrs={
                'class': 'bg-light',
                'readonly': True
            }),
            'advisers_percentage_max_period_3': forms.TextInput(attrs={
                'class': 'bg-light',
                'readonly': True
            }),
        }

    advisers_specific = forms.ModelChoiceField(
        widget=forms.SelectMultiple(attrs={'class': "select2 select2-design"}),
        queryset=Advisers.objects.none(),
        label='Asesores especificos',
        required=False,
    )


class PeriodCommissionsManagerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_all_field(self.fields)

    class Meta:
        model = PeriodCommissions
        fields = ('manager_percentage', 'manager_percentage_max')
        widgets = {
            'manager_percentage_max': forms.TextInput(attrs={
                'class': 'bg-light',
                'readonly': True
            }),
        }

    managers_specific = forms.ModelChoiceField(
        widget=forms.SelectMultiple(attrs={'class': "select2 select2-design"}),
        queryset=Managers.objects.filter(deleted=False),
        label='Gerentes especificos',
        required=False,
    )


class PaymentAdviserCommissionsForm(forms.ModelForm):
    class Meta:
        model = PaymentAdviserCommissions
        fields = ('type_functionary', 'month', 'year')

        widgets = {
            'type_functionary': forms.Select(attrs={'class': "select2 select2-design"}),
            'month': forms.Select(attrs={'class': "select2 select2-design"}),
            'year': forms.Select(attrs={'class': "select2 select2-design"}),
        }


class AdviserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_required_field(self.fields)

    class Meta:
        model = Advisers
        fields = '__all__'
        exclude = ('deleted', 'manager', 'user')


class AdviserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_readonly_field([self.fields['code'], self.fields['email']], is_list=True)
        FormCommon.update_required_field(self.fields)

    class Meta:
        model = Advisers
        fields = '__all__'
        exclude = ('deleted', 'manager', 'user')


class ManagerProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_readonly_field([self.fields['code'], self.fields['email']], is_list=True)
        FormCommon.update_required_field(self.fields)

    class Meta:
        model = Managers
        fields = '__all__'
        exclude = ('deleted', 'user')


class PaymentMethodForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_required_field(self.fields, excludes=('is_default',))

    class Meta:
        model = PaymentMethod
        fields = '__all__'
        exclude = ('deleted', 'user')
