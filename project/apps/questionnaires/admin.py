from django.contrib import admin

from .models import (
    Questionnaire, Question, QuestionnaireResult, QuestionCategory, Answer,
)


class QuestionAdminInline(admin.StackedInline):
    model = Question
    fields = ('ordinal_number', 'title', 'type', 'category','text_hint',)
    ordering = ('ordinal_number',)


class AnswerAdminInline(admin.StackedInline):
    model = Answer
    extra = 0
    min_num = 0


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'pk',)
    exclude = ('pk',)
    raw_id_fields = ('template',)
    inlines = [QuestionAdminInline]

    def get_queryset(self, request):
        qs = super(QuestionnaireAdmin, self).get_queryset(request)
        return qs.exclude(title__icontains='Результат опроса:')


class QuestionnaireAdminInline(admin.StackedInline):
    model = Questionnaire


@admin.register(QuestionnaireResult)
class QuestionnaireResultAdmin(admin.ModelAdmin):
    list_display = ('pk', 'full_name', 'phone', 'created_at',)
    inlines = [AnswerAdminInline]


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'ordinal_number',)
    ordering = ('ordinal_number',)
