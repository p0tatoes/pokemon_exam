from django.urls import path

from pokepedia.views import PokemonListView

urlpatterns = [
    path("", PokemonListView.as_view(), name="pokemon-list"),
]
