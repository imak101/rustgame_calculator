import enum


class IngredientNames(enum.Enum):
    SULFUR = "Sulfur"
    CHARCOAL = "Charcoal"


class Ingredient:
    def __init__(self, name: IngredientNames, qty: int):
        self.name: str = name.value
        self.qty: int = qty

    def __eq__(self, other):
        if isinstance(other, Ingredient):
            return self.name == other.name
        return False

    # def __ge__(self, other):
    #     if isinstance(other, Ingredient):
    #         return other.qty >= self.qty

    def __repr__(self):
        return f"{self.name} x{self.qty}"


def sulfur(qty: int) -> Ingredient:
    return Ingredient(IngredientNames.SULFUR, qty)


def charcoal(qty: int) -> Ingredient:
    return Ingredient(IngredientNames.CHARCOAL, qty)
