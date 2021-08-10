from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, GroupPerson,QuestionsPull,TestResults

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

class TestQuestionsAdmin(ModelAdmin):
    model = QuestionsPull
    list_display = ('question','answer','factor','data_created','data_update',)
    fieldsets = (
        (None, {'fields': ('question','answer','factor',)}),
    )

    search_fields = ('question','factor',)
    ordering = ('question','data_created','factor',)
    read_only = ('data_created','data_update')




class GroupAdmin(ModelAdmin):
    model = GroupPerson
    list_display = ('Name_Group','max_test_factor','pass_test_factor')
    fieldsets = (
        (None, {'fields': ('Name_Group','max_test_factor','pass_test_factor')}),
    )

    search_fields = ('Name_Group',)
    ordering = ('Name_Group','max_test_factor','pass_test_factor')
    read_only = ('data_created','data_update')



class TestingAdmin(ModelAdmin):
    model = TestResults
    list_display = ('tested_user','test_result','test_mark')
    search_fields = ('tested_user',)
    ordering = ('tested_user','test_result','test_mark')
    read_only = ('tested_user','test_result','test_mark')



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(GroupPerson, GroupAdmin)
admin.site.register(QuestionsPull,TestQuestionsAdmin)
admin.site.register(TestResults,TestingAdmin)