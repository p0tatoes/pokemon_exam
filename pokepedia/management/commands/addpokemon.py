from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from requests import HTTPError, get

from pokepedia.models import Pokemon, Type


class Command(BaseCommand):
    help = "Retrieves data from PokeAPI (https://pokeapi.co/api/v2/) for generation 1 pokemon, and stores it to the database"

    # TODO: add option to select which generation to retrieve and store
    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--clear",
    #         action="store_true",
    #         help="clears existing data in the database",
    #     )

    # newest_generation = 9  # Update this when a new generation comes out
    # generations = [gen for gen in range(1, newest_generation + 1)]
    # parser.add_argument(
    #     "generation",
    #     type=int,
    #     choices=generations,
    #     help="[integer] Pokemon generation to retrieve from",
    # )

    def handle(self, *args, **options):
        base_api_url = "https://pokeapi.co/api/v2"

        try:
            self.stdout.write(
                self.style.WARNING("WARNING: Deleting all existing data.")
            )
            call_command("flush", interactive=False)

            # create types
            # assign weaknesses
            # create pokemon
            # assign types
            types_response = get(f"{base_api_url}/type/")
            types_response.raise_for_status()
            type_results = types_response.json()["results"]

            for type in type_results:
                type_name = type["name"]
                type_resource, type_created = Type.objects.get_or_create(name=type_name)

                if type_created:
                    self.stdout.write(
                        self.style.SUCCESS(f"SUCCESS: created type `{type_name}`")
                    )

                response = get(f"{base_api_url}/type/{type_name}")
                response.raise_for_status()
                results = response.json()
                weaknesses = results["damage_relations"]["double_damage_from"]

                for weakness in weaknesses:
                    weakness_name = weakness["name"]
                    weakness_resource, weakness_created = Type.objects.get_or_create(
                        name=weakness_name
                    )
                    type_resource.weaknesses.add(weakness_resource)

                    if weakness_created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"SUCCESS: created type `{weakness_name}`"
                            )
                        )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"SUCCESS: added `{weakness_name}` weakness to type `{type_name}`"
                        )
                    )

            evolution_chains = {}
            for pokemon_index in range(1, 152):
                response = get(f"{base_api_url}/pokemon/{pokemon_index}")
                response.raise_for_status()
                json_response = response.json()

                pokemon_sprite = json_response["sprites"]["front_default"]
                pokemon_name = json_response["name"]
                pokemon_height = json_response["height"]
                pokemon_weight = json_response["weight"]

                species_url = json_response["species"]["url"]
                species_response = get(species_url)
                species_response.raise_for_status()
                json_species_response = species_response.json()
                pokemon_flavor_text = self._get_english_text(
                    json_species_response["flavor_text_entries"],
                    "flavor_text",
                )
                pokemon_genus = self._get_english_text(
                    json_species_response["genera"],
                    "genus",
                )

                evolution_chain_url = json_species_response["evolution_chain"]["url"]
                evolution_chains[pokemon_name] = evolution_chain_url

                pokemon_resource = Pokemon(
                    image=pokemon_sprite,
                    name=pokemon_name,
                    genus=pokemon_genus,
                    height=pokemon_height,
                    weight=pokemon_weight,
                    flavor_text=pokemon_flavor_text,
                )
                pokemon_resource.save()

                for pokemon_type in json_response["types"]:
                    type_name = pokemon_type["type"]["name"]
                    type_resource, type_created = Type.objects.get_or_create(
                        name=type_name,
                    )
                    pokemon_resource.types.add(type_resource)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"SUCCESS: created pokemon `{pokemon_resource}` - {pokemon_resource.types.all()}"
                    )
                )

            processed_chains = set()
            for pokemon_name, evolution_chain_url in evolution_chains.items():
                if evolution_chain_url in processed_chains:
                    continue

                response = get(evolution_chain_url)
                response.raise_for_status()
                chain_data = response.json()

                # Process the evolution chain
                self._process_evolution_chain(chain_data["chain"])
                processed_chains.add(evolution_chain_url)
        except HTTPError as http_err:
            self.stderr.write(self.style.ERROR(http_err))
            raise CommandError("ERROR: Failed to retrieve data from API.")
        except Exception as err:
            call_command("flush", interactive=False)

            self.stderr.write(self.style.ERROR(err))
            raise CommandError("ERROR: Failed to store Pokemon data.")
        else:
            self.stdout.write(self.style.SUCCESS("SUCCESS: Stored Pokemon data :D"))

    def _get_english_text(self, entry_list, key):
        for entry in entry_list:
            if entry["language"]["name"] == "en":
                return entry[key]

        return entry_list[0][key]

    def _process_evolution_chain(self, chain_data, parent=None):
        species_name = chain_data["species"]["name"]
        try:
            current_pokemon = Pokemon.objects.get(name=species_name)

            # If there's a parent, add it to evolutions
            if parent:
                current_pokemon.evolutions.add(parent)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"SUCCESS: added evolution relationship {species_name} -> {parent.name}"
                    )
                )

            for evolution in chain_data["evolves_to"]:
                self._process_evolution_chain(evolution, current_pokemon)

        except Pokemon.DoesNotExist:
            pass
