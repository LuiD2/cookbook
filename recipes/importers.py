# Utility class to ingest structured text as a recipe

import yaml
import logging
from recipes.models import Recipe, Ingredient, RecipeIngredient, IngredientUnit, RecipeTag

def get_log_level(name):
    levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR
    }
    try:
        return levels[name]
    except KeyError:
        raise ValueError("Invalid log level name {}. Choose one of {}.".format(
            name, ", ".join(levels.keys())
        ))

def get_logger(logName, fileName, level):
    "Gets a preconfigured logger"
    log = logging.getLogger(logName)
    log.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fh = logging.FileHandler(fileName)
    sh = logging.StreamHandler()
    for h in [fh, sh]:
        h.setLevel(level)
        h.setFormatter(formatter)
        log.addHandler(h)
    return log

class RecipeImporter:
    """
    Imports a data structure as a recipe:
    {
        name: str,
        source: url,
        servings: int,
        notes: str,
        ingredients: [qty, unit, ingerdient, notes?],
        steps: [str]
    }
    """
    def __init__(self, log=None):
        self.log = log or get_logger(__file__, "recipe_importer.log", logging.WARNING)

    def import_recipe(self, data):
        self.r = Recipe(
            name=data['name'],
            source=data['source'],
            servings=data['servings'],
            notes=data.get('notes'),
        )
        self.r.save()
        self.log.info("Created recipe {}".format(self.r))
        counter = 1
        self.r.stepsAndIngredients += "{\"steps\":["
        for s in data['steps']:
            if(len(data['steps']) == counter):
                self.r.stepsAndIngredients += "\"" + str(counter) + ". " + str(s) + "\""
            else:
                self.r.stepsAndIngredients += "\"" + str(counter) + ". " + str(s) + "\","
            counter += 1
            self.r.save()

        self.r.stepsAndIngredients += "], \"ingredients\":["
        self.r.save()
        for i in data['ingredients']:
            self.import_ingredient(*i)
        self.r.stepsAndIngredients = self.r.stepsAndIngredients.rstrip(self.r.stepsAndIngredients[-1]) + "]}"
        self.r.save()
        for tagName in data.get('tags', []):
            tag, _ = RecipeTag.objects.get_or_create(name=tagName)
            self.r.tags.add(tag)

    def import_ingredient(self, quantity, unit, name, notes=None):
        "Parses a string as a RecipeIngredient"
        ingredient, created = Ingredient.objects.get_or_create(name=name)
        self.log.info("{} ingredient {}".format("Created" if created else "Loaded", ingredient))
        try:
            ingUnit = IngredientUnit.lookup(unit)
            self.log.info("Loaded ingredient unit {}".format(ingUnit))
        except IngredientUnit.DoesNotExist:
            ingUnit = IngredientUnit.objects.create(name=unit, short=unit)
            self.log.info("Created ingredient unit {}".format(ingUnit))
        ri = self.r.ingredients.create(
            ingredient=ingredient, 
            unit=ingUnit,
            recipe = self.r,
            quantity = quantity,
            notes = notes
        )
        self.r.stepsAndIngredients += "\"" + str(quantity) + " " + str(ingUnit) + " " + str(ingredient) + ("" if str(notes) == "None" else " " + str(notes)) + "\","
        self.r.save()
        self.log.info("Added {}".format(ri))

class YAMLRecipeImporter(RecipeImporter):
    def import_recipe(self, path):
        with open(path) as recipeFile:
            super().import_recipe(yaml.load(recipeFile.read()))
