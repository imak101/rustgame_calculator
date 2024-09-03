from rust_ingredients import IngredientKey as ingredient
from rust_ingredients import *
from recipe_table import *

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", help="Calculator mode. 1='ingredients need for...' 2='how much boom can i make with...'", choices=['1', '2'])
parser.add_argument("-i", "--item", nargs="*", help=f"item format: (quantity:item name) e.g. 1000:sulfur or 2000:gun_power. CHOICES: {"\n".join([item.value.replace(" ", "_").lower() + "\n" for item in ingredient])}") # choices=[item.value.replace(" ", "_").lower() for item in ingredient])
parser.add_argument("-r", "--raw", help="Also show raw ingredients", action="store_true")
args = parser.parse_args()


def item_string_to_rust_ingredient(item: str) -> RustIngredient:
    item_qty, item_name = item.split(":")

    if float(item_qty) % 1.0 != 0:
        print("You cannot craft a fraction of an item in Rust!")
        print(f"FIX ---> {item_qty}x {item_name} <--- FIX")
        exit(0)

    return ingredient[item_name.replace("-", "_").replace(".", "").upper()].from_qty(int(float(item_qty))) # cast twice to avoid ValueError when user inputs "XXXX.00"


def make_item_list(items: list[str]) -> list[RustIngredient]:
    return [item_string_to_rust_ingredient(item_str) for item_str in items]


if __name__ == '__main__':
    if args.mode is None:
        parser.print_help()
        exit(0)

    if args.item is None:
        print("No items provided! Please try again with a '-i'(item) paramater.")
        exit(0)
    
    if int(args.mode) == 1:
        input_items = make_item_list(args.item)
        table = RecipeTable()

        for item in input_items:
            if len(input_items) > 1:
                print(f"↓↓ ----- {item.name.upper()} ----- ↓↓ \n")

            print(table.ingredients_needed_for(item.total_qty, item.key).tree())
            if args.raw:
                print(table.ingredients_needed_for(item.total_qty, item.key).raw_needed_tree())

    if int(args.mode) == 2:
        input_items = make_item_list(args.item)
        table = RecipeTable()

        boom_queries = table.boom_from(input_items)
        if len(boom_queries) == 0:
            print(f"You cannot make any boom from these ingredients: {','.join([str(item) for item in input_items])}")
        for query in boom_queries:
            if len(boom_queries) > 1:
                print(f"↓↓ ----- {query.parent_ingredient.name.upper()} ----- ↓↓ \n")

            print(query.tree())
            if args.raw:
                print(query.raw_needed_tree())




