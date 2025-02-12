from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from pokepedia.forms import PokemonForm
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
    model = Pokemon
    form_class = PokemonForm
    template_name = "pokemon-form.html"
    success_url = reverse_lazy("pokemon-list")


class PokemonUpdateView(UpdateView):
    model = Pokemon
    form_class = PokemonForm
    template_name = "pokemon-form.html"
    success_url = reverse_lazy("pokemon-list")


class PokemonDeleteView(DeleteView):
    model = Pokemon
    context_object_name = "pokemon"
    template_name = "pokemon-delete.html"
    success_url = reverse_lazy("pokemon-list")
