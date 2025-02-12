from django.forms import ModelForm

from pokepedia.models import Pokemon


class PokemonSearchForm(ModelForm):
    class Meta:
        model = Pokemon
        fields = ["name", "types"]


class PokemonForm(ModelForm):
    class Meta:
        model = Pokemon
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["evolutions"].queryset = Pokemon.objects.exclude(
                id=self.instance.id,
            )
