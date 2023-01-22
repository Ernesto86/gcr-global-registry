from core.common.form.form_common import FormCommon
from system.models import AcademicLevel
from .models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ["email", "username", "first_name", "last_name"]
        error_class = "error"


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name"]
        error_class = "error"


class SignUpRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_all_field(self.fields, with_place_holder_cover=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        error_class = "error"


class AcademicLevelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FormCommon.update_required_field(self.fields)

    class Meta:
        model = AcademicLevel
        fields = '__all__'
        exclude = ('deleted',)