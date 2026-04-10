import random
from bonus_squares import *
def get_random_case(pos):
    square = random.choices([ReplaySquare, KillSquare, SideSquare, ReplaceableSquare ,
                           DefaultSquare, DivisionSquare, BurningSquare, MoneySquare, DestructionSquare,
                           InterestSquare, DeathSquare, ItemSquare, JailSquare, CreeperSquare, RandomSquare,
                           FirstSquare, DiamondSquare, LuckySquare, BluePrintSquare,
                           YinYangSquare, TeleportSquare, StoneSquare])[0]
    return square(pos)

def get_random_c1ase(pos):
    case = random.choices([DefaultSquare, StoneSquare])[0]
    return case(pos)

def get_random_cas1e(pos):
    return CreeperSquare(pos)
