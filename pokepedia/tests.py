from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from pokepedia.models import Pokemon, Type


class TypeModelTests(TestCase):
    def setUp(self):
        self.fire = Type.objects.create(name="Fire")
        self.water = Type.objects.create(name="Water")
        self.grass = Type.objects.create(name="Grass")

        # Set up weaknesses
        self.fire.weaknesses.add(self.water)
        self.water.weaknesses.add(self.grass)
        self.grass.weaknesses.add(self.fire)

    def test_type_creation(self):
        """Is pokemon Type resource with name `Fire` created?"""
        self.assertEqual(self.fire.name, "Fire")
        self.assertTrue(isinstance(self.fire, Type))
        self.assertEqual(str(self.fire), "Fire")

    def test_type_weaknesses(self):
        """Is `Fire` type pokemon weak to `Water` types?"""
        self.assertEqual(self.fire.get_weaknesses(), "Water")

        """Is `Water` type pokemon weak to `Grass` types?"""
        self.assertEqual(self.water.get_weaknesses(), "Grass")

        """Is `Grass` type pokemon weak to `Firer` types?"""
        self.assertEqual(self.grass.get_weaknesses(), "Fire")


class PokemonModelTests(TestCase):
    def setUp(self):
        self.fire = Type.objects.create(name="Fire")
        self.flying = Type.objects.create(name="Flying")
        self.water = Type.objects.create(name="Water")

        self.charizard = Pokemon.objects.create(
            image="https://example.com/charizard.jpg",
            name="Charizard",
            genus="Flame Pokemon",
            height=1.7,
            weight=90.5,
            flavor_text="Breathes fire of such great heat that it melts anything.",
        )
        self.charizard.types.add(self.fire, self.flying)

        self.charmeleon = Pokemon.objects.create(
            image="https://example.com/charmeleon.jpg",
            name="Charmeleon",
            genus="Flame Pokemon",
            height=1.1,
            weight=19.0,
            flavor_text="When it swings its burning tail, it elevates the temperature.",
        )

        # Set up evolution chain
        self.charizard.evolutions.add(self.charmeleon)

    def test_pokemon_creation(self):
        """Is pokemon `Charizard` created?"""
        self.assertEqual(self.charizard.name, "Charizard")
        self.assertTrue(isinstance(self.charizard, Pokemon))
        self.assertEqual(str(self.charizard), "Charizard")

    def test_pokemon_types(self):
        """Does `Charizard` have `Fire` and `Flying` types assigned?"""
        self.assertEqual(self.charizard.get_types(), "Fire, Flying")

    def test_pokemon_evolutions(self):
        """Does `Charizard` have `Charmeleon` in its evolution tree/chan (and vice versa)?"""
        self.assertEqual(self.charizard.get_evolutions_list(), ["Charmeleon"])
        self.assertEqual(self.charmeleon.get_evolutions_list(), ["Charizard"])

    def test_pokemon_weaknesses(self):
        """Does `Charizard` (Fire-type pokemon) have weakness to the `Water` type?"""
        # Assuming Fire is weak to Water
        self.fire.weaknesses.add(self.water)
        self.assertEqual(self.charizard.get_weaknesses(), "Water")


# class PokemonFormTests(TestCase):
#     def setUp(self):
#         self.fire = Type.objects.create(name="Fire")
#         self.pokemon = Pokemon.objects.create(
#             image="https://example.com/charizard.jpg",
#             name="Charizard",
#             genus="Flame Pokemon",
#             height=1.7,
#             weight=90.5,
#             flavor_text="Breathes fire of such great heat that it melts anything.",
#         )

#     def test_pokemon_form_valid(self):
#         """Is `Charizard` pokemon created from create form?"""
#         form_data = {
#             "image": "https://example.com/charizard.jpg",
#             "name": "Charizard",
#             "genus": "Flame Pokemon",
#             "height": 1.7,
#             "weight": 90.5,
#             "flavor_text": "Breathes fire of such great heat that it melts anything.",
#             "types": [self.fire.id],
#         }
#         form = PokemonForm(data=form_data)
#         self.assertTrue(form.is_valid())

#     def test_pokemon_search_form_valid(self):
#         """Is `Charizard` shown as a search result in the search form?"""
#         form_data = {
#             "pokemon_name": "Charizard",
#             "pokemon_type": self.fire.id,
#         }
#         form = PokemonSearchForm(data=form_data)
#         self.assertTrue(form.is_valid())


class PokemonViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.fire = Type.objects.create(name="Fire")
        self.water = Type.objects.create(name="Water")

        self.charizard = Pokemon.objects.create(
            image="https://example.com/charizard.jpg",
            name="Charizard",
            genus="Flame Pokemon",
            height=1.7,
            weight=90.5,
            flavor_text="Breathes fire of such great heat that it melts anything.",
        )
        self.charizard.types.add(self.fire)

        # Create test user for authenticated views
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_pokemon_list_view(self):
        """Is pokemon list view returned/displayed successfully?"""
        response = self.client.get(reverse("pokemon-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pokemon-list.html")
        self.assertIn("pokemon_list", response.context)
        self.assertIn("form", response.context)

    def test_pokemon_detail_view(self):
        """Is pokemon details view for `Charizard` returned/displayed successfully?"""
        response = self.client.get(
            reverse("pokemon-details", kwargs={"pk": self.charizard.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pokemon-details.html")
        self.assertEqual(response.context["pokemon"], self.charizard)

    def test_pokemon_search(self):
        """Is `Charizard` included in the search results?"""
        response = self.client.get(
            reverse("pokemon-list"),
            {"pokemon_name": "Charizard", "pokemon_type": self.fire.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.charizard, response.context["pokemon_list"])

    def test_pokemon_create_view_authenticated(self):
        """Is pokemon create view accessible to authenticated users?"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("pokemon-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pokemon-form.html")

    def test_pokemon_create_view_unauthenticated(self):
        """Is pokemon create view not accessible to unauthenticated users?"""
        response = self.client.get(reverse("pokemon-create"))
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_pokemon_update_view_authenticated(self):
        """Is pokemon update view accessible to authenticated users?"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("pokemon-update", kwargs={"pk": self.charizard.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pokemon-form.html")

    def test_pokemon_update_view_unauthenticated(self):
        """Is pokemon update view not accessible to unauthenticated users?"""
        response = self.client.get(
            reverse("pokemon-update", kwargs={"pk": self.charizard.pk})
        )
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_pokemon_delete_view_authenticated(self):
        """Is pokemon delete view accessible to authenticated users?"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("pokemon-delete", kwargs={"pk": self.charizard.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pokemon-delete.html")

    def test_pokemon_delete_view_unauthenticated(self):
        """Is pokemon delete view not accessible to unauthenticated users?"""
        response = self.client.get(
            reverse("pokemon-delete", kwargs={"pk": self.charizard.pk})
        )
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_pokemon_create_post_success(self):
        """Can create a pokemon from create view?"""
        self.client.login(username="testuser", password="testpass123")
        new_pokemon_data = {
            "image": "https://example.com/squirtle.jpg",
            "name": "Squirtle",
            "genus": "Tiny Turtle Pokemon",
            "height": 0.5,
            "weight": 9.0,
            "flavor_text": "Shoots water at prey while in the water.",
            "types": [self.water.id],
        }
        response = self.client.post(reverse("pokemon-create"), new_pokemon_data)

        self.assertEqual(response.status_code, 200)

        # Verify pokemon was created
        created_pokemon = Pokemon.objects.get(name="Squirtle")
        self.assertEqual(created_pokemon.genus, "Tiny Turtle Pokemon")
        self.assertEqual(created_pokemon.height, 0.5)
        self.assertEqual(created_pokemon.weight, 9.0)
        self.assertEqual(list(created_pokemon.types.all()), [self.water])

    def test_pokemon_create_invalid_data(self):
        """Displays warnings about errors in the page when submitting invalid data?"""
        self.client.login(username="testuser", password="testpass123")
        invalid_data = {
            "image": "not-a-url",  # Invalid URL
            "name": "",  # Required field
            "genus": "Test Pokemon",
            "height": -1.0,  # Invalid negative height
            "weight": 0,
        }
        response = self.client.post(reverse("pokemon-create"), invalid_data)

        # Should stay on the same page with errors
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pokemon-form.html")

        # Verify form errors
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertEqual(form.errors["name"], ["This field is required."])
        self.assertIn("image", form.errors)

        # Verify no pokemon was created
        self.assertFalse(Pokemon.objects.filter(genus="Test Pokemon").exists())

    def test_pokemon_create_duplicate_name(self):
        """Does not create duplicate pokemon entries?"""
        self.client.login(username="testuser", password="testpass123")
        duplicate_pokemon_data = {
            "image": "https://example.com/charizard2.jpg",
            "name": "Charizard",  # Already exists
            "genus": "Flame Pokemon",
            "height": 1.7,
            "weight": 90.5,
            "flavor_text": "Another Charizard description.",
            "types": [self.fire.id],
        }
        response = self.client.post(reverse("pokemon-create"), duplicate_pokemon_data)

        # Should stay on the same page with errors
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pokemon-form.html")

        # Verify form error about unique constraint
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertTrue(any("already exists" in error for error in form.errors["name"]))

    def test_pokemon_create_with_evolutions(self):
        """Can create a pokemon with evolution tree/chain from create view?"""
        self.client.login(username="testuser", password="testpass123")
        new_pokemon_data = {
            "image": "https://example.com/wartortle.jpg",
            "name": "Wartortle",
            "genus": "Turtle Pokemon",
            "height": 1.0,
            "weight": 22.5,
            "flavor_text": "Often hides in water to stalk unwary prey.",
            "types": [self.water.id],
            "evolutions": [self.charizard.id],  # Add evolution relationship
        }
        response = self.client.post(reverse("pokemon-create"), new_pokemon_data)

        # Check redirect to success URL
        self.assertEqual(response.status_code, 302)

        # Verify pokemon was created with evolution
        created_pokemon = Pokemon.objects.get(name="Wartortle")
        self.assertTrue(self.charizard in created_pokemon.evolutions.all())

    def test_pokemon_create_multiple_types(self):
        """Can create a pokemon with multiple types from create view?"""
        self.client.login(username="testuser", password="testpass123")
        self.dragon = Type.objects.create(name="Dragon")
        new_pokemon_data = {
            "image": "https://example.com/gyarados.jpg",
            "name": "Gyarados",
            "genus": "Atrocious Pokemon",
            "height": 6.5,
            "weight": 235.0,
            "flavor_text": "Rarely seen in the wild.",
            "types": [self.water.id, self.dragon.id],  # Multiple types
        }
        response = self.client.post(reverse("pokemon-create"), new_pokemon_data)

        self.assertEqual(response.status_code, 200)

        # Verify pokemon was created with multiple types
        created_pokemon = Pokemon.objects.get(name="Gyarados")
        self.assertEqual(set(created_pokemon.types.all()), {self.water, self.dragon})

    def test_pokemon_update_post_success(self):
        """Does update form successfully update `Charizard` pokemon data?"""
        self.client.login(username="testuser", password="testpass123")
        update_data = {
            "image": "https://example.com/charizard-mega.jpg",
            "name": "Mega Charizard",
            "genus": "Flame Pokemon",
            "height": 1.7,
            "weight": 100.5,
            "flavor_text": "Updated flavor text.",
            "types": [self.fire.id, self.water.id],
        }
        response = self.client.post(
            reverse("pokemon-update", kwargs={"pk": self.charizard.pk}), update_data
        )

        self.assertEqual(response.status_code, 200)

        # Verify the update
        updated_pokemon = Pokemon.objects.get(pk=self.charizard.pk)
        self.assertEqual(updated_pokemon.name, "Mega Charizard")
        self.assertEqual(updated_pokemon.weight, 100.5)
        self.assertEqual(updated_pokemon.flavor_text, "Updated flavor text.")
        self.assertEqual(set(updated_pokemon.types.all()), {self.fire, self.water})

    def test_pokemon_update_invalid_data(self):
        """Does invalid data not update pokemon data?"""
        self.client.login(username="testuser", password="testpass123")
        invalid_data = {
            "name": "",  # Name is required
            "genus": "Flame Pokemon",
            "height": 1.7,
            "weight": 100.5,
        }
        response = self.client.post(
            reverse("pokemon-update", kwargs={"pk": self.charizard.pk}), invalid_data
        )
        self.assertEqual(response.status_code, 200)  # Returns to form
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertEqual(form.errors["name"], ["This field is required."])

    def test_pokemon_delete_confirmation(self):
        """Is pokemon deleted successfully?"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("pokemon-delete", kwargs={"pk": self.charizard.pk})
        )
        self.assertEqual(response.status_code, 302)  # Redirects to success URL
        self.assertFalse(Pokemon.objects.filter(pk=self.charizard.pk).exists())

    def test_pokemon_delete_nonexistent(self):
        """Does it return a 404 when trying to delete a non-existing pokemon"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse("pokemon-delete", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)
