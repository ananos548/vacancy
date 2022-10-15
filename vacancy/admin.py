from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Vacancy, Specialty, Company


@admin.register(Vacancy)
class VacancyAdmin(ModelAdmin):
    pass


@admin.register(Specialty)
class SpecialtyAdmin(ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    pass
