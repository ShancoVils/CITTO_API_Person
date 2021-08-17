from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, GroupPerson,QuestionsPull, TestResults

class ActiveteUserFilter(admin.SimpleListFilter):
    title = ('Активирован')
    parameter_name = 'is_active'
    def lookups(self):
           return (
            ('is_active_true', ('Активирован')),
            ('is_active_false', ('Не активирован')),
        )
    def queryset(self, request, queryset):

        if self.value() == 'is_active_true':
            return queryset.filter(is_active=True)

        if self.value() == 'is_active_false':
                    return queryset.filter(is_active=False)

# Форма для админ-панели отображающая модель "Пользователи"

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id','email','fio','official','is_staff', 'is_active','person_group',)
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

# Форма для админ-панели отображающая модель "Вопросы"

class TestQuestionsAdmin(ModelAdmin):
    model = QuestionsPull
    list_display = ('id','question','answer','factor','data_created','data_update')
    fieldsets = (
        (None, {'fields': ('question','answer','factor',)}),
    )
    search_fields = ('question','factor',)
    ordering = ('question','data_created','factor',)
    read_only = ('data_created','data_update')


# Форма для админ-панели отображающая модель "Отделы"

class GroupAdmin(ModelAdmin):
    model = GroupPerson
    list_display = ('id','Name_Group','max_test_factor','pass_test_factor')
    fieldsets = (
        (None, {'fields': ('Name_Group','max_test_factor','pass_test_factor')}),
    )
    search_fields = ('Name_Group',)
    ordering = ('Name_Group','max_test_factor','pass_test_factor')
    read_only = ('data_created','data_update')

# Форма для админ-панели отображающая модель "Результаты тестирования"

class TestingAdmin(ModelAdmin):
    model = TestResults
    list_display = ('id','tested_user','test_questions','test_answers','test_sum_factor','test_result','test_time_begin','test_time_end')
    search_fields = ('tested_user',)
    ordering = ('tested_user','test_questions','test_answers')
    read_only = ('tested_user','test_questions','test_answers')

# Зарегистрированные модели

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(GroupPerson, GroupAdmin)
admin.site.register(QuestionsPull,TestQuestionsAdmin)
admin.site.register(TestResults,TestingAdmin)
