from enum import Enum


class CraftingStation(Enum):
    NONE = "Crafted without a workbench"

    T1 = "Workbench Level 1"
    T2 = "Workbench Level 2"
    T3 = "Workbench Level 3"

    MIXING_TABLE = "Mixing Table"
    SMALL_OIL_REFINERY = "Small Oil Refinery"
