from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from .models import Badge, Category, Fund, Company, Rating


class HoldingInline(admin.TabularInline):
    model = Fund.companies.through
    extra = 0


class HoldingReadonlyInline(HoldingInline):
    model = Fund.companies.through
    readonly_fields = ["company", "fund", "percentage"]
    can_delete = False
    max_num = 0


class FundRatingInline(admin.TabularInline):
    model = Fund.ratings.through
    extra = 0


class FundAdmin(admin.ModelAdmin):
    inlines = [
        FundRatingInline,
        HoldingInline,
    ]
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Returns & fees", {"fields": ["returns", "fees"]}),
        ("Badges", {"fields": ["badges"]}),
        (
            "Scores",
            {
                "classes": ["collapse", "horizontal"],
                "fields": [
                    "animal_cruelty_score",
                    "environmental_harm_score",
                    "fossil_fuels_score",
                    "human_rights_violations_score",
                    "social_harm_score",
                    "weapons_score",
                ],
            },
        ),
    ]
    list_display = [
        "name",
        "animal_cruelty_score",
        "environmental_harm_score",
        "fossil_fuels_score",
        "human_rights_violations_score",
        "social_harm_score",
        "weapons_score",
    ]
    readonly_fields = [
        "animal_cruelty_score",
        "environmental_harm_score",
        "fossil_fuels_score",
        "human_rights_violations_score",
        "social_harm_score",
        "weapons_score",
    ]


class CompanyAdmin(admin.ModelAdmin):
    inlines = [
        HoldingReadonlyInline,
    ]
    exclude = ["companies"]
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
    list_display = [
        "name",
        "animal_cruelty",
        "environmental_harm",
        "fossil_fuels",
        "human_rights_violations",
        "social_harm",
        "weapons",
    ]


class RatingAdmin(admin.ModelAdmin):
    list_display = ["name", "short_desc"]


admin.site.register(Fund, FundAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Category)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Badge)
