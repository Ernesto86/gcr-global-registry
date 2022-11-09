from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import *

class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = [
        "pkid",
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]
    list_display_links = ["id", "email"]
    list_filter = [
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]
    fieldsets = (
        (
            _("Login Credentials"),
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Photo Information"),
            {
                "fields": (
                    "foto",
                )
            },
        ),(
            _("Personal Information"),
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name"
                )
            },
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Institution"),
            {
                "fields": (
                    "institution",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ["email", "username", "first_name", "last_name"]

admin.site.register(User, UserAdmin)
admin.site.register(ModuleGrupCategory)

class ModuleAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'url',
        'name',
        'type_module',
        'visible',
        'order',
        'status'
    )
    list_per_page = 20
    ordering = ('type_module','name')
    search_fields = ('code','name')
    list_filter = (
        'type_module',
        'deleted',
    )
    def status(self, obj):
        return not obj.deleted
    status.boolean = True

admin.site.register(Module, ModuleAdmin)

class ModuleGrupPermissionsAdmin(admin.ModelAdmin):
    list_display = (
        'description',
        'main_category',
        'group',
        'module',
        'priority',
        'status',
    )
    list_per_page = 20
    ordering = ('priority',)
    search_fields = ('description',)
    list_filter = (
        'deleted',
    )
    def status(self, obj):
        return not obj.deleted
    status.boolean = True

admin.site.register(ModuleGrupPermissions,ModuleGrupPermissionsAdmin)
