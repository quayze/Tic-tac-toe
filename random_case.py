import random
from bonus_case import *
def get_random_case(pos):
    case = random.choices([ReplayCase, KillCase, SideCase, ReplacableCase ,
                           DefaultCase, DivisionCase, BurningCase, MoneyCase, 
                           InterestCase, DeathCase, ItemCase, JailCase, CreeperCase, RandomCase,
                           FirstCase, DiamondSquare, DestructionSquare, LuckySquare, BluePrintCase])[0]
    return case(pos)

def get_random_case1(pos):
    case = random.choices([KillCase, DefaultCase])[0]
    return case(pos)

def get_random_case(pos):
    return DefaultCase(pos)
