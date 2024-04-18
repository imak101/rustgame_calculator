from rust_ingredients import IngredientKey as ingredient
from rust_ingredients import *
from recipe_table import *

if __name__ == '__main__':
    input_char = 7000
    input_sulf = 7000

    print(RECIPES[CraftingStation.T1][ingredient.SATCHEL_CHARGE].ingredients)
