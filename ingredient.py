from rust_ingredients import RustIngredients
from recipe import Recipe

class Ingredient:
    def __init__(self, name: RustIngredients, recipe: Recipe, qty: int):
        self.name: str = name.value
        self.recipe: Recipe = recipe
        self.qty: int = qty

    def __eq__(self, other):
        if isinstance(other, Ingredient):
            return self.name == other.name
        return False

    def copy_with_new_qty(self, new_qty: int) -> "Ingredient":
        return Ingredient(RustIngredients[self.name.replace(" ", "_").upper()], self.recipe, new_qty)

    # def __ge__(self, other):
    #     if isinstance(other, Ingredient):
    #         return other.qty >= self.qty

    def __repr__(self):
        return f"{self.name} x{self.qty}"
