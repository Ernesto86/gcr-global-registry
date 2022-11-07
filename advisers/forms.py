from django import forms
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


TL_MONTH = (
    ("", "----------"),
    (1, "ENERO"),
    (2, "FEBRERO"),
    (3, "MARZO"),
    (4, "ABRIL"),
    (5, "MAYO"),
    (6, "JUNIO"),
    (7, "JULIO"),
    (8, "AGOSTO"),
    (9, "SEPTIEMBRE"),
    (10, "OCTUBRE"),
    (11, "NOVIEMBRE"),
    (12, "DICIEMBRE"),
)


class PaymentAdviserCommissionsForm(forms.ModelForm):
    class Meta:
        model = PaymentAdviserCommissions
        fields = '__all__'

    payment_to = forms.ChoiceField(
        widget=forms.Select(attrs={'class': "select2 select2-design"}),
        choices=PaymentAdviserCommissions.TYPE_FUNCTIONARY,
        label='Pagar a',
        required=True,
    )
    year_option = forms.ChoiceField(
        widget=forms.Select(attrs={'class': "select2 select2-design"}),
        choices=(
            ("", "------------"),
            (2022, 2022),
            (2023, 2023),
            (2024, 2024),
            (2025, 2025),
            (2026, 2026),
            (2027, 2027),
            (2028, 2028),
            (2029, 2029),
            (2030, 2030),
        ),
        label='Año',
        required=True,
    )
    month_option = forms.ChoiceField(
        widget=forms.Select(attrs={'class': "select2 select2-design"}),
        choices=TL_MONTH,
        label='Mes',
        required=True,
    )
