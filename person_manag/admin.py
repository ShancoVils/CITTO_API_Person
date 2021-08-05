from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, GroupPerson
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email','fio','Official','is_staff', 'is_active','activate_code','person_group')
    list_filter = ('email', 'is_staff', 'is_active','activate_code','person_group')
    fieldsets = (
        (None, {'fields': ('email','fio','Official','password','activate_code','person_group')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','fio','Official', 'password1', 'password2', 'is_staff', 'is_active','person_group')}
        ),
    )
    search_fields = ('email','name',)
    ordering = ('email','name',)
admin.site.register(CustomUser, CustomUserAdmin)



@admin.register(GroupPerson)
class GroupPerson(admin.ModelAdmin):
    list_display = ['id', 'Name_Group']