from recipe import *
from crafting_station import *
from rust_ingredients import IngredientKey as ingredient

mixing_table_recipes: dict[IngredientKey, Recipe] = {
    ingredient.GUN_POWDER: Recipe(ingredient.GUN_POWDER,
                                  ingredients=[ingredient.SULFUR.from_qty(20),
                                               ingredient.CHARCOAL.from_qty(20)],
                                  result=ingredient.GUN_POWDER.from_qty(10),
                                  crafting_station=CraftingStation.MIXING_TABLE,
                                  seconds_to_craft=1),
}

workbench_t1_recipes: dict[IngredientKey, Recipe] = {
    ingredient.GUN_POWDER: Recipe(ingredient.GUN_POWDER,
                                  ingredients=[ingredient.SULFUR.from_qty(20), ingredient.CHARCOAL.from_qty(30)],
                                  result=ingredient.GUN_POWDER.from_qty(10), crafting_station=CraftingStation.T1,
                                  seconds_to_craft=2),

    ingredient.BEANCAN_GRENADE: Recipe(ingredient.BEANCAN_GRENADE,
                                       ingredients=[ingredient.GUN_POWDER.from_qty(60),
                                                    ingredient.METAL_FRAGMENTS.from_qty(20)],
                                       result=ingredient.BEANCAN_GRENADE.from_qty(1),
                                       crafting_station=CraftingStation.T1,
                                       seconds_to_craft=10),

    ingredient.SATCHEL_CHARGE: Recipe(ingredient.SATCHEL_CHARGE,
                                      ingredients=[ingredient.BEANCAN_GRENADE.from_qty(4),
                                                   ingredient.SMALL_STASH.from_qty(1),
                                                   ingredient.ROPE.from_qty(1)],
                                      result=ingredient.SATCHEL_CHARGE.from_qty(1), crafting_station=CraftingStation.T1,
                                      seconds_to_craft=5)
}

workbench_t2_recipes: dict[IngredientKey, Recipe] = {
    ingredient.GUN_POWDER: Recipe(ingredient.GUN_POWDER,
                                  ingredients=[ingredient.SULFUR.from_qty(20), ingredient.CHARCOAL.from_qty(30)],
                                  result=ingredient.GUN_POWDER.from_qty(10), crafting_station=CraftingStation.T2,
                                  seconds_to_craft=1),
}

workbench_t3_recipes: dict[IngredientKey, Recipe] = {}

default_recipes: dict[IngredientKey, Recipe] = {
    ingredient.SMALL_STASH: Recipe(ingredient.SMALL_STASH, ingredients=[ingredient.CLOTH.from_qty(10)],
                                   result=ingredient.SMALL_STASH.from_qty(1),
                                   crafting_station=CraftingStation.NONE, seconds_to_craft=15)
}

RECIPES: dict[CraftingStation, dict[IngredientKey, Recipe]] = {
    CraftingStation.NONE: default_recipes,
    CraftingStation.T1: default_recipes | workbench_t1_recipes,
    CraftingStation.T2: default_recipes | workbench_t1_recipes | workbench_t2_recipes,
    CraftingStation.T3: default_recipes | workbench_t1_recipes | workbench_t2_recipes | workbench_t3_recipes,
    CraftingStation.MIXING_TABLE: default_recipes | workbench_t1_recipes | workbench_t2_recipes | workbench_t3_recipes | mixing_table_recipes
}


class RecipeTableOptions:
    def __init__(self, crafting_station: CraftingStation):
        self.crafting_station = crafting_station


class RecipeTable:
    def __init__(self, options: RecipeTableOptions):
        self.options: RecipeTableOptions = options
        self.recipes: dict[IngredientKey, Recipe] = {}
        # self.ingredient_table: IngredientTable = IngredientTable(self.options)

        # self.ingredient_table.gun_powder()
