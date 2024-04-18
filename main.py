from rust_ingredients import IngredientKey as ingredient
from rust_ingredients import *
from recipe_table import *

if __name__ == '__main__':
    input_char = 7000
    input_sulf = 7000

    # print(RECIPES[CraftingStation.T3][ingredient.SATCHEL_CHARGE].ingredients)

    table = RecipeTable(RecipeTableOptions(CraftingStation.T3))
    # print(table[ingredient.SATCHEL_CHARGE])
    # print(table[ingredient.SATCHEL_CHARGE].recipes[0].ingredients_needed_for(8))
    # print(table[ingredient.GUN_POWDER].recipes[0].ingredients_needed_for(1920))
    #
    # print(table[ingredient.GUN_POWDER].qty())
    # table.ingredients_needed_for(10, ingredient.SATCHEL_CHARGE)
    # table.what_can_i_make_with(500, ingredient.GUN_POWDER)
    # table.recipe_for(ingredient.SMALL_STASH)

    satchel = table.ingredients_needed_for(12, ingredient.SATCHEL_CHARGE)
    # print(satchel.recipes)
    satchel.print_tree()
    print("\n")

    mixing_table = RecipeTable(RecipeTableOptions(CraftingStation.MIXING_TABLE))
    satchel_from_mixing = mixing_table.ingredients_needed_for(12, ingredient.SATCHEL_CHARGE)
    satchel_from_mixing.print_tree()


    # print(table[ingredient.METAL_FRAGMENTS])

    # table[ingredient.SATCHEL_CHARGE].deep
