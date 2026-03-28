import random
from bonus_case import *
def get_random_case(pos):
    case = random.choices([ReplayCase, KillCase, SideCase, 
                           DefaultCase, DivisionCase, BurningCase, MoneyCase, 
                           InterestCase, DeathCase, ItemCase, JailCase, CreeperCase, RandomCase,
                           FirstCase])[0]
    return case(pos)

def get_random_case1(pos):
    case = random.choices([DefaultCase, RandomCase, JailCase])[0]
    return case(pos)


