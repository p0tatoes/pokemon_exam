from django import forms

from pokepedia.models import Pokemon, Type


class PokemonSearchForm(forms.Form):
    # POKEMON_TYPES = [
    #     [pokemon_type.pk, pokemon_type.name] for pokemon_type in Type.objects.all()
    # ]

    pokemon_name = forms.CharField(
        max_length=100,
        required=False,
    )
    pokemon_type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        required=False,
    )


class PokemonForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["evolutions"].queryset = Pokemon.objects.exclude(
                id=self.instance.id,
            )
