import random
from bonus_squares import *
def get_random_case(pos):
    square = random.choices([ReplaySquare, KillSquare, SideSquare, ReplaceableSquare ,
                           DefaultSquare, DivisionSquare, BurningSquare, MoneySquare, 
                           InterestSquare, DeathSquare, ItemSquare, JailSquare, CreeperSquare, RandomSquare,
                           FirstSquare, DiamondSquare, DestructionSquare, LuckySquare, BluePrintSquare,
                           ModifySideSquare, TeleportSquare])[0]
    return square(pos)

def get_random_cas1e(pos):
    case = random.choices([ModifySideSquare, DefaultSquare])[0]
    return case(pos)

def get_random_cas1e(pos):
    return ReplaceableSquare(pos)
