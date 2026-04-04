from square import Square
from settings import *
from functions import *
from context import GameContext
import random
from marker import Marker
import pygame
from item import *
from effect import *
import importlib


def generate_random_case():
    data : dict = get_all_squares_data()
    classes, weights = [], []
    module = importlib.import_module('bonus_squares')

    for class_name, info in data.items():
        weight = CaseConfig.RARITY_WEIGHTS.get(info['rarity'], 0)
        if weight != 0:
            cls = getattr(module, class_name, None)
            if cls is not None:
                classes.append(cls)
                weights.append(weight)
    
    square_type = random.choices(classes, weights=weights)[0]

    return square_type()



#----------------------------------------------
# DEFAULT SQUARE
#----------------------------------------------

class DefaultSquare(Square):
    """Base case functionning"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image()
        self.blit_image()

    def trigger_effect(self, context):
        return context

#----------------------------------------------
# COMMON SQUARES
#----------------------------------------------


class ReplaySquare(Square):
    """Replay if marker placed"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(1, 0)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            context.replay = True

        return context
    
class ReplaceableSquare(Square):
    """Replace 1 time if ennemy marker on it"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(2, 0)
        self.blit_image()
        self.effect_triggered = False

    def trigger_effect(self, context : GameContext):
        if context.try_place and self.marker is not None and context.player != self.get_owner():
            self.marker.kill()
            self.marker = None
            if not context.blueprint: self.effect_triggered = True # no unknown variable for blueprint

        elif not context.blueprint and context.marker_placed and self.effect_triggered: #no self destruct if executed by blueprint / no unknown variable for blueprint
            new_case = DefaultSquare()
            context.add_changed_case(self, new_case)
            context.add_marker(new_case, self.marker)

        return context

    

class SideSquare(Square):
    """Add marker to a case on one of it side"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(3, 0)
        self.side = random.randint(0, 3)
        self.image = pygame.transform.rotate(self.image, self.side * -90)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            index = context.table.get_index(self)
            
            if context.blueprint : self.side = random.randint(0, 3)

            #haut
            if self.side == 0:
                target_case : Square = context.table.get_side(index, 'top')
            #droite
            elif self.side == 1:
                target_case : Square = context.table.get_side(index, 'right')
            #bas
            elif self.side == 2:
                target_case : Square = context.table.get_side(index, 'bottom')
            #gauche
            elif self.side == 3:
                target_case : Square = context.table.get_side(index, 'left')
            
            
            if target_case is not None and target_case.can_place():
                marker_pos = target_case.get_pos()
                marker = Marker(owner= context.player, pos= marker_pos)
                context.add_marker(target_case, marker)

        return context


class KillSquare(Square):
    """Destroy 1 ennemy marker and square"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(4, 0)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            list = context.table.get_case_list()
            killable_list = []
            for case in list:
                if case.get_owner() is not None and case.get_owner() != context.player:
                    killable_list.append(case)

            if killable_list != []:
                if len(killable_list) == 1:
                    kill = killable_list[0]
                else:
                    kill : Square = random.choices(killable_list)[0]
                    

                context.add_changed_case(kill, DefaultSquare())
                context.add_marker(kill, None)
                # Effects
                context.add_effect(BloodEffect(
                    kill.get_pos(), direction= kill.get_pos() - self.pos
                ))
                context.add_effect(
                    TargetEffect(
                    self.pos, amount= 1, surface= load_image('bullet', PartConfig.BULLET), 
                    target= kill.get_pos(), scale_range=(8, 8), life_time= (0.1, 0.1),
                    adaptative_angle= True, kill_duration= 0.1, sound= SFX.GUN
                ))


        return context
    
class DivisionSquare(Square):
    """Replace nearby case with its type, +on other bonus squares"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(6, 0)
        self.blit_image()



    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            index = context.table.get_index(self)
            none_divisable_case = [DivisionSquare, EmptySquare]

            targets_cases = []
            target_case = None

            targets_cases.append(context.table.get_side(index, 'top'))
            targets_cases.append(context.table.get_side(index, 'right'))
            targets_cases.append(context.table.get_side(index, 'bottom'))
            targets_cases.append(context.table.get_side(index, 'left'))

    
            #se duplique sur les cases spéciales en priorité
            for case in targets_cases:
                if case is not None and type(case) != DefaultSquare and type(case) not in none_divisable_case:
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
                case = DivisionSquare()
                context.add_changed_case(target_case, case)
                context.add_marker(case, marker)


        return context
    
class EmptySquare(Square):
    """Can't place marker on it"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(8, 0)
        self.blit_image()
        self.counting = False

    def can_place(self):
        return False

class BurningSquare(Square):
    """Transform on random square into empty square except itself"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(9, 0)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            index = context.table.get_index(self)
            table = context.table.get_case_list()
            empty_case_list = [case for case in table if isinstance(case, EmptySquare)]
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

                context.add_changed_case(burned_case, EmptySquare())
                context.add_marker(burned_case, None)

        return context
                

class MoneySquare(Square):
    """Gives random amount of $ to the player who place the marker on it"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(7, 0)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            gain = random.randint(0, 10)
            context.add_gain(context.player, gain)
        return context
    
class InterestSquare(Square):
    """Gives 10% of player's balance if on of his case is on it"""
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
    
class ChainSquare(Square):
    """Can define on play who will be the only one who can place a marker on it"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(1, 1)
        self.blit_image()
        self.owner = None
        self.icon = None
        self.placable = True
        self.blueprint = False

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
        self.get_icon()

    def get_icon(self):
        if self.owner is not None:
            icon = get_marker(self.owner.marker_type)
            self.icon = resize(icon, PIXEL_SIZE*0.3)

    def can_place(self):
        return self.placable and self.marker is None
    
    def draw(self, screen):
        super().draw(screen)
        if self.icon is not None:
            screen.blit(self.icon, (self.rect.left +PIXEL_SIZE*3, self.rect.top +PIXEL_SIZE*3))
    


class ItemSquare(Square):
    """Gives one random item to the player who placed the marker"""
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
    

class RandomSquare(Square):
    """Shuffle all squares on the table except empty cases"""
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.get_image(4, 1)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            all_squares = context.table.get_case_list().copy()
            changed_squares = []
            shuffled_squares = []
            final_dict = {}
            for square in all_squares:
                if square is not self and type(square) not in (EmptySquare, ChainSquare):
                    changed_squares.append(square)
                    shuffled_squares.append(type(square))

            if len(shuffled_squares) > 1:
                random.shuffle(shuffled_squares)
                for i, square in enumerate(changed_squares):
                    final_dict[square] = shuffled_squares[i]
                for base_square, new_type in final_dict.items():
                    new_square = new_type()
                    context.add_changed_case(base_square, new_square)
                    context.add_marker(new_square, base_square.get_marker())

                new_self = DefaultSquare()
                context.add_changed_case(self, new_self)
                context.add_marker(new_self, self.get_marker())

                for square in all_squares:
                    context.add_effect(
                    VanishEffect(
                    square.get_pos(), amount= 1, surface= load_image('q_mark_case', PartConfig.Q_MARK_SQUARE), 
                    scale_range= (PIXEL_SIZE, PIXEL_SIZE), life_time= (0.3, 1), z_index= 5
                ))


        return context
    

    
class FirstSquare(Square):
    """Player start next round if marker placed on it"""
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


class JailSquare(Square):
    """-5$ or -30% at the end of the round but add a chain case linked to the player on the table"""
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.get_image(7, 1)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            case_list = context.table.get_case_list()
            potential_cases = []
            for case in case_list:
                if isinstance(case, DefaultSquare) and case.get_marker() is None:
                    potential_cases.append(case)
            if len(potential_cases) < 1:
                for case in case_list:
                    if self != case and case.get_marker() is None and not isinstance(case, ChainSquare):
                        potential_cases.append(case)
            
            if potential_cases != []:
                random.shuffle(potential_cases)
                case = potential_cases[0]
                
                chain_case = ChainSquare()
                chain_case.set_owner(context.player)
                context.add_changed_case(case, chain_case)


        elif context.end_round:
            player = self.get_owner()
            if player is not None:
                total_money = player.get_balance()
                lost = max(5, int(total_money*0.3))
                context.add_lost(player, lost)

        return context
    
#----------------------------------------------
# RARE SQUARES
#----------------------------------------------

class BluePrintSquare(Square):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image(5, 0)
        self.blit_image()
        self.blueprint = False

    def trigger_effect(self, context : GameContext):
        index = context.table.get_index(self)
        target_case : Square = context.table.get_side(index, 'right')
            
        if target_case is not None:
            self.counting = target_case.counting
            if target_case.blueprint:
                context.blueprint = True
                effect = target_case.trigger_effect.__func__.__get__(self, target_case)
                context = effect(context)
                context.blueprint = False

        return context

class DeathSquare(Square):
    """50/50 kill all ennemy squares or all player squares"""
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
                    if self == killed_case and not context.blueprint: #no self destruct if executed by blueprint
                        context.add_changed_case(self, DefaultSquare())
                        context.add_marker(self)
                    else:
                        context.add_marker(killed_case)     

                if self not in dead_player_list and not context.blueprint: #no self destruct if executed by blueprint
                    d_case = DefaultSquare()
                    context.add_changed_case(self, d_case)
                    context.add_marker(d_case, self.get_marker())

                for square in dead_player_list:
                    context.add_effect(
                    VanishEffect(
                    square.get_pos(), amount= 1, surface= load_image('ghost', PartConfig.GHOST), 
                    scale_range= (8, 8), life_time= (1, 1), z_index= 20, dir_range_x= (0, 0),
                    dir_range_y= (-1, -1), speed_range=(100, 150), base_alpha= 150
                ))
            

        return context

class CreeperSquare(Square):
    """Transform itself and up to 4 adjacent cases into empty cases"""
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
                    context.add_changed_case(case, EmptySquare())
                    context.add_marker(case, None)

        return context



#----------------------------------------------
# LEGENDARY SQUARES
#----------------------------------------------

class DestructionSquare(Square):
    """Destroy all bonus squares on the table"""
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.get_image(0, 3)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            squares = context.table.get_case_list()
            for square in squares:
                if square != self and not isinstance(square, DefaultSquare):
                    new_case = DefaultSquare()
                    context.add_changed_case(square, new_case)
                    context.add_marker(new_case, square.get_marker())

        return context

class DiamondSquare(Square):
    """Gives 20 $ if player balance < 20 else double money, 10% interest a the end of the round"""
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.get_image(1, 3)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            current_player = context.player
            money = current_player.get_balance()
            if money < 20:
                context.add_gain(current_player, 20)
            else:
               gain = money
               context.add_gain(current_player, gain) 

        elif context.end_round:
            player = self.get_owner()
            if player is not None:
                money = player.get_balance()
                gain = int(money * 0.2) + 1
                context.add_gain(player, gain)

        return context

class LuckySquare(Square):
    """1/2 -> give legendary square on placement else rare square, 1/2 to re-obtain the square at the end of the round"""
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.get_image(2, 3)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            current_player = context.player
            inventory = context.game_session.get_inventory(current_player)
            item = Item(self.pos, ItemConfig.ITEM_SIZE, ItemConfig.ITEM_SIZE, object= generate_random_case())
            if inventory.can_add_item():
                inventory.add_item(item)

        elif context.end_round:
            add_self = random.randint(0, 1)
            if add_self == 1:
                current_player = self.get_owner()
                if current_player is not None:
                    inventory = context.game_session.get_inventory(current_player)
                    item = Item(self.pos, ItemConfig.ITEM_SIZE, ItemConfig.ITEM_SIZE, object= type(self)() , negative= True)
                    inventory.add_item(item)

        return context

class TableSquare(Square):
    """Extend the table on the right : 3 * 4 if not already"""
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.get_image(3, 3)
        self.blit_image()

class StoneSquare(Square):
    """Block one case permenently for 1 game """
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.get_image(4, 3)
        self.blit_image()
        self.blueprint = False
        self.counting = False

    def can_place(self):
        return False
