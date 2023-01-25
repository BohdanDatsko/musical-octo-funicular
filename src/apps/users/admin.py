from allauth.account.admin import EmailAddressAdmin
from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from rest_framework.authtoken.models import Token

from apps.users.forms import UserChangeForm, UserCreationForm

from apps.users.models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ["username", "is_superuser", "email"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ("key", "user", "created")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.unregister(EmailAddress)


@admin.register(EmailAddress)
class MyEmailAddressAdmin(EmailAddressAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
