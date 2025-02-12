from django.views.generic import ListView

from pokepedia.models import Pokemon


# Create your views here.
class PokemonListView(ListView):
    model = Pokemon
    context_object_name = "pokemon_list"
    template_name = "pokemon-list.html"
