import random
from bonus_squares import *
def get_random_case(pos):
    square = random.choices([ReplaySquare, KillSquare, SideSquare, ReplaceableSquare ,
                           DefaultSquare, DivisionSquare, BurningSquare, MoneySquare, DestructionSquare,
                           InterestSquare, DeathSquare, ItemSquare, JailSquare, CreeperSquare, RandomSquare,
                           FirstSquare, DiamondSquare, LuckySquare, BluePrintSquare,
                           YinYangSquare, TeleportSquare, StoneSquare])[0]
    return square(pos)

def get_random_case(pos):
    case = random.choices([DefaultSquare, LuckySquare])[0]
    return case(pos)

def get_random_case1(pos):
    return DefaultSquare(pos)
