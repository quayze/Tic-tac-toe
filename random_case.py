import random
from bonus_squares import *
def get_random_case(pos):
    square = random.choices([ReplaySquare, KillSquare, SideSquare, ReplaceableSquare ,
                           DefaultSquare, DivisionSquare, BurningSquare, MoneySquare, DestructionSquare,
                           InterestSquare, DeathSquare, ItemSquare, JailSquare, CreeperSquare, RandomSquare,
                           FirstSquare, DiamondSquare, LuckySquare, BluePrintSquare, TriggerSideSquare,
                           YinYangSquare, TeleportSquare, StoneSquare, LaserSquare, LoseMoneySquare])[0]
    return square(pos)

def get_random_ca1se(pos):
    case = random.choices([TriggerSideSquare, TeleportSquare, ReplaySquare, KillSquare])[0]
    return case(pos)

def get_random_case(pos):
    return TriggerSideSquare(pos)
