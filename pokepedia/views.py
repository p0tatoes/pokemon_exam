from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from pokepedia.forms import PokemonForm, PokemonSearchForm
from pokepedia.models import Pokemon


# Create your views here.
class PokemonListView(ListView):
    model = Pokemon
    context_object_name = "pokemon_list"
    template_name = "pokemon-list.html"

    form = PokemonSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = PokemonSearchForm(self.request.GET)

        if form.is_valid():
            pokemon_name = form.cleaned_data["pokemon_name"]
            pokemon_type = form.cleaned_data["pokemon_type"]

            if pokemon_name and pokemon_type:
                queryset = Pokemon.objects.filter(name__icontains=pokemon_name).filter(
                    types__name=pokemon_type
                )
            elif pokemon_name:
                queryset = Pokemon.objects.filter(name__icontains=pokemon_name)
            elif pokemon_type:
                queryset = Pokemon.objects.filter(types__name=pokemon_type)

        return queryset


class PokemonDetailView(DetailView):
    model = Pokemon
    context_object_name = "pokemon"
    template_name = "pokemon-details.html"


class PokemonCreateView(LoginRequiredMixin, CreateView):
    model = Pokemon
    form_class = PokemonForm
    template_name = "pokemon-form.html"
    success_url = reverse_lazy("pokemon-list")


class PokemonUpdateView(LoginRequiredMixin, UpdateView):
    model = Pokemon
    form_class = PokemonForm
    template_name = "pokemon-form.html"
    success_url = reverse_lazy("pokemon-list")


class PokemonDeleteView(LoginRequiredMixin, DeleteView):
    model = Pokemon
    context_object_name = "pokemon"
    template_name = "pokemon-delete.html"
    success_url = reverse_lazy("pokemon-list")
