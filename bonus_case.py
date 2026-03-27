from case import Case
from settings import *
from functions import *
from context import GameContext
import random
from marker import Marker
import pygame
from item import *


def generate_random_case():
    custom_cases = {ReplacableCase : 'common', ReplayCase: 'common', KillCase: 'common', SideCase: 'common', 
                    DivisionCase: 'common', BurningCase: 'common', MoneyCase: 'common', InterestCase: 'common', 
                    DeathCase: 'rare', ItemCase: 'common', ChainCase: 'common', CreeperCase: 'rare', FirstCase: 'common', 
                    RandomCase: 'common'}
    proba_cases = {}
    for case, rarity in custom_cases.items():
        proba_cases[case] = CaseConfig.RARITY_PERCENTAGE[rarity]
        
    case_type =  random.choices(list(proba_cases.keys()), list(proba_cases.values()))[0]
    return case_type()

class DefaultCase(Case):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image()
        self.blit_image()

    def trigger_effect(self, context):
        return context
    

class ReplayCase(Case):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(1, 0)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            context.replay = True

        return context
    
class ReplacableCase(Case):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(2, 0)
        self.blit_image()
        self.effect_triggered = False

    def trigger_effect(self, context : GameContext):
        if context.try_place and self.marker is not None and context.player != self.get_owner():
            self.marker.kill()
            self.marker = None
            self.effect_triggered = True

        elif context.marker_placed and self.effect_triggered:
            new_case = DefaultCase()
            context.add_changed_case(self, new_case)
            context.add_marker(new_case, self.marker)

        return context

    

class SideCase(Case):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(3, 0)
        self.side = random.randint(0, 3)
        self.image = pygame.transform.rotate(self.image, self.side * -90)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            index = context.table.get_index(self) if context.index is None else context.index
            #haut
            if self.side == 0:
                target_case : Case = context.table.get_side(index, 'top')
            #droite
            elif self.side == 1:
                target_case : Case = context.table.get_side(index, 'right')
            #bas
            elif self.side == 2:
                target_case : Case = context.table.get_side(index, 'bottom')
            #gauche
            elif self.side == 3:
                target_case : Case = context.table.get_side(index, 'left')
            
            
            if target_case is not None and target_case.can_place():
                marker_pos = target_case.get_pos()
                marker = Marker(owner= context.player, pos= marker_pos)
                context.add_marker(target_case, marker)

        return context


class KillCase(Case):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(4, 0)
        self.blit_image()
        self.shots = 6

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            list = context.table.get_case_list()
            killable_list = []
            for case in list:
                if case.get_owner() is not None and case.get_owner() != context.player:
                    killable_list.append(case)

            if killable_list != [] and self.shots != 0:
                if len(killable_list) == 1:
                    kill = killable_list[0]
                else:
                    kill : Case = random.choices(killable_list)[0]
                    
                self.shots = self.shots if context.blueprint else self.shots - 1

                context.add_changed_case(kill, DefaultCase())
                context.add_marker(kill, None)

                
            

        return context
    
class DivisionCase(Case):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(6, 0)
        self.blit_image()



    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            index = context.index if context.index is not None else context.table.get_index(self)
            none_divisable_case = [DivisionCase, EmptyCase]

            targets_cases = []
            target_case = None

            targets_cases.append(context.table.get_side(index, 'top'))
            targets_cases.append(context.table.get_side(index, 'right'))
            targets_cases.append(context.table.get_side(index, 'bottom'))
            targets_cases.append(context.table.get_side(index, 'left'))

    
            #se duplique sur les cases spéciales en priorité
            for case in targets_cases:
                if case is not None and type(case) != DefaultCase and type(case) not in none_divisable_case:
                    target_case = case
                    break
            
            #si aucune case spéciale trouvée se duplique sur la case normal adjacente
            if target_case is None:
                for case in targets_cases:
                    if case is not None and type(case) not in none_divisable_case:
                        target_case = case
                        break

            if target_case is not None:
                marker = target_case.get_marker()
                case = DivisionCase()
                context.add_changed_case(target_case, case)
                context.add_marker(case, marker)


        return context
    
class EmptyCase(Case):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(8, 0)
        self.blit_image()

    def can_place(self):
        return False

class BurningCase(Case):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(9, 0)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            index = context.table.get_index(self) if context.index is None else context.index
            table = context.table.get_case_list()
            empty_case_list = [case for case in table if isinstance(case, EmptyCase)]
            select_table = table.copy()
            select_table.remove(context.table.get_case(index))
            #on eleve les cases vide du compte
            for empty_case in empty_case_list:
                select_table.remove(empty_case)
            
            #si toutes les cases sont vides, ne fait rien
            if len(select_table) != 0:
                if len(select_table) == 1:
                    burned_case = select_table[0]
                else:
                    burned_case = random.choice(select_table)

                context.add_changed_case(burned_case, EmptyCase())
                context.add_marker(burned_case, None)

        return context
                

class MoneyCase(Case):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(7, 0)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            gain = random.randint(0, 20)
            context.add_gain(context.player, gain)
        return context
    
class InterestCase(Case):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(0, 1)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.end_round:
            player = self.get_owner()
            if player is not None:
                money = player.get_balance()
                gain = int(money * 0.1) + 1
                context.add_gain(player, gain)
        return context
    
class ChainCase(Case):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(1, 1)
        self.blit_image()
        self.owner = None
        self.placable = True

    def trigger_effect(self, context : GameContext):
        if context.try_place:
            if self.owner is None:
                self.set_owner(context.player)

            if context.player == self.owner:
                self.placable = True
            else:
                self.placable = False
        return context
    
    def set_owner(self, player):
        self.owner = player

    def can_place(self):
        return self.placable and self.marker is None

    
class BluePrintCase(Case):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(5, 0)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        index = context.table.get_index(self)
        copied_case = context.table.get_side(index, 'right')
        if copied_case is not None and not context.blueprint:
            context.blueprint = True
            context.index = index
            context = copied_case.trigger_effect(context)
            context.blueprint = False
            context.index = None
        return context
    
class DeathCase(Case):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(2, 1)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            cases_list = context.table.get_case_list()
            current_player_list = []
            other_player_list = []

            for case in cases_list:
                if case.get_owner() is not None:
                    if case.get_owner() == context.player:
                        current_player_list.append(case)
                    else:
                        other_player_list.append(case)

            dead_player_list : list = random.choices([current_player_list, other_player_list])[0]

            if dead_player_list != []:
                for killed_case in dead_player_list:
                    if self == killed_case:
                        context.add_changed_case(self, DefaultCase())
                        context.add_marker(self)
                    else:
                        context.add_marker(killed_case)     

                if self not in dead_player_list:
                    d_case = DefaultCase()
                    context.add_changed_case(self, d_case)
                    context.add_marker(d_case, self.get_marker())
            

        return context

class ItemCase(Case):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(3, 1)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            current_player = context.player
            inventory = context.game_session.get_inventory(current_player)
            item = Item(self.pos, ItemConfig.ITEM_SIZE, ItemConfig.ITEM_SIZE, object= generate_random_case())
            if inventory.can_add_item():
                inventory.add_item(item)
        return context
    

class RandomCase(Case):
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.get_image(4, 1)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            shuffled_cases = context.table.get_case_list().copy()
            random.shuffle(shuffled_cases)
            copied_cases = []
            for case in shuffled_cases:
                current_case = type(case)() if case != self else DefaultCase()
                copied_cases.append(current_case)
            
            for i, case in enumerate(copied_cases):
                base_case = context.table.get_case_list()[i]

                context.add_changed_case(base_case, case)
                context.add_marker(case, base_case.get_marker())

            
        return context
    
class CreeperCase(Case):
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.get_image(5, 1)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            index = context.table.get_index(self)
            destroyed_cases = []
            destroyed_cases.append(self)
            destroyed_cases.append(context.table.get_side(index, 'top'))
            destroyed_cases.append(context.table.get_side(index, 'right'))
            destroyed_cases.append(context.table.get_side(index, 'bottom'))
            destroyed_cases.append(context.table.get_side(index, 'left'))

            for case in destroyed_cases:
                if case is not None:
                    context.add_changed_case(case, EmptyCase())
                    context.add_marker(case, None)

        return context
    
class FirstCase(Case):
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.get_image(6, 1)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.end_round:
            owner = self.get_owner()
            if owner is not None:
                if context.first_to_play is None:
                    context.first_to_play = owner
                else:
                    activate = random.randint(0, 1)
                    if activate == 1:
                        context.first_to_play = owner

        return context
    