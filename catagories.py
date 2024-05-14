from enum import Enum
from rust_ingredients import IngredientKey as ingredient
from rust_ingredients import *


class IngredientCategory(Enum):
    EXPLOSIVES: list[IngredientKey] = [
        ingredient.BEANCAN_GRENADE,
        ingredient.SATCHEL_CHARGE,
        ingredient.EXPLOSIVES,
        ingredient.ROCKET,
        ingredient.TIMED_EXPLOSIVE_CHARGE,
        ingredient.EXPLOSIVE_556_RIFLE_AMMO,
        ingredient.HIGH_VELOCITY_ROCKET
    ]

    AMMO: list[IngredientKey] = []
