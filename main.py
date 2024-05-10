from rust_ingredients import IngredientKey as ingredient
from rust_ingredients import *
from recipe_table import *

if __name__ == '__main__':

    # mixing_table = RecipeTable(RecipeTableOptions(CraftingStation.MIXING_TABLE))
    # satchel_from_mixing = mixing_table.ingredients_needed_for(12, ingredient.SATCHEL_CHARGE)
    # satchel_from_mixing.print_tree()

    oil_ref = RecipeTable(RecipeTableOptions(CraftingStation.SMALL_OIL_REFINERY, True, True, True))
    oil_ref.ingredients_needed_for(750, ingredient.LOW_GRADE_FUEL).print_tree()
    # oil_ref.ingredients_needed_for(4, ingredient.LOW_GRADE_FUEL).print_tree()
    # oil_ref.ingredients_needed_for(6, ingredient.LOW_GRADE_FUEL).print_tree()
    # oil_ref.ingredients_needed_for(10, ingredient.LOW_GRADE_FUEL).print_tree()

    t3 = RecipeTable(RecipeTableOptions(CraftingStation.T3, True, False, False))

    # todo: add what_can_i_make_with()
    # todo: show_raw exceptions
    # todo: add more recipes
    # todo: add command line api
    # todo: add interactive ui while running the program
    # todo: make discord port
    # todo: add raid calculator
    t3.ingredients_needed_for(20, ingredient.SULFUR).print_tree()
    t3.ingredients_needed_for(6, ingredient.TIMED_EXPLOSIVE_CHARGE).print_tree()

    t3.ingredients_needed_for(6, ingredient.TIMED_EXPLOSIVE_CHARGE).print_total_raw_needed()
    t3.ingredients_needed_for(21, ingredient.TIMED_EXPLOSIVE_CHARGE).print_total_raw_needed()
    t3.ingredients_needed_for(50, ingredient.ROCKET).print_total_raw_needed()

    t3.ingredients_needed_for(101, ingredient.EXPLOSIVE_556_RIFLE_AMMO).print_total_raw_needed()

    # t3.what_can_i_make_with([ingredient.SULFUR.from_qty(25127)])
    t3.boom_from([ingredient.SULFUR.from_qty(1000), ingredient.GUN_POWDER.from_qty(1000), ingredient.EXPLOSIVES.from_qty(20)])
    # t3.boom_from([ ingredient.SULFUR.from_qty(1000), ingredient.GUN_POWDER.from_qty(1000), ])
    # t3.what_can_i_make_with([ingredient.GUN_POWDER.from_qty(1000), ingredient.SULFUR.from_qty(1000)])



