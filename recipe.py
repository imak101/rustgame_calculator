import ingredient
import enum
import math

class CraftingMethod(enum.Enum):
    T1 = "Workbench Level 1"
    T2 = "Workbench Level 2"
    T3 = "Workbench Level 3"

    MIXING_TABLE = "Mixing Table"

class Recipe:
    def __init__(self, name: str, ingredients: list[ingredient.Ingredient], result: ingredient.Ingredient, crafting_method: CraftingMethod, seconds_to_craft: int):
        self.name: str = name
        self.ingredients: list[ingredient.Ingredient] = ingredients
        self.result: ingredient.Ingredient = result

        self.crafting_method: CraftingMethod = crafting_method
        self.seconds_to_craft: int = seconds_to_craft

    def qty_from(self, ingredients: list[ingredient.Ingredient]) -> ingredient.Ingredient:
        # makes a list that contains valid ingredients for this recipe
        # if for example, an ingredient is passed that doesn't have enough to make even one item from the recipe, it gets filtered
        filtered_ingredients = [suppliedIngredient for suppliedIngredient in ingredients
                                for requiredIngredient in self.ingredients
                                if suppliedIngredient.name == requiredIngredient.name and suppliedIngredient.qty >= requiredIngredient.qty]
        # return early if we don't have enough ingredients to make this recipe
        if len(filtered_ingredients) < len(self.ingredients):
            return 0

        craft_qty_possible = []
        for supplied_ingredient in filtered_ingredients:
            matched_recipe_ingredient = [item for item in self.ingredients if item == supplied_ingredient][0]
            craft_qty_possible.append(math.floor(supplied_ingredient.qty / matched_recipe_ingredient.qty))

        final_qty = min(craft_qty_possible) if self.result.qty == 1 else min(craft_qty_possible) * self.result.qty
        return self.result.copy_with_new_qty(final_qty)

    def ingredients_needed_for(self, units: int) -> list[ingredient.Ingredient]:
        if units <= 0:
            return []
        if units < self.result.qty:
            units = self.result.qty

        return [item.copy_with_new_qty(new_qty=(item.qty * units if self.result.qty == 1 else math.floor(item.qty * units / self.result.qty))) for item in self.ingredients]


# Gun Powder
t1_gun_powder = Recipe("Gun Powder T1", ingredients=[ingredient.sulfur(20), ingredient.charcoal(30)], result=ingredient.gun_powder(10), crafting_method=CraftingMethod.T1, seconds_to_craft=2)
t23_gun_powder = Recipe("Gun Powder T2/3", ingredients=[ingredient.sulfur(20), ingredient.charcoal(30)], result=ingredient.gun_powder(10), crafting_method=CraftingMethod.T2, seconds_to_craft=1)
mixing_table_gun_powder = Recipe("Gun Powder from Mixing Table", ingredients=[ingredient.sulfur(20), ingredient.charcoal(20)], result=ingredient.gun_powder(10), crafting_method=CraftingMethod.MIXING_TABLE, seconds_to_craft=1)
