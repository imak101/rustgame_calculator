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
                                   crafting_station=CraftingStation.NONE, seconds_to_craft=15)
}

RECIPES: dict[CraftingStation, dict[IngredientKey, Recipe]] = {
    CraftingStation.NONE: default_recipes,
    CraftingStation.T1: default_recipes | workbench_t1_recipes,
    CraftingStation.T2: default_recipes | workbench_t1_recipes | workbench_t2_recipes,
    CraftingStation.T3: default_recipes | workbench_t1_recipes | workbench_t2_recipes | workbench_t3_recipes,
    CraftingStation.MIXING_TABLE: default_recipes | workbench_t1_recipes | workbench_t2_recipes | workbench_t3_recipes | mixing_table_recipes
}


class RecipeTableOptions:
    def __init__(self, crafting_station: CraftingStation):
        self.crafting_station = crafting_station


class RecipeTable:
    def __init__(self, options: RecipeTableOptions):
        self.options: RecipeTableOptions = options
        self.recipes: dict[IngredientKey, Recipe] = RECIPES[options.crafting_station]

    def ingredients_needed_for(self, qty: int, recipe: IngredientKey) -> "RecipeQueryResult":
        if recipe not in self.recipes:
            return RecipeQueryResult(recipe.from_qty(qty), None, None)

        matched_recipe = self.recipes[recipe]
        return RecipeQueryResult(recipe.from_qty(qty), matched_recipe.ingredients_needed_for(qty), self)

    # def __getitem__(self, recipe: IngredientKey) -> RecipeQueryResult:
    #     try:
    #         return RecipeQueryResult([self.recipes[recipe]], self.recipes)
    #     except KeyError:
    #         return None


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
        print_tabs = lambda: "\t" * self.__nodes_deep
        return f"RecipeQueryResult for {self.parent_ingredient}: Ingredients: {self.ingredients} Recipes: {len(self.recipes)}"
