import enum


class RustIngredients(enum.Enum):
    SULFUR = "Sulfur"
    CHARCOAL = "Charcoal"

    GUN_POWDER = "Gun Powder"


class Ingredient:
    def __init__(self, name: RustIngredients, qty: int):
        self.name: str = name.value
        self.qty: int = qty

    def __eq__(self, other):
        if isinstance(other, Ingredient):
            return self.name == other.name
        return False

    def copy_with_new_qty(self, new_qty: int) -> "Ingredient":
        return Ingredient(RustIngredients[self.name.replace(" ", "_").upper()], new_qty)

    # def __ge__(self, other):
    #     if isinstance(other, Ingredient):
    #         return other.qty >= self.qty

    def __repr__(self):
        return f"{self.name} x{self.qty}"


def sulfur(qty: int) -> Ingredient:
    return Ingredient(RustIngredients.SULFUR, qty)


def charcoal(qty: int) -> Ingredient:
    return Ingredient(RustIngredients.CHARCOAL, qty)

def gun_powder(qty: int) -> Ingredient:
    return Ingredient(RustIngredients.GUN_POWDER, qty)
