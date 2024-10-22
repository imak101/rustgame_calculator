from enum import Enum
import math


class IngredientKey(Enum):
    # Resource
    SULFUR = "Sulfur"
    CHARCOAL = "Charcoal"
    GUN_POWDER = "Gun Powder"
    METAL_FRAGMENTS = "Metal Fragments"
    CLOTH = "Cloth"
    LOW_GRADE_FUEL = "Low Grade Fuel"
    ANIMAL_FAT = "Animal Fat"
    CRUDE_OIL = "Crude Oil"
    WOOD = "Wood"
    HIGH_QUALITY_METAL = "High Quality Metal"
    SCRAP = "Scrap"

    # Misc
    SMALL_STASH = "Small Stash"

    # Comps
    ROPE = "Rope"
    METAL_PIPE = "Metal Pipe"
    TECH_TRASH = "Tech Trash"

    # Boom
    BEANCAN_GRENADE = "Beancan Grenade"
    SATCHEL_CHARGE = "Satchel Charge"
    EXPLOSIVES = "Explosives"
    ROCKET = "Rocket"
    TIMED_EXPLOSIVE_CHARGE = "Timed Explosive Charge"
    EXPLOSIVE_556_RIFLE_AMMO = "Explosive 5.56 Rifle Ammo"
    HIGH_VELOCITY_ROCKET = "High Velocity Rocket"

    def from_qty(self, qty: float, extra: float | None = None) -> "RustIngredient":
        return RustIngredient(self, qty, extra)


class RustIngredient:
    """In Rust, ingredients are represented and used only in whole numbers.
    However, specific crafting recipes consume specific ingredients in fractions (e.g. the oil refinery converts 2.22 wood and 1 crude oil into 3 low grade)
    so every RustIngredient quantity is a float even if the actual ingredient is a whole number.

    The [extra] argument is used to represent the amount that is needed for the original [qty]
    to be divisible by the crafting amount of whatever recipe that requires this ingredient.
    This is done so that the original, requested, quantity is not lost and only requires adding [qty] and [extra] to see the true amount.

    e.g. A user requests the ingredients needed to make 1 low grade fuel from an oil refinery.
    Because the oil refinery can only make low grade in stacks of 3, we will instantiate the result [RustIngredient] with
    the [qty] as 1 and [extra] as 2. If the user requests 2 low grade: [qty] = 2 and [extra] as 1. For 3LGF (a valid stack size): [qty] = 3, [extra] = 0

    [extra] can be None when no calculation was performed to see if any extra was actually needed. 0 is a valid amount for [extra].
     """
    def __init__(self, key: IngredientKey, qty: float, extra: float | None = None):
        self.key: IngredientKey = key
        self.name: str = key.value
        self.qty: float = qty
        self.extra: float | None = extra

        self.total_qty: float = qty + (extra if extra is not None else 0)

        # True when representing an ingredient that is not yet real in a Rust inventory.
        # e.g. is imaginary when representing a possible craft result but not yet actually crafted
        # Imaginary ingredients don't needed to be math.ceiling()-ed to represent a real craft-able amount from a partial craft amount from imperfect craft quantities requested via a user.
        # Imaginary ingredients can **only ever** be crafted in their respective quantity because crafting station never craft in partial stack sizes.
        # (e.g. gunpowder crafts in increments of 10. you can *never* craft less than this amount or in amounts that aren't divisible by 10)
        self.is_imaginary: bool = False

    def __eq__(self, other):
        if not isinstance(other, RustIngredient):
            raise TypeError(f'Cannot compare {type(self).__name__} to {type(other).__name__}')
        return self.name == other.name

    def __add__(self, other) -> "RustIngredient":
        if not isinstance(other, RustIngredient):
            raise TypeError(f'Cannot add {type(self).__name__} to {type(other).__name__}')
        if self.key != other.key:
            raise ValueError(f'Cannot add {self.key.value} to {other.key.value}. Make sure they both share the same key.')

        extra = (self.extra or 0) + (other.extra or 0)
        if self.extra is None and other.extra is None:
            extra = None
        return RustIngredient(self.key, self.qty + other.qty, extra)

    def __mul__(self, other):
        if not isinstance(other, RustIngredient):
            raise TypeError(f'Cannot multiply {type(self).__name__} by {type(other).__name__}')
        if self.key != other.key:
            raise ValueError(f'Cannot multiply {self.key.value} by {other.key.value}. Make sure they both share the same key.')

        extra = self.extra if self.extra is not None else 1 * other.extra if other.extra is not None else 1
        if self.extra is None and other.extra is None:
            extra = None
        return RustIngredient(self.key, self.qty * other.qty, extra)

    def copy_with_new_qty(self, new_qty: float, extra: float | None = None) -> "RustIngredient":
        return RustIngredient(self.key, new_qty, extra)

    def __repr__(self):
        if self.is_imaginary:
            return f"{self.name} x{math.floor(self.qty)} {f'(originally x{round(self.total_qty, 2)})' if math.floor(self.qty) != self.total_qty else ''}"

        show_exact_amount_too = self.total_qty < math.ceil(self.total_qty) != 1
        exact_amount = '(' + f'≡{self.total_qty:.2f}' + ')' if show_exact_amount_too else ''
        if self.extra is None or self.extra <= 0:
            payload = f"{self.name} x{math.ceil(self.qty):,}{exact_amount}"
        else:
            payload = f"{self.name} x{math.ceil(self.total_qty):,}{exact_amount} (originally x{round(self.qty, 2):,})"

        return payload
