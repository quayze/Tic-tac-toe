import random
from bonus_case import *
def get_random_case(pos):
    case = random.choices([ReplacableCase, ReplayCase, KillCase, SideCase, 
                           DefaultCase, DivisionCase, BurningCase, MoneyCase, 
                           InterestCase, DeathCase,ItemCase, ChainCase, CreeperCase, RandomCase,
                           FirstCase])[0]
    return case(pos)

def get_random_case(pos):
    case = random.choices([DefaultCase, ItemCase])[0]
    return case(pos)


