from django.contrib import admin

from language_tests.models import Answer, LanguageTestType


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer',)
    list_display_links = ('id', 'answer',)
    search_fields = ('answer',)


class LanguageTestTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_published',)
    list_display_links = ('id', 'name',)
    list_editable = ('is_published',)
    search_fields = ('name',)


admin.site.register(Answer, AnswerAdmin)
admin.site.register(LanguageTestType, LanguageTestTypeAdmin)
