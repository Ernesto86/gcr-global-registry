from django import forms

from advisers.choices import TL_YEAR, TL_MONTH
from advisers.models import AdvisersCommissions, PeriodCommissions, Advisers, PaymentAdviserCommissions, \
    ManagersCommissions, \
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_required_field(self.fields)

    class Meta:
        model = ManagersCommissions
        fields = '__all__'


# https://stackoverflow.com/questions/673199/disabled-option-for-choicefield-django

# class Select(Select):
#     def create_option(self, *args,**kwargs):
#         option = super().create_option(*args,**kwargs)
#         if not option.get('value'):
#             option['attrs']['disabled'] = 'disabled'
#
#         if option.get('value') == 2:
#             option['attrs']['disabled'] = 'disabled'
#
#         return option

# class SelectWidget(Select):
#     """
#     Subclass of Django's select widget that allows disabling options.
#     """
#     def __init__(self, *args, **kwargs):
#         self._disabled_choices = []
#         super(SelectWidget, self).__init__(*args, **kwargs)
#
#     @property
#     def disabled_choices(self):
#         return self._disabled_choices
#
#     @disabled_choices.setter
#     def disabled_choices(self, other):
#         self._disabled_choices = other
#
#     def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
#         option_dict = super(SelectWidget, self).create_option(
#             name, value, label, selected, index, subindex=subindex, attrs=attrs
#         )
#         if value in self.disabled_choices:
#             option_dict['attrs']['disabled'] = 'disabled'
#         return option_dict

# class MySelect(Select):
#     def __init__(self, attrs=None, choices=(), disabled_choices=()):
#         super(MySelect, self).__init__(attrs, choices=choices)
#         self.disabled_choices = disabled_choices
#
#     def render_option(self, selected_choices, option_value, option_label):
#         if option_value is None:
#             option_value = ''
#         option_value = force_text(option_value)
#         if option_value in selected_choices:
#             selected_html = mark_safe(' selected="selected"')
#             if not self.allow_multiple_selected:
#                 selected_choices.remove(option_value)
#         else:
#             selected_html = ''
#         for key, value in self.disabled_choices:
#             if option_value in key:
#                 return format_html('<option disabled value="{}"{}>{}</option>', option_value, selected_html,
#                                    force_text(option_label))
#         return format_html('<option value="{}"{}>{}</option>', option_value, selected_html, force_text(option_label))


# https://djangosnippets.org/snippets/10646/
#
# from django.forms import Select
#
# class SelectWidget(Select):
#     """
#     Subclass of Django's select widget that allows disabling options.
#     """
#
#     def __init__(self, *args, **kwargs):
#         self._disabled_choices = []
#         super().__init__(*args, **kwargs)
#
#     @property
#     def disabled_choices(self):
#         return self._disabled_choices
#
#     @disabled_choices.setter
#     def disabled_choices(self, other):
#         self._disabled_choices = other
#
#     def create_option(self, name, value, *args, **kwargs):
#         option_dict = super().create_option(name, value, *args, **kwargs)
#         if value in self.disabled_choices:
#             option_dict['attrs']['disabled'] = 'disabled'
#         return option_dict

class PeriodCommissionsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_all_field(self.fields)
        FormCommon.update_readonly_field(
            [
                self.fields['days_commissions_period_1'],
                self.fields['days_commissions_period_2'],
                self.fields['days_commissions_period_3'],
                self.fields['advisers_percentage_max_period_1'],
                self.fields['advisers_percentage_max_period_2'],
                self.fields['advisers_percentage_max_period_3'],
            ],
            is_list=True
        )

    class Meta:
        model = PeriodCommissions
        fields = '__all__'
        exclude = ('manager_percentage', 'manager_percentage_max')

    advisers_specific = forms.ModelChoiceField(
        widget=forms.SelectMultiple(attrs={'class': "select2 select2-design", 'placeholder': 'Todos...'}),
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
        empty_label=None
    )


class PaymentAdviserCommissionsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_required_field(self.fields)
        FormCommon.update_all_field(self.fields)

    class Meta:
        model = PaymentAdviserCommissions
        fields = ('type_functionary', 'month', 'year')


class AdviserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_required_field(self.fields)
        FormCommon.update_readonly_field([self.fields['code']], is_list=True)

    class Meta:
        model = Advisers
        fields = '__all__'
        exclude = ('deleted', 'manager', 'user')


class ManagerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_required_field(self.fields)
        FormCommon.update_readonly_field([self.fields['code']], is_list=True)

    class Meta:
        model = Managers
        fields = '__all__'
        exclude = ('deleted', 'user')


class AdviserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_readonly_field([self.fields['code'], self.fields['email']], is_list=True)
        FormCommon.update_required_field(self.fields)

    class Meta:
        model = Advisers
        fields = '__all__'
        exclude = ('deleted', 'manager', 'user')


class PeriodCommissionsAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_all_field(self.fields)
        FormCommon.update_readonly_field(
            [
                self.fields['advisers_percentage_period_1'],
                self.fields['advisers_percentage_period_2'],
                self.fields['advisers_percentage_period_3'],
                self.fields['manager_percentage']
            ],
            is_list=True)

    class Meta:
        model = PeriodCommissions
        fields = '__all__'


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
        FormCommon.update_all_field(self.fields)

    class Meta:
        model = PaymentMethod
        fields = '__all__'
        exclude = ('deleted', 'user')
