from django.contrib import admin

from pokepedia.models import Pokemon

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
        "pk",
        "image",
        "name",
        "genus",
        "show_types",
        "height",
        "weight",
        "flavor_text",
    ]
    list_filter = ["types", "genus"]
    search_fields = ["name"]


admin.site.register(Pokemon, PokemonAdmin)
