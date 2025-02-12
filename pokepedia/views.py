from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from pokepedia.models import Pokemon


# Create your views here.
class PokemonListView(ListView):
    model = Pokemon
    context_object_name = "pokemon_list"
    template_name = "pokemon-list.html"


class PokemonDetailView(DetailView):
    model = Pokemon
    context_object_name = "pokemon"
    template_name = "pokemon-details.html"


class PokemonCreateView(CreateView):
    pass


class PokemonUpdateView(UpdateView):
    pass


class PokemonDeleteView(DeleteView):
    pass
