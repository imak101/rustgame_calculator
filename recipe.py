import rust_ingredients as ingredient
from ingredient import Ingredient
import enum
import math

class CraftingStation(enum.Enum):
    NONE = "Crafted without a workbench"

    T1 = "Workbench Level 1"
    T2 = "Workbench Level 2"
    T3 = "Workbench Level 3"

    MIXING_TABLE = "Mixing Table"

class Recipe:
    def __init__(self, name: str, ingredients: list[Ingredient], result: Ingredient, crafting_station: CraftingStation, seconds_to_craft: int):
        self.name: str = name
        self.ingredients: list[Ingredient] = ingredients
        self.result: Ingredient = result

        self.crafting_station: CraftingStation = crafting_station
        self.seconds_to_craft: int = seconds_to_craft

    def qty_from(self, ingredients: list[Ingredient]) -> Ingredient:
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

    def ingredients_needed_for(self, units: int) -> list[Ingredient]:
        if units <= 0:
            return []
        if units < self.result.qty:
            units = self.result.qty

        return [item.copy_with_new_qty(new_qty=(item.qty * units if self.result.qty == 1 else math.floor(item.qty * units / self.result.qty))) for item in self.ingredients]


# Gun Powder
t1_gun_powder = Recipe("Gun Powder T1", ingredients=[ingredient.sulfur(20), ingredient.charcoal(30)], result=ingredient.gun_powder(10), crafting_station=CraftingStation.T1, seconds_to_craft=2)
t23_gun_powder = Recipe("Gun Powder T2/3", ingredients=[ingredient.sulfur(20), ingredient.charcoal(30)], result=ingredient.gun_powder(10), crafting_station=CraftingStation.T2, seconds_to_craft=1)
mixing_table_gun_powder = Recipe("Gun Powder from Mixing Table", ingredients=[ingredient.sulfur(20), ingredient.charcoal(20)], result=ingredient.gun_powder(10), crafting_station=CraftingStation.MIXING_TABLE, seconds_to_craft=1)

# Small Stash
small_stash = Recipe("Small Stash", ingredients=[ingredient.cloth(10)], result=ingredient.small_stash(1), crafting_station=CraftingStation.NONE, seconds_to_craft=15)

# Beancan Grenade
beancan_grenade = Recipe("Beancan Grenade", ingredients=[ingredient.gun_powder(60), ingredient.metal_fragments(20)], result=ingredient.beancan_grenade(1), crafting_station=CraftingStation.T1, seconds_to_craft=10)

# Satchel Charge
satchel_charge = Recipe("Satchel Charge", ingredients=[ingredient.beancan_grenade(4), ingredient.small_stash(1), ingredient.rope(1)], result=ingredient.beancan_grenade(1), crafting_station=CraftingStation.T1, seconds_to_craft=5)
