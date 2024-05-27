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
        # if len(filtered_ingredients) < len(self.ingredients):
        #     return None
        if len(filtered_ingredients) == 0:
            return None

        craft_qty_possible = []
        for supplied_ingredient in filtered_ingredients:
            matched_recipe_ingredient = [item for item in self.ingredients if item == supplied_ingredient][0]
            craft_qty_possible.append(math.floor(supplied_ingredient.qty / matched_recipe_ingredient.qty))

        final_qty = min(craft_qty_possible) if self.result.qty == 1 else min(craft_qty_possible) * self.result.qty
        return self.result.copy_with_new_qty(final_qty)

    def __ingredients_needed_for_without_extra(self, units: int) -> list[RustIngredient]:
        return [item.copy_with_new_qty(new_qty=(item.qty * units / self.result.qty), extra=0) for item in self.ingredients]

    def ingredients_needed_for(self, units: int) -> list[RustIngredient]:
        # if units < self.result.qty:
        #     units = self.result.qty

        # check if requested amount is divisible by recipe stack amount which means there will be no extras
        if units % self.result.qty == 0:
            return self.__ingredients_needed_for_without_extra(units)

        ingredients_needed_for_closest_stack = self.__ingredients_needed_for_without_extra(self.__find_closest_stack_size(units, self.result))
        return [adjusted_ingredient.copy_with_new_qty(
                    # pure relative quantity to parent ingredient quantity
                    new_qty=(original_ingredient.qty * units / self.result.qty),
                    # how much extra the new ingredient needs to be to reach the closet valid stack size
                    extra=adjusted_ingredient.qty % (original_ingredient.qty * units / self.result.qty))
                for adjusted_ingredient in ingredients_needed_for_closest_stack
                for original_ingredient in self.ingredients
                if adjusted_ingredient == original_ingredient]

    @staticmethod
    def __find_closest_stack_size(wanted_qty: float, ingredient: RustIngredient) -> float:
        crafting_increments = ingredient.qty
        closest_stack_size = crafting_increments
        while closest_stack_size < wanted_qty:
            closest_stack_size += crafting_increments
        return closest_stack_size

