from django.contrib import admin

from .models import Affiliate, SocialNetwork, Director, Employee, Partner, TermsOfUseFiles, Requisite


class SocialNetworkAdminInline(admin.StackedInline):
    model = SocialNetwork
    extra = 0
    min_num = 0
    ordering = ('created_at',)


class DirectorAdminInline(admin.StackedInline):
    model = Director
    extra = 0
    raw_id_fields = ('photo',)
    min_num = 0


class EmployeeAdminInline(admin.StackedInline):
    model = Employee
    extra = 0
    min_num = 0
    raw_id_fields = ('photo',)
    ordering = ('created_at',)


class PartnerAdminInline(admin.StackedInline):
    model = Partner
    extra = 0
    min_num = 0
    raw_id_fields = ('logo',)
    ordering = ('created_at',)


@admin.register(Requisite)
class RequisiteAdminInline(admin.ModelAdmin):
    pass


class TermsOfUseFilesAdmin(admin.StackedInline):
    model = TermsOfUseFiles


@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'name', 'company_name', 'logo', 'main_photo', 'phone_up', 'phone_down', 'email', 'city', 'address','requisite',
            'copyright', 'address_storage', 'work_graphic_office', 'work_graphic_storage', 'about', 'slug', 'domens', 'theme', 'latitude', 'longitude', 'latitude_storage', 'longitude_storage',
            )
        }),
    )
    raw_id_fields = ('logo', 'main_photo')
    list_display = ('name', 'address')
    search_fields = ('name',)
    ordering = ('created_at',)
    inlines = [
        TermsOfUseFilesAdmin, SocialNetworkAdminInline, DirectorAdminInline,
        EmployeeAdminInline, PartnerAdminInline
    ]
