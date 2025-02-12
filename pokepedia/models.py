from django.db import models


# Create your models here.
class Pokemon(models.Model):
    image = models.URLField()
    name = models.CharField(max_length=100)
    genus = models.CharField(max_length=50)
    types = models.ManyToManyField("pokepedia.Type")
    height = models.FloatField()
    weight = models.FloatField()
    flavor_text = models.TextField()

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)
    weaknesses = models.ManyToManyField(
        "self",
        symmetrical=False,
    )

    def __str__(self):
        return self.name
