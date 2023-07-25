from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import *
from django.contrib.auth import get_user_model
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


User = get_user_model()

admin.site.register(ekon)

admin.site.register(Device)

admin.site.register(Test)

admin.site.register(RefDr)

admin.site.register(Visit)

admin.site.register(patientcategory)

admin.site.register(Scansummary)

admin.site.register(Devicecheck)