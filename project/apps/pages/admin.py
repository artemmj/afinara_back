from django.contrib import admin

from .models import SolutionForArea, CompleteProject, AboutProduction


class CompleteProjectInline(admin.StackedInline):
    model = CompleteProject
    extra = 0
    min_num = 0
    raw_id_fields = ('photo', 'solution_for_area',)


@admin.register(SolutionForArea)
class SolutionForAreaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [CompleteProjectInline]
    raw_id_fields = ('photo',)
    filter_horizontal = ('products',)


@admin.register(AboutProduction)
class AboutProductionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    raw_id_fields = ('preview_for_mainpage', 'photo',)
