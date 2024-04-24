from rust_ingredients import IngredientKey as ingredient
from rust_ingredients import *
from recipe_table import *

if __name__ == '__main__':

    # mixing_table = RecipeTable(RecipeTableOptions(CraftingStation.MIXING_TABLE))
    # satchel_from_mixing = mixing_table.ingredients_needed_for(12, ingredient.SATCHEL_CHARGE)
    # satchel_from_mixing.print_tree()

    # oil_ref = RecipeTable(RecipeTableOptions(CraftingStation.SMALL_OIL_REFINERY))
    # oil_ref.ingredients_needed_for(1, ingredient.LOW_GRADE_FUEL).print_tree()
    # oil_ref.ingredients_needed_for(4, ingredient.LOW_GRADE_FUEL).print_tree()
    # oil_ref.ingredients_needed_for(6, ingredient.LOW_GRADE_FUEL).print_tree()
    # oil_ref.ingredients_needed_for(10, ingredient.LOW_GRADE_FUEL).print_tree()

    t3 = RecipeTable(RecipeTableOptions(CraftingStation.T3, False, False, True))

    t3.ingredients_needed_for(20, ingredient.SULFUR).print_tree()
    t3.ingredients_needed_for(6, ingredient.TIMED_EXPLOSIVE_CHARGE).print_tree()

    t3.ingredients_needed_for(6, ingredient.TIMED_EXPLOSIVE_CHARGE).print_total_raw_needed()
    t3.ingredients_needed_for(21, ingredient.TIMED_EXPLOSIVE_CHARGE).print_total_raw_needed()




