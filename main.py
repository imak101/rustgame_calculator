import recipe
import ingredient

if __name__ == '__main__':
    input_char = 1000
    input_sulf = 1000

    # recipe.mixing_table_gun_powder.qty_from()
    recipe.t23_gun_powder.ingredients_needed_for(5000)
    print(recipe.t23_gun_powder.amount_from(ingredients=[ingredient.sulfur(input_sulf), ingredient.charcoal(input_char)]))
    print(recipe.mixing_table_gun_powder.amount_from(ingredients=[ingredient.sulfur(input_sulf), ingredient.charcoal(input_char)]))
