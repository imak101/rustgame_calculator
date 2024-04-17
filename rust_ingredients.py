import enum
from ingredient import Ingredient

class RustIngredients(enum.Enum):
    # Resources
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


# Resources

def sulfur(qty: int) -> Ingredient:
    return Ingredient(RustIngredients.SULFUR, qty)


def charcoal(qty: int) -> Ingredient:
    return Ingredient(RustIngredients.CHARCOAL, qty)

def gun_powder(qty: int) -> Ingredient:
    return Ingredient(RustIngredients.GUN_POWDER, qty)

def metal_fragments(qty: int) -> Ingredient:
    return Ingredient(RustIngredients.METAL_FRAGMENTS, qty)

def cloth(qty: int) -> Ingredient:
    return Ingredient(RustIngredients.CLOTH, qty)

# End Resources
# Misc

def small_stash(qty: int) -> Ingredient:
    return Ingredient(RustIngredients.SMALL_STASH, qty)

# End Misc
# Comps

def rope(qty: int) -> Ingredient:
    return Ingredient(RustIngredients.ROPE, qty)

# End Comps
# Boom

def beancan_grenade(qty: int) -> Ingredient:
    return Ingredient(RustIngredients.BEANCAN_GRENADE, qty)

def satchel_charge(qty: int) -> Ingredient:
    return Ingredient(RustIngredients.SATCHEL_CHARGE, qty)

# End Boom