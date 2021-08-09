from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, GroupPerson
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email','fio','official','is_staff', 'is_active','person_group',)
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email','fio','last_name','namej','first_name','official','password','activate_code','person_group')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','last_name','namej','first_name','official', 'password1', 'password2', 'is_staff', 'is_active','person_group')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email','first_name','official','is_staff', 'is_active','person_group')
    read_only = ('email','fio')

    def fio(self, obj):
        return obj.fio()





admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(GroupPerson)
