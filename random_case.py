import random
from bonus_squares import *
def get_random_case1(pos):
    square = random.choices([ReplaySquare, KillSquare, SideSquare, ReplaceableSquare ,
                           DefaultSquare, DivisionSquare, BurningSquare, MoneySquare, 
                           InterestSquare, DeathSquare, ItemSquare, JailSquare, CreeperSquare, RandomSquare,
                           FirstSquare, DiamondSquare, DestructionSquare, LuckySquare, BluePrintSquare])[0]
    return square(pos)

def get_random_case(pos):
    case = random.choices([ModifySideSquare, DefaultSquare])[0]
    return case(pos)

def get_random_case(pos):
    return DefaultSquare(pos)
