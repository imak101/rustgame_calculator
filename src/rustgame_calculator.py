from rust_ingredients import IngredientKey as ingredient
from rust_ingredients import *
from recipe_table import *

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", help="Calculator mode. 1='ingredients need for...' 2='how much boom can i make with...'", choices=['1', '2'])
parser.add_argument("-i", "--item", nargs="*", help="item format: ('item name':quantity of item) e.g. sulfur:1000 or gun_power:2000") # choices=[item.value.replace(" ", "_").lower() for item in ingredient]
parser.add_argument("-r", "--raw", help="Also show raw ingredients", action="store_true")
args = parser.parse_args()


def item_string_to_rust_ingredient(item: str) -> RustIngredient:
    item_name, item_qty = item.split(":")
    return ingredient[item_name.replace("-", "_").upper()].from_qty(int(item_qty))


def make_item_list(items: list[str]) -> list[RustIngredient]:
    return [item_string_to_rust_ingredient(item_str) for item_str in items]


if __name__ == '__main__':
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
        for query in boom_queries:
            if len(boom_queries) > 1:
                print(f"↓↓ ----- {query.parent_ingredient.name.upper()} ----- ↓↓ \n")

            print(query.tree())
            if args.raw:
                print(query.raw_needed_tree())




