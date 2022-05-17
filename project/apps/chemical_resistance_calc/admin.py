from django.contrib import admin

from .models import TableOfChemicalResistance, CalculatorCalculationRequest


@admin.register(TableOfChemicalResistance)
class TableOfChemicalResistanceAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'formula', 'state', 'concentration', 'temperature',
        'pvh', 'pp', 'pvdf', 'hpvh', 'nbr', 'epdm', 'fmk', 'ptfe',
    )


@admin.register(CalculatorCalculationRequest)
class CalculatorCalculationRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'mail_or_phone', 'chemical_resistance',)
