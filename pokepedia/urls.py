from django.urls import path

from pokepedia.views import (
    PokemonCreateView,
    PokemonDeleteView,
    PokemonDetailView,
    PokemonListView,
    PokemonUpdateView,
)

urlpatterns = [
    path("", PokemonListView.as_view(), name="pokemon-list"),
    path("<int:pk>", PokemonDetailView.as_view(), name="pokemon-details"),
    path("create/", PokemonCreateView.as_view(), name="pokemon-create"),
    path("<int:pk>/delete/", PokemonDeleteView.as_view(), name="pokemon-delete"),
    path("<int:pk>/update/", PokemonUpdateView.as_view(), name="pokemon-update"),
]
