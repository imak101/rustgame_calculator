import recipe
import ingredient

if __name__ == '__main__':
    input_char = 7000
    input_sulf = 7000

    result = recipe.satchel_charge.ingredients_needed_for(12)
    for item in result:
        print(item)
        print(item.recipe)

