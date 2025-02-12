from django.urls import path

from pokepedia.views import PokemonDetailView, PokemonListView

urlpatterns = [
    path("", PokemonListView.as_view(), name="pokemon-list"),
    path("<int:pk>", PokemonDetailView.as_view(), name="pokemon-details"),
]
