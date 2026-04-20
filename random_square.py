import random
from bonus_squares import *
def get_random_square(pos):
    square = random.choices([ReplaySquare, KillSquare, SideSquare, ReplaceableSquare , TableSquare,
                           DefaultSquare, DivisionSquare, BurningSquare, MoneySquare, DestructionSquare,
                           InterestSquare, DeathSquare, ItemSquare, JailSquare, CreeperSquare, RandomSquare,
                           FirstSquare, DiamondSquare, LuckySquare, BluePrintSquare, TriggerSideSquare,
                           YinYangSquare, TeleportSquare, StoneSquare, LaserSquare, LoseMoneySquare])[0]
    return square(pos)

def get_random_square(pos):
    square = random.choices([RandomSquare, SideSquare])[0]
    return square(pos)

def get_random_square(pos):
    return TriggerSideSquare(pos)
