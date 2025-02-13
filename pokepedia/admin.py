from django.contrib import admin

from pokepedia.models import Pokemon, Type

# Register your models here.


class PokemonAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Details",
            {
                "fields": [
                    "image",
                    "name",
                    "genus",
                    "height",
                    "weight",
                    "flavor_text",
                ]
            },
        ),
        ("Types", {"fields": ["types"]}),
        ("Evolutions", {"fields": ["evolutions"]}),
    ]
    list_display = [
        "name",
        "flavor_text",
        "genus",
        "get_types",
        "height",
        "weight",
        "image",
    ]
    list_filter = ["types", "genus"]
    search_fields = ["name"]


class TypeAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Name",
            {
                "fields": ["name"],
            },
        ),
        (
            "Weaknesses",
            {
                "fields": ["weaknesses"],
            },
        ),
    ]
    list_display = ["name", "get_weaknesses"]
    list_filter = ["weaknesses"]
    search_fields = ["name"]


admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(Type, TypeAdmin)
