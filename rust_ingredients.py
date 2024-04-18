from enum import Enum


class IngredientKey(Enum):
    SULFUR = "Sulfur"
    CHARCOAL = "Charcoal"
    GUN_POWDER = "Gun Powder"
    METAL_FRAGMENTS = "Metal Fragments"
    CLOTH = "Cloth"

    # Misc
    SMALL_STASH = "Small Stash"

    # Comps
    ROPE = "Rope"

    # Boom
    BEANCAN_GRENADE = "Beancan Grenade"
    SATCHEL_CHARGE = "Satchel Charge"

    def from_qty(self, qty: int) -> "RustIngredient":
        return RustIngredient(self, qty)


class RustIngredient:
    def __init__(self, key: IngredientKey, qty: int):
        self.key: Ingredient = key
        self.name: str = key.value
        self.qty: int = qty

    def __eq__(self, other):
        if isinstance(other, RustIngredient):
            return self.name == other.name
        return False

    def copy_with_new_qty(self, new_qty: int) -> "RustIngredient":
        return RustIngredient(self.key, new_qty)

    # def __ge__(self, other):
    #     if isinstance(other, Ingredient):
    #         return other.qty >= self.qty

    def __repr__(self):
        return f"{self.name} x{self.qty}"

