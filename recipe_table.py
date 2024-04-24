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

workbench_t3_recipes: dict[IngredientKey, Recipe] = {
    ingredient.EXPLOSIVES: Recipe(ingredient.EXPLOSIVES,
                                  ingredients=[ingredient.GUN_POWDER.from_qty(50), ingredient.LOW_GRADE_FUEL.from_qty(3),
                                               ingredient.SULFUR.from_qty(10), ingredient.METAL_FRAGMENTS.from_qty(10)],
                                  result=ingredient.EXPLOSIVES.from_qty(1), crafting_station=CraftingStation.T3,
                                  seconds_to_craft=5),

    ingredient.ROCKET: Recipe(ingredient.ROCKET,
                              ingredients=[ingredient.METAL_PIPE.from_qty(2), ingredient.GUN_POWDER.from_qty(150),
                                           ingredient.EXPLOSIVES.from_qty(10)],
                              result=ingredient.ROCKET.from_qty(1), crafting_station=CraftingStation.T3, seconds_to_craft=10),

    ingredient.TIMED_EXPLOSIVE_CHARGE: Recipe(ingredient.TIMED_EXPLOSIVE_CHARGE,
                                              ingredients=[ingredient.EXPLOSIVES.from_qty(20), ingredient.CLOTH.from_qty(5),
                                                           ingredient.TECH_TRASH.from_qty(2)],
                                              result=ingredient.TIMED_EXPLOSIVE_CHARGE.from_qty(1), crafting_station=CraftingStation.T3, seconds_to_craft=30)


}

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

component_recipes: dict[IngredientKey, Recipe] = {
    ingredient.METAL_PIPE: Recipe(ingredient.METAL_PIPE, ingredients=[ingredient.HIGH_QUALITY_METAL.from_qty(2), ingredient.SCRAP.from_qty(20)],
                                  result=ingredient.METAL_PIPE.from_qty(1), crafting_station=CraftingStation.T3, seconds_to_craft=1),
}

RECIPES: dict[CraftingStation, dict[IngredientKey, Recipe]] = {
    CraftingStation.NONE: default_recipes,
    CraftingStation.T1: default_recipes | workbench_t1_recipes,
    CraftingStation.T2: default_recipes | workbench_t1_recipes | workbench_t2_recipes,
    CraftingStation.T3: default_recipes | workbench_t1_recipes | workbench_t2_recipes | workbench_t3_recipes,
    CraftingStation.MIXING_TABLE: mixing_table_recipes,
    CraftingStation.SMALL_OIL_REFINERY: oil_refinery_recipes
}


class RecipeTableOptions:
    def __init__(self, crafting_station: CraftingStation, use_low_grade_from_refinery: bool, use_mixing_table_recipes: bool, use_component_recipes: bool):
        self.crafting_station = crafting_station
        self.use_low_grade_from_refinery = use_low_grade_from_refinery
        self.use_mixing_table_recipes = use_mixing_table_recipes
        self.use_component_recipes = use_component_recipes

    def __repr__(self):
        options = []
        if self.use_mixing_table_recipes:
            options.append("Mixing Table Recipes")
        if self.use_low_grade_from_refinery:
            options.append("Low Grade From Refinery")
        if self.use_component_recipes:
            options.append("Component Recipes")
        options_string = "(with " + ", ".join(options) + ")"

        return f"{self.crafting_station.value} {options_string}"


class RecipeTable:
    def __init__(self, options: RecipeTableOptions):
        self.options: RecipeTableOptions = options
        self.recipes: dict[IngredientKey, Recipe] = RECIPES[options.crafting_station]

        # todo: refactor
        if self.options.use_low_grade_from_refinery:
            self.recipes = self.recipes | RECIPES[CraftingStation.SMALL_OIL_REFINERY]
        if self.options.use_mixing_table_recipes:
            self.recipes = self.recipes | RECIPES[CraftingStation.MIXING_TABLE]
        if self.options.use_component_recipes:
            self.recipes = self.recipes | component_recipes

    def ingredients_needed_for(self, qty: int, recipe: IngredientKey) -> "RecipeQueryResult":
        if not isinstance(qty, int):
            # While internal ingredient quantity is represented as a float, in Rust, items are ONLY shown in integers.
            raise TypeError("qty must be an integer! You cannot create non-integral quantities of items in Rust.")
        if qty <= 0:
            raise ValueError("qty must be greater than zero!")

        if recipe not in self.recipes:
            # todo: determine if we should throw vs just returning an empty query
            # raise ValueError(f"You cannot craft {recipe.value}.")
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
            if node.associated_recipe_table is None:
                print("There are no recipes for:")
            else:
                print(str(node.associated_recipe_table.options))
        elbow = "└──"
        pipe = "│  "
        tee = "├──"
        blank = "   "
        print(header + (elbow if last else tee) + str(node.parent_ingredient))
        if node.recipes is not None:
            # index, node
            for i, n in enumerate(node.recipes):
                self.print_tree(n, header=header + (blank if last else pipe), last=i == len(node.recipes) - 1)

    def __raw(self) -> list[RustIngredient]:
        totals = []
        if self.recipes is None:
            totals.append(self.parent_ingredient)
            return totals
        for recipe_query in self.recipes:
            # if there are no ingredients for this recipe (None), insert just the parent ingredient
            totals.extend([ingredient for ingredient in recipe_query.ingredients or [recipe_query.parent_ingredient]])
        return totals

    def print_total_raw_needed(self):
        if self.recipes is None:
            raise ValueError(f"You cannot craft {self.parent_ingredient.name}.")

        all_raw_ingredients = []
        for recipe_query in self.recipes:
            for recipe_ingredient in recipe_query.__raw():
                run_combine = 1 <= len([ingredient for ingredient in all_raw_ingredients if ingredient == recipe_ingredient])
                if run_combine:
                    # reassign all_raw_ingredients with new list that combined all [RustIngredients] with the same [IngredientKey]. all others are unchanged.
                    all_raw_ingredients = [raw_total_ingredient + recipe_ingredient if recipe_ingredient == raw_total_ingredient else raw_total_ingredient for raw_total_ingredient in all_raw_ingredients]
                    continue

                all_raw_ingredients.append(recipe_ingredient)

        # todo: refactor these 5 lines
        all_raw_ingredients = sorted(all_raw_ingredients, key=lambda ingredient: ingredient.qty, reverse=True)
        # all_raw_ingredients = sorted(all_raw_ingredients, key=lambda ingredient: ingredient.name, reverse=False)
        print(str(self.associated_recipe_table.options))
        print(f"└──(Raw){self.parent_ingredient}")
        [print(f"   {'└──' if index == len(all_raw_ingredients) - 1 else '├──' }{item}") for index, item in enumerate(all_raw_ingredients)]

    def __repr__(self):
        return f"RecipeQueryResult for {self.parent_ingredient}: Ingredients: {self.ingredients} Recipes: {len(self.recipes)}"
