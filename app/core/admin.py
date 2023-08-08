'''django admin customisation'''

from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# if we ever have to integrate translation in our project, future proofing
from django.utils.translation import gettext_lazy as _
from core import models


class UserAdmin(BaseUserAdmin):
    '''define the admin pages for users'''
    ordering = ['id']
    list_display = ['email', 'name']

    fieldsets = (
        (
            None,
            {
                'fields': (
                  'email',
                  'password'
                )
            }
        ),
        (
            _('Permissions'), {
                'fields': (
                  'is_active',
                  'is_staff',
                  'is_superuser',
                )
            }
        ),
        (
            _('Important Dates'), {
                'fields': (
                    'last_login',
                )
            }
        )
    )
    readonly_fields = ['last_login']

    add_fieldsets = (
        (
            None,
            {
                # custom css classes
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
    )


admin.site.register(models.User, UserAdmin)
# admin.site.register(models.User)
