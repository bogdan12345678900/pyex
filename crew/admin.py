from django.contrib import admin
from .models import Application, CrewRequest, Rank, Vacancy, VesselType


@admin.register(VesselType)
class VesselTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "kind"]
    search_fields = ["name"]


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ["name", "department"]
    list_filter = ["department"]
    search_fields = ["name"]


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ["rank", "vessel_type", "vessel_name", "salary_usd", "joining_port", "joining_date", "is_active"]
    list_filter = ["is_active", "vessel_type", "rank__department"]
    list_editable = ["is_active"]
    search_fields = ["rank__name", "vessel_name", "joining_port"]
    date_hierarchy = "joining_date"


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["full_name", "rank", "experience_years", "phone", "email", "created_at", "processed"]
    list_filter = ["processed", "rank__department", "rank"]
    list_editable = ["processed"]
    search_fields = ["full_name", "email", "phone"]


@admin.register(CrewRequest)
class CrewRequestAdmin(admin.ModelAdmin):
    list_display = ["company", "contact_person", "vessel_type", "email", "created_at", "processed"]
    list_filter = ["processed", "vessel_type"]
    list_editable = ["processed"]
