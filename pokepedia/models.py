from django.db import models


# Create your models here.
class Pokemon(models.Model):
    image = models.URLField()
    name = models.CharField(max_length=100, unique=True)
    genus = models.CharField(max_length=50)
    types = models.ManyToManyField("pokepedia.Type")
    height = models.FloatField()
    weight = models.FloatField()
    flavor_text = models.TextField()
    evolutions = models.ManyToManyField("self")

    def __str__(self):
        return self.name

    def get_weaknesses(self):
        results = []

        types = self.types.all()
        for pokemon_type in types:
            weaknesses = pokemon_type.weaknesses.all()
            for weakness in weaknesses:
                results.append(weakness.name)

        return ", ".join(results)

    def get_evolutions_list(self):
        evolutions_list = []
        for evolution in self.evolutions.all():
            evolutions_list.append(evolution.name)

        return evolutions_list

    def show_types(self):
        return ", ".join([type.name for type in self.types.all()])


class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)
    weaknesses = models.ManyToManyField(
        "self",
        symmetrical=False,
    )

    def __str__(self):
        return self.name
