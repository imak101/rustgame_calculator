from crafting_station import *
from rust_ingredients import IngredientKey as ingredient
from rust_ingredients import *

import math

class Recipe:
    def __init__(self, key: IngredientKey, ingredients: list[RustIngredient], result: RustIngredient, crafting_station: CraftingStation, seconds_to_craft: int):
        self.key: IngredientKey = key
        self.name: str = key.value
        self.ingredients: list[RustIngredient] = ingredients
        self.result: RustIngredient = result

        self.crafting_station: CraftingStation = crafting_station
        self.seconds_to_craft: int = seconds_to_craft

    def __repr__(self):
        return f"Recipe: {self.name}, Needs:{self.ingredients} to make {self.result})"

    def qty_from(self, ingredients: list[RustIngredient]) -> RustIngredient:
        # makes a list that contains valid ingredients for this recipe
        # if for example, an ingredient is passed that doesn't have enough to make even one item from the recipe, it gets filtered
        filtered_ingredients = [suppliedIngredient for suppliedIngredient in ingredients
                                for requiredIngredient in self.ingredients
                                if suppliedIngredient.name == requiredIngredient.name and suppliedIngredient.qty >= requiredIngredient.qty]
        # return early if we don't have enough ingredients to make this recipe
        if len(filtered_ingredients) < len(self.ingredients):
            return None

        craft_qty_possible = []
        for supplied_ingredient in filtered_ingredients:
            matched_recipe_ingredient = [item for item in self.ingredients if item == supplied_ingredient][0]
            craft_qty_possible.append(math.floor(supplied_ingredient.qty / matched_recipe_ingredient.qty))

        final_qty = min(craft_qty_possible) if self.result.qty == 1 else min(craft_qty_possible) * self.result.qty
        return self.result.copy_with_new_qty(final_qty)

    def ingredients_needed_for(self, units: int) -> list[RustIngredient]:
        if units <= 0:
            return []
        if units < self.result.qty:
            units = self.result.qty

        return [item.copy_with_new_qty(new_qty=(item.qty * units if self.result.qty == 1 else math.floor(item.qty * units / self.result.qty))) for item in self.ingredients]
