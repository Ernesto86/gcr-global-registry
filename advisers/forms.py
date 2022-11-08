from django import forms

from advisers.choices import TL_YEAR, TL_MONTH
from advisers.models import AdvisersCommissions, PeriodCommissions, Advisers, PaymentAdviserCommissions


class AdvisersCommissionsForm(forms.ModelForm):
    class Meta:
        model = AdvisersCommissions
        fields = '__all__'


class PeriodCommissionsForm(forms.ModelForm):
    class Meta:
        model = PeriodCommissions
        fields = '__all__'
        exclude = ('manager_percentage', 'manager_percentage_max')
        widgets = {
            'days_commissions_period_1': forms.TextInput(attrs={
                'class': 'bg-light',
                'disabled': True
            }),
            'days_commissions_period_2': forms.TextInput(attrs={
                'class': 'bg-light',
                'disabled': True
            }),
            'days_commissions_period_3': forms.TextInput(attrs={
                'class': 'bg-light',
                'disabled': True
            }),
            'advisers_percentage_max_period_1': forms.TextInput(attrs={
                'class': 'bg-light',
                'disabled': True
            }),
            'advisers_percentage_max_period_2': forms.TextInput(attrs={
                'class': 'bg-light',
                'disabled': True
            }),
            'advisers_percentage_max_period_3': forms.TextInput(attrs={
                'class': 'bg-light',
                'disabled': True
            }),
        }

    advisers_specific = forms.ModelChoiceField(
        widget=forms.SelectMultiple(attrs={'class': "select2 select2-design"}),
        queryset=Advisers.objects.filter(deleted=False),
        label='Asesores especificos',
        required=False,
    )


class PaymentAdviserCommissionsForm(forms.ModelForm):
    class Meta:
        model = PaymentAdviserCommissions
        fields = '__all__'

        widgets = {
            'type_functionary': forms.Select(attrs={'class': "select2 select2-design"}),
            'month': forms.Select(attrs={'class': "select2 select2-design"}),
            'year': forms.Select(attrs={'class': "select2 select2-design"}),
        }