from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, GroupPerson

class ActiveteUserFilter(admin.SimpleListFilter):
    title = ('Активирован')
    parameter_name = 'is_active'
    def lookups(self, request, model_admin):
           return (
            ('is_active_true', ('Активирован')),
            ('is_active_false', ('Не активирован')),
        )
    def queryset(self, request, queryset):

        if self.value() == 'is_active_true':
            return queryset.filter(is_active=True)

        if self.value() == 'is_active_false':
                    return queryset.filter(is_active=False)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email','fio','official','is_staff', 'is_active','person_group',)
    list_filter = (ActiveteUserFilter,)
    fieldsets = (
        (None, {'fields': ('email','last_name','namej','first_name','official','password','activate_code','person_group')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','last_name','namej','first_name','official', 'password1', 'password2', 'is_staff', 'is_active','person_group')}
        ),
    )
    search_fields = ('email','fio')
    ordering = ('email','first_name','official','is_staff', 'is_active','person_group')
    read_only = ('email','fio')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(GroupPerson)
