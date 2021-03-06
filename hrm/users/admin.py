from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from hrm.users.forms import UserChangeForm, UserCreationForm
from hrm.users import models

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = auth_admin.UserAdmin.fieldsets
    list_display = ["username", "first_name", "is_superuser"]
    search_fields = ["first_name"]


admin.site.register(models.Organization)
