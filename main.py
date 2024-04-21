from rust_ingredients import IngredientKey as ingredient
from rust_ingredients import *
from recipe_table import *

if __name__ == '__main__':
    # table = RecipeTable(RecipeTableOptions(CraftingStation.T3))

    # mixing_table = RecipeTable(RecipeTableOptions(CraftingStation.MIXING_TABLE))
    # satchel_from_mixing = mixing_table.ingredients_needed_for(12, ingredient.SATCHEL_CHARGE)
    # satchel_from_mixing.print_tree()

    oil_ref = RecipeTable(RecipeTableOptions(CraftingStation.SMALL_OIL_REFINERY))
    oil_ref.ingredients_needed_for(1, ingredient.LOW_GRADE_FUEL).print_tree()
    oil_ref.ingredients_needed_for(4, ingredient.LOW_GRADE_FUEL).print_tree()
    oil_ref.ingredients_needed_for(6, ingredient.LOW_GRADE_FUEL).print_tree()
    oil_ref.ingredients_needed_for(10, ingredient.LOW_GRADE_FUEL).print_tree()

    # for i in range(0, 100):
    #     oil_ref.ingredients_needed_for(i, ingredient.LOW_GRADE_FUEL).print_tree()

