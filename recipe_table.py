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

oil_refinery_recipes: dict[IngredientKey, Recipe] = {
    ingredient.LOW_GRADE_FUEL: Recipe(ingredient.LOW_GRADE_FUEL,
                                      ingredients=[ingredient.CRUDE_OIL.from_qty(1), ingredient.WOOD.from_qty(2.22)],
                                      result=ingredient.LOW_GRADE_FUEL.from_qty(3),
                                      crafting_station=CraftingStation.SMALL_OIL_REFINERY, seconds_to_craft=3.33),
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
                                   crafting_station=CraftingStation.NONE, seconds_to_craft=15),

    ingredient.LOW_GRADE_FUEL: Recipe(ingredient.LOW_GRADE_FUEL,
                                      ingredients=[ingredient.CLOTH.from_qty(1), ingredient.ANIMAL_FAT.from_qty(3)],
                                      result=ingredient.LOW_GRADE_FUEL.from_qty(4),
                                      crafting_station=CraftingStation.NONE,
                                      seconds_to_craft=5),
}

RECIPES: dict[CraftingStation, dict[IngredientKey, Recipe]] = {
    CraftingStation.NONE: default_recipes,
    CraftingStation.T1: default_recipes | workbench_t1_recipes,
    CraftingStation.T2: default_recipes | workbench_t1_recipes | workbench_t2_recipes,
    CraftingStation.T3: default_recipes | workbench_t1_recipes | workbench_t2_recipes | workbench_t3_recipes,
    CraftingStation.MIXING_TABLE: default_recipes | workbench_t1_recipes | workbench_t2_recipes | workbench_t3_recipes | mixing_table_recipes,
    CraftingStation.SMALL_OIL_REFINERY: oil_refinery_recipes
}


class RecipeTableOptions:
    def __init__(self, crafting_station: CraftingStation):
        self.crafting_station = crafting_station


class RecipeTable:
    def __init__(self, options: RecipeTableOptions):
        self.options: RecipeTableOptions = options
        self.recipes: dict[IngredientKey, Recipe] = RECIPES[options.crafting_station]

    def ingredients_needed_for(self, qty: int, recipe: IngredientKey) -> "RecipeQueryResult":
        if not isinstance(qty, int):
            # While internal ingredient quantity is represented as a float, in Rust, items are ONLY shown in integers.
            raise TypeError("qty must be an integer! You cannot create non-integral quantities of items in Rust.")
        if qty <= 0:
            raise ValueError("qty must be greater than zero!")

        if recipe not in self.recipes:
            return RecipeQueryResult(recipe.from_qty(qty), None, None)

        matched_recipe = self.recipes[recipe]
        extra_needed_for_parent = self.__calculate_extra(qty, matched_recipe.result)
        return RecipeQueryResult(parent_ingredient=recipe.from_qty(qty, extra_needed_for_parent),
                                 ingredients=matched_recipe.ingredients_needed_for(qty),
                                 associated_recipe_table=self)

    @staticmethod
    def __calculate_extra(wanted_qty: int, ingredient: RustIngredient) -> float:
        crafting_increments = ingredient.qty
        extra = 0
        while True:
            remainder = (wanted_qty + extra) % crafting_increments
            if remainder == 0:
                return extra
            extra += 1


class RecipeQueryResult:
    def __init__(self, parent_ingredient: RustIngredient, ingredients: list[RustIngredient] | None,
                 associated_recipe_table: RecipeTable | None):
        self.parent_ingredient: RustIngredient = parent_ingredient
        self.ingredients: list[RustIngredient] | None = ingredients
        self.associated_recipe_table: RecipeTable | None = associated_recipe_table

        self.recipes: list["RecipeQueryResult"] | None = self.__recipes()

    def __recipes(self) -> list["RecipeQueryResult"] | None:
        if self.ingredients is None:
            return None

        result = []
        for self_ingredient in self.ingredients:
            if self_ingredient.key not in self.associated_recipe_table.recipes:
                result.append(RecipeQueryResult(self_ingredient, None, None))
                continue

            matched_recipe = self.associated_recipe_table.recipes[self_ingredient.key]
            final_ingredients = matched_recipe.ingredients_needed_for(self_ingredient.qty)
            result.append(RecipeQueryResult(self_ingredient, final_ingredients, self.associated_recipe_table))

        return result

    def print_tree(self, node: "RecipeQueryResult" = None, last=True, header=''):
        if node is None:
            node = self
            print(f"{node.associated_recipe_table.options.crafting_station.value}")
        elbow = "└──"
        pipe = "│  "
        tee = "├──"
        blank = "   "
        print(header + (elbow if last else tee) + str(node.parent_ingredient))
        if node.recipes is not None:
            for i, n in enumerate(node.recipes):
                self.print_tree(n, header=header + (blank if last else pipe), last=i == len(node.recipes) - 1)

    def __repr__(self):
        return f"RecipeQueryResult for {self.parent_ingredient}: Ingredients: {self.ingredients} Recipes: {len(self.recipes)}"
