from square import *
from settings import *
from functions import *
from context import GameContext
import random
from marker import Marker
import pygame
from item import *
from effect import *
import importlib
from particles import *


#----------------------------------------------
# RANDOM GENERATION
#----------------------------------------------

def generate_random_square():
    data : dict = get_all_squares_data()
    classes, weights = [], []
    module = importlib.import_module('bonus_squares')

    for class_name, info in data.items():
        weight = SquareConfig.RARITY_WEIGHTS.get(info['rarity'], 0)
        if weight != 0:
            cls = getattr(module, class_name, None)
            if cls is not None:
                classes.append(cls)
                weights.append(weight)
    
    square_type = random.choices(classes, weights=weights)[0]

    return square_type()

def square_random_rarity(rarity = 'common'):
    data : dict = get_all_squares_data()
    classes = []
    module = importlib.import_module('bonus_squares')

    for class_name, info in data.items():
        curr_rarity = info['rarity']
        if curr_rarity == rarity:
            cls = getattr(module, class_name, None)
            if cls is not None:
                classes.append(cls)
    
    square_type = random.choices(classes)[0]

    return square_type()

#----------------------------------------------
# ALL SQUARES
#----------------------------------------------
def get_all_squares():
    data : dict = get_all_squares_data()
    classes = []
    module = importlib.import_module('bonus_squares')

    for class_name, info in data.items():
        cls = getattr(module, class_name, None)
        if cls is not None:
            classes.append(cls)

    return classes


#----------------------------------------------
# COMMON SQUARES
#----------------------------------------------


class ReplaySquare(Square):
    """Replay if marker placed"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            context.replay = True
            center = WIDTH // 2, HEIGHT // 2
            replay_particule = load_image('replay_particule', PartConfig.REWIND)
            context.add_effect(
                RotateEffect(center, 1, replay_particule, death_effect= FadeDeath, alpha= (230, 230),
                             scale= 25, kill_duration= 0.3, rotation_speed= 500, life_time= 0.7,
                             sound= SFX.SCRATCH
            ))
            context.add_effect(ScreenShakeEffect(0.5, 40, 0))

        return context
    
class ReplaceableSquare(Square):
    """Replace 1 time if ennemy marker on it"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.blit_image()
        self.effect_triggered = False

    def copy_attributes(self, square):
        if not hasattr(square, 'effect_triggered'):
            square.effect_triggered = False

    def trigger_effect(self, context : GameContext):
        if context.try_place and self.marker is not None and context.player != self.get_owner():
            self.marker.kill()
            context.add_effect(BreakEffect(self.get_pos(), self.marker.image, z_index= 5))
            self.marker = None
            self.effect_triggered = True

        elif context.marker_placed and self.effect_triggered:
            new_square = DefaultSquare()
            context.add_changed_square(self, new_square)
            context.add_marker(new_square, self.marker)

        return context
    


    

class SideSquare(Square):
    """Add marker to a square on one of it side"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.side = random.randint(0, 3)
        self.image = pygame.transform.rotate(self.image, self.side * -90)
        self.blit_image()

    def copy_attributes(self, square : Square):
        square.side = self.side

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            index = context.table.get_index(self)
            

            #haut
            if self.side == 0:
                target_square : Square = context.table.get_side(index, 'top')
            #droite
            elif self.side == 1:
                target_square : Square = context.table.get_side(index, 'right')
            #bas
            elif self.side == 2:
                target_square : Square = context.table.get_side(index, 'bottom')
            #gauche
            elif self.side == 3:
                target_square : Square = context.table.get_side(index, 'left')
            
            
            if target_square is not None and target_square.can_place():
                marker_pos = target_square.get_pos()
                marker = Marker(owner= context.player, pos= marker_pos)
                context.add_marker(target_square, marker)

                context.add_effect(ArrowEffect(self.get_pos(), target_square.get_pos(), 8))
                context.add_effect(SoundEffect(SFX.POP, delay= (context.recursion_depth+1) * 0.06))


        return context
    



class KillSquare(Square):
    """Destroy 1 ennemy marker and square"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            list = context.table.get_square_list()
            killable_list = []
            for square in list:
                if square.get_owner() is not None and square.get_owner() != context.player:
                    killable_list.append(square)

            if killable_list != []:
                if len(killable_list) == 1:
                    kill = killable_list[0]
                else:
                    kill : Square = random.choices(killable_list)[0]
                    

                context.add_changed_square(kill, DefaultSquare())
                context.add_marker(kill, None)
                
                # Effects
                barrel_pos = self.rect.centerx, self.rect.centery - 3*PIXEL_SIZE
                bullet = resize(load_image('bullet', PartConfig.BULLET), 8)
                context.add_effect(GunEffect(self.pos, kill.get_pos(), bullet,
                                             (0, - 3*PIXEL_SIZE), (30, 30, 30), (200, 200, 200), kill.marker.image         
                                             ))
                context.add_effect(
                    ParticleEffect(barrel_pos, 1, load_image('gun_shoot', PartConfig.SHOOT), 
                                   death_effect= FadeDeath, scale= 5, life_time= 0.5, kill_duration= 0.5, angle= (-10, 10)
                ))

        return context
    
class DivisionSquare(Square):
    """Replace nearby square with its type, +on other bonus squares"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.blit_image()



    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            index = context.table.get_index(self)
            none_divisable_square = [DivisionSquare, EmptySquare, StoneSquare]

            targets_squares = []
            target_square = None

            targets_squares.append(context.table.get_side(index, 'top'))
            targets_squares.append(context.table.get_side(index, 'right'))
            targets_squares.append(context.table.get_side(index, 'bottom'))
            targets_squares.append(context.table.get_side(index, 'left'))

    
            #se duplique sur les squares spéciales en priorité
            for square in targets_squares:
                if square is not None and type(square) != DefaultSquare and type(square) not in none_divisable_square:
                    target_square = square
                    break
            
            #si aucune square spéciale trouvée se duplique sur la square normal adjacente
            if target_square is None:
                for square in targets_squares:
                    if square is not None and type(square) not in none_divisable_square:
                        target_square = square
                        break

            if target_square is not None:
                marker = target_square.get_marker()
                square = DivisionSquare()
                context.add_changed_square(target_square, square)
                context.add_marker(square, marker)


        return context
    
class EmptySquare(Square):
    """Can't place marker on it"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.blit_image()
        self.counting = False

    def can_place(self):
        return False

class BurningSquare(Square):
    """Transform on random square into empty square except itself"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            index = context.table.get_index(self)
            table = context.table.get_square_list()
            empty_square_list = [square for square in table if not square.counting]
            select_table = table.copy()
            select_table.remove(context.table.get_square(index))
            #on eleve les squares vide du compte
            for empty_square in empty_square_list:
                select_table.remove(empty_square)
            
            #si toutes les squares sont vides, ne fait rien
            if len(select_table) != 0:
                if len(select_table) == 1:
                    burned_square = select_table[0]
                else:
                    burned_square = random.choice(select_table)

                context.add_changed_square(burned_square, EmptySquare())
                context.add_marker(burned_square, None)

        return context
                

class MoneySquare(Square):
    """Gives random amount of $ to the player who place the marker on it"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            gain = random.randint(0, 10)
            if gain > 0:
                context.add_gain(context.player, gain)
                coin = load_image('coin', PartConfig.COIN)
                context.add_effect(
                    FallEffect(
                        self.get_pos(), gain, coin, angle_offset= 30, scale=PIXEL_SIZE, 
                        speed= (500, 1200), sound= SFX.COIN_DROP, angle= (-180, 180)
                    ))
                

        return context
    
class LoseMoneySquare(Square):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            if context.player.get_balance() > 0:
                lost = random.randint(1, 5)
                context.add_lost(context.player, lost)
                coin = load_image('coin', PartConfig.COIN)
                context.add_effect(
                        CompressEffect(self.get_pos(), amount= lost*10, life_time= (0.3, 0.5), surface= coin, scale= 3,
                        alpha= 255, kill_duration= 0, distance= (100, 400), angle= (-180, 180))
                    )

        return context
    
class InterestSquare(Square):
    """Gives 10% of player's balance if on of his square is on it"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.end_round:
            player = self.get_owner()
            if player is not None:
                money = player.get_balance()
                gain = int(money * 0.1) + 1
                context.add_gain(player, gain)

                coin = load_image('coin', PartConfig.COIN)
                context.add_effect(
                    FallEffect(
                        self.get_pos(), min(50, gain), coin, angle_offset= 90, scale=7, 
                        speed= (300, 600), sound= SFX.MULT, angle= (-180, 180), gravity_direction= (0, -1)
                    ))
        return context
    
class ChainSquare(Square):
    """Can define on play who will be the only one who can place a marker on it"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
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
        self.placable = False
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
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            current_player = context.player
            inventory = context.game_session.get_inventory(current_player)
            item = SquareItem(self.pos, ItemConfig.ITEM_SIZE, ItemConfig.ITEM_SIZE, object= generate_random_square())
            if inventory.can_add_item():
                inventory.add_item(item)
        return context
    

class RandomSquare(Square):
    """Shuffle all squares on the table except empty squares"""
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            all_squares = context.table.get_square_list().copy()
            changed_squares = []
            shuffled_squares = []
            final_dict = {}
            for square in all_squares:
                if square is not self and type(square) not in (EmptySquare, ChainSquare, StoneSquare):
                    changed_squares.append(square)
                    shuffled_squares.append(type(square))

            if len(shuffled_squares) > 1:
                random.shuffle(shuffled_squares)
                for i, square in enumerate(changed_squares):
                    final_dict[square] = shuffled_squares[i]
                for base_square, new_type in final_dict.items():
                    new_square = new_type()
                    context.add_changed_square(base_square, new_square)
                    context.add_marker(new_square, base_square.get_marker())

                new_self = DefaultSquare()
                context.add_changed_square(self, new_self)
                context.add_marker(new_self, self.get_marker())

                for square in all_squares:
                    context.add_effect(
                    ParticleEffect(
                    square.get_pos(), amount= 1, surface= load_image('q_mark_square', PartConfig.Q_MARK_SQUARE), 
                    scale= PIXEL_SIZE, life_time= (0.3, 1), z_index= 5, death_effect= FadeDeath
                ))
                context.add_effect(
                    SoundEffect(sound_path= SFX.SHUFFLE)
                )


        return context
    

    
class FirstSquare(Square):
    """Player start next round if marker placed on it"""
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
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
    """-5$ or -30% at the end of the round but add a chain square linked to the player on the table"""
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            square_list = context.table.get_square_list()
            potential_squares = []
            for square in square_list:
                if isinstance(square, DefaultSquare) and square.get_marker() is None and square.counting:
                    potential_squares.append(square)

            if len(potential_squares) < 1:
                for square in square_list:
                    if self != square and square.get_marker() is None and not isinstance(square, ChainSquare) and square.counting:
                        potential_squares.append(square)
            
            if potential_squares != []:
                random.shuffle(potential_squares)
                square = potential_squares[0]
                
                chain_square = ChainSquare()
                chain_square.set_owner(context.player)
                context.add_changed_square(square, chain_square)


        elif context.end_round:
            player = self.get_owner()
            if player is not None:
                total_money = player.get_balance()
                lost = max(5, int(total_money*0.3))
                context.add_lost(player, lost)

        return context
    
class YinYangSquare(Square):
    """Add marker to a square on one of it side"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            index = context.table.get_index(self)
            
            self.sides = []

            for side in ['top', 'right', 'bottom', 'left']:
                target_square : Square = context.table.get_side(index, side)
                if target_square is not None and target_square.counting:
                    self.sides.append(target_square)
            



            
            
            if self.sides != []:
                if len(self.sides) != 1:
                    random.shuffle(self.sides)

                target_square = self.sides[0]
                if not isinstance(target_square, DefaultSquare):
                    new_square = DefaultSquare()
                    color = (0, 0, 0)
                else:
                    new_square = generate_random_square()
                    color = (255, 255, 255)

                context.add_changed_square(target_square, new_square)
                context.add_marker(new_square, target_square.get_marker())
                

                context.add_effect(ExplosionEffect(
                    target_square.get_pos(), 100, speed= (150, 350), scale= 2,
                    final_speed= 10, kill_duration= 0.2, color= color
                ))

        return context
    

class TeleportSquare(Square):
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            all_squares : list[Square] = context.table.get_square_list()
            selected_list = []
            teleported_square = None
            for square in all_squares:
                if square.marker is None and self != square and square.counting:
                    selected_list.append(square)

            if len(selected_list) == 1:
                teleported_square = selected_list[0]
            elif len(selected_list) > 1:
                teleported_square = random.choices(selected_list)[0]

            if teleported_square is not None:
                marker = Marker(context.player, teleported_square.get_pos())
                if not context.blueprint : context.add_changed_square(self, DefaultSquare())
                context.add_marker(self, None)
                context.add_marker(teleported_square, marker)


                enter_image = pygame.Surface((10, 10), pygame.SRCALPHA).convert_alpha()
                exit_image = pygame.Surface((10, 10), pygame.SRCALPHA).convert_alpha()
                enter_image.fill((0, 255, 255))
                exit_image.fill((255, 150, 0))

                context.add_effect(
                    CompressEffect(self.get_pos(), amount= 300, life_time= (0.3, 0.5), surface= enter_image, scale= (1, 3),
                    alpha= 255, kill_duration= 0, distance= (100, 400), angle= (-180, 180), sound= SFX.TELEPORTATION)
                )
                context.add_effect(
                    ParticleEffect(teleported_square.get_pos(), amount= 300, life_time= (0.3, 0.5), surface= exit_image, scale= (1, 3),
                    alpha= 255, kill_duration= 0.3, angle= (-180, 180), speed= (200, 500), death_effect= ScaleDeath)
                )
                context.add_effect(ScreenShakeEffect(0.5))


        return context
    
class PointingSquare(Square):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.side = 0
        self.base_image = self.image
        self.image = self.base_image.copy()
        self.blit_image()

    def copy_attributes(self, square : Square):
        square.side = self.side

    def trigger_effect(self, context : GameContext):
        if context.marker_placed and not context.blueprint:
            index = context.table.get_index(self)
            

            #haut
            if self.side == 0:
                target_square : Square = context.table.get_side(index, 'top')
            #droite
            elif self.side == 1:
                target_square : Square = context.table.get_side(index, 'right')
            #bas
            elif self.side == 2:
                target_square : Square = context.table.get_side(index, 'bottom')
            #gauche
            elif self.side == 3:
                target_square : Square = context.table.get_side(index, 'left')
            
            
            if target_square is not None and target_square.can_place():
                marker_pos = target_square.get_pos()
                marker = Marker(owner= context.player, pos= marker_pos)
                context.add_marker(target_square, marker)


        elif context.new_turn and not context.blueprint:
            
            self.side = (self.side + 1)%4
            self.image = pygame.transform.rotate(self.base_image, self.side * -90)
            self.blit_image()


        return context


    


    
#----------------------------------------------
# RARE SQUARES
#----------------------------------------------

class BluePrintSquare(Square):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.blit_image()
        self.blueprint = False

    def trigger_effect(self, context : GameContext):
        index = context.table.get_index(self)
        target_square : Square = context.table.get_side(index, 'right')
            
        if target_square is not None:
            self.counting = target_square.counting
            if target_square.blueprint:
                target_square.copy_attributes(self)
                context.blueprint = True
                effect = target_square.trigger_effect.__func__.__get__(self, target_square)
                context = effect(context)
                context.blueprint = False

        return context

class DeathSquare(Square):
    """50/50 kill all ennemy squares or all player squares"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            squares_list = context.table.get_square_list()
            current_player_list = []
            other_player_list = []

            for square in squares_list:
                if square.get_owner() is not None:
                    if square.get_owner() == context.player:
                        current_player_list.append(square)
                    else:
                        other_player_list.append(square)

            dead_player_list : list = random.choices([current_player_list, other_player_list])[0]

            if dead_player_list != []:
                for killed_square in dead_player_list:
                    if self == killed_square and not context.blueprint: #no self destruct if executed by blueprint
                        context.add_changed_square(self, DefaultSquare())
                        context.add_marker(self)
                    else:
                        context.add_marker(killed_square)     

                if self not in dead_player_list and not context.blueprint: #no self destruct if executed by blueprint
                    d_square = DefaultSquare()
                    context.add_changed_square(self, d_square)
                    context.add_marker(d_square, self.get_marker())

                for square in dead_player_list:
                    context.add_effect(BreakEffect(square.get_pos(), square.marker.image, z_index= 49))
                    context.add_effect(
                    ParticleEffect(
                    square.get_pos(), amount= 1, surface= load_image('ghost', PartConfig.GHOST), 
                    scale= 8, life_time= 1, z_index= 20, direction_x= 0,
                    direction_y= -1, speed=(100, 150), alpha= (150, 200), death_effect= FadeDeath
                ))
                context.add_effect(SoundEffect(sound_path= SFX.DEATH))
            

        return context

class CreeperSquare(Square):
    """Transform itself and up to 4 adjacent squares into empty squares"""
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            index = context.table.get_index(self)
            destroyed_squares : list[Square] = []
            destroyed_squares.append(self)
            destroyed_squares.append(context.table.get_side(index, 'top'))
            destroyed_squares.append(context.table.get_side(index, 'right'))
            destroyed_squares.append(context.table.get_side(index, 'bottom'))
            destroyed_squares.append(context.table.get_side(index, 'left'))

            for square in destroyed_squares:
                if square is not None and square.counting:
                    context.add_changed_square(square, EmptySquare())
                    context.add_marker(square, None)


                    if square != self:
                        context.add_effect(BreakEffect(square.get_pos(), square.surface, intensity= 1200))

            context.add_effect(FullExplosionEffect(self.get_pos()))
            context.add_effect(ScreenShakeEffect(offset_x = 30, offset_y= 30))

        return context

class LaserSquare(Square):
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.blit_image()



    def trigger_effect(self, context : GameContext):
        if context.skip_turn:
            squares : list[Square] = context.table.get_square_list()
            targets = []

            best_squares = {}

            for square in squares:
                if isinstance(square, LaserSquare):
                    if square.marker is None : quality = 2
                    elif square.get_owner() == context.player : quality = 1
                    else : quality = 0
                    best_squares[square] = quality
            
            sorted_squares = [k for k, v in sorted(best_squares.items(), key=lambda x: x[1], reverse=True)]
            if sorted_squares[0] == self:

                for square in squares:
                    if square.has_marker() and square.get_owner() != context.player and square != self:
                        targets.append(square)

                if targets != []:
                    kill_list = []
                    context.skip_turn = False

                    if len(targets) > 1: 
                        random.shuffle(targets)
                        for i in range(2):
                            kill_list.append(targets[i])
                    else:
                        kill_list.append(targets[0])

                    for killed_square in kill_list:
                        marker = Marker(context.player, killed_square.get_pos())
                        context.add_marker(killed_square, marker)

                    default_square = DefaultSquare()
                    context.add_changed_square(self, default_square)
                    context.add_marker(default_square, self.get_marker())

                    
                    # Effect
                    laser_beam = pygame.Surface((30, 100), pygame.SRCALPHA).convert_alpha()
                    laser_beam.fill((0, 255, 0))
                    marker_image = marker.image.copy()
                    marker_image.fill((100, 255, 100), special_flags= pygame.BLEND_RGBA_MULT)

                    context.add_effect(ParticleEffect(self.get_pos(), 1, self.surface, life_time= 0.9, kill_duration= 0, z_index= 5))
                    context.add_effect(BreakEffect(self.get_pos(), self.surface, delay= 0.9, z_index= 5))
                    for killed_square in kill_list:
                        context.add_effect(ParticleEffect(killed_square.get_pos(), 1, marker_image, life_time= 0, kill_duration= 1.5, 
                                                        death_effect= FadeDeath, z_index= 10))


                        context.add_effect(GunEffect(self.pos, killed_square.get_pos(), laser_beam,
                                    (-PIXEL_SIZE, 0), (0, 50, 0), (0, 120, 0), killed_square.marker.image,
                                    break_intensity= 700, sound= None   
                                    ))
                    context.add_effect(SoundEffect(SFX.LASER))


        return context
    
class TriggerSideSquare(Square):
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.side = random.randint(0, 3)
        self.image = pygame.transform.rotate(self.image, self.side * -90)
        self.blit_image()

    def copy_attributes(self, square : Square):
        square.side = self.side

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            index = context.table.get_index(self)

            #haut
            if self.side == 0:
                target_square : Square = context.table.get_side(index, 'top')
            #droite
            elif self.side == 1:
                target_square : Square = context.table.get_side(index, 'right')
            #bas
            elif self.side == 2:
                target_square : Square = context.table.get_side(index, 'bottom')
            #gauche
            elif self.side == 3:
                target_square : Square = context.table.get_side(index, 'left')
            
            context.recursion_depth += 1 
            if target_square is not None and target_square.can_place() and context.recursion_depth <= 9:
                marker_pos = target_square.get_pos()
                marker = Marker(owner= context.player, pos= marker_pos)
                context.add_marker(target_square, marker)
                context.add_triggers(target_square, 'marker_placed')

                
                context.add_effect(ExplosionEffect(target_square.get_pos(), 40, speed= (200, 400), 
                                                   life_time=(0.4, 0.6), color= (255, 255, 0), scale= 3, final_speed= 10))
                context.add_effect(ExplosionEffect(target_square.get_pos(), 30, speed= (100, 400), life_time=(0.5, 0.7), 
                                                   color= (255, 170, 0), scale= 2, final_speed= 10))
                context.add_effect(ArrowEffect(self.get_pos(), target_square.get_pos(), 8))
                context.add_effect(SoundEffect(SFX.POP, delay= context.recursion_depth * 0.06))

        return context
    
    


#----------------------------------------------
# LEGENDARY SQUARES
#----------------------------------------------

class DestructionSquare(Square):
    """Destroy all bonus squares on the table"""
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            squares = context.table.get_square_list()
            if squares != []:
                for square in squares:
                    if square != self and not isinstance(square, DefaultSquare):
                        new_square = DefaultSquare()
                        context.add_changed_square(square, new_square)
                        context.add_marker(new_square, square.get_marker())

                        context.add_effect(
                            BreakEffect(square.get_pos(), square.surface, z_index= 5, intensity= 1000)
                        )
                        context.add_effect(
                            LightningEffect(square.get_pos(), thickness= random.randint(12, 15), sound= None)
                        )
                context.add_effect(SoundEffect(sound_path= SFX.LIGHTNING))
                context.add_effect(ScreenShakeEffect(2, 30, 30))
                context.add_effect((FlashEffect((255, 255, 255), 0.5, 255, 0.1, 0.5, FadeDeath)))
                

        return context

class DiamondSquare(Square):
    """Gives 20 $ if player balance < 20 else double money, 10% interest a the end of the round"""
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            current_player = context.player
            money = current_player.get_balance()
            if money < 10:
                context.add_gain(current_player, 10)
            else:
               gain = min(100, money)
               context.add_gain(current_player, gain) 

            coin = load_image('coin', PartConfig.COIN)
            diamond = load_image('diamond', PartConfig.DIAMOND)
            context.add_effect(
                FallEffect(
                    self.get_pos(), 10, coin, angle_offset= 30, scale=PIXEL_SIZE, 
                    speed= (500, 1100), sound= SFX.COIN_DROP, angle= (-180, 180)
                ))
            context.add_effect(
                FallEffect(
                    self.get_pos(), 1, diamond, angle_offset= 20, scale=PIXEL_SIZE, 
                    speed= (800, 1100), angle= (-20, 20)
                ))
            

        elif context.end_round:
            player = self.get_owner()
            if player is not None:
                money = player.get_balance()
                gain = int(money * 0.2) + 1
                context.add_gain(player, gain)

                coin = load_image('coin', PartConfig.COIN)
                diamond = load_image('diamond', PartConfig.DIAMOND)
                context.add_effect(
                    FallEffect(
                        self.get_pos(), min(50, gain), coin, angle_offset= 90, scale=7, 
                        speed= (300, 600), sound= SFX.MULT, angle= (-180, 180), gravity_direction= (0, -1)
                    ))
                
                context.add_effect(
                    FallEffect(
                        self.get_pos(), 1, diamond, angle_offset= 90, scale=7, 
                        speed= (300, 600), sound= SFX.MULT, angle= (-180, 180), gravity_direction= (0, -1), z_index= 51
                    ))



        return context

class LuckySquare(Square):
    """1/2 -> give legendary square on placement else rare square, 1/2 to re-obtain the square at the end of the round"""
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context : GameContext):
        if context.marker_placed:
            current_player = context.player
            inventory = context.game_session.get_inventory(current_player)

            rarity = random.choices(['rare', 'legendary'])[0]
            
            if inventory.can_add_item():
                item = SquareItem(self.pos, ItemConfig.ITEM_SIZE, ItemConfig.ITEM_SIZE, object= square_random_rarity(rarity))
                inventory.add_item(item)

        elif context.end_round:
            add_self = random.randint(0, 1)
            if add_self == 1:
                current_player = self.get_owner()
                if current_player is not None:
                    inventory = context.game_session.get_inventory(current_player)
                    item = SquareItem(self.pos, ItemConfig.ITEM_SIZE, ItemConfig.ITEM_SIZE, object= type(self)() , negative= True)
                    inventory.add_item(item)

        return context

class TableSquare(Square):
    """Extend the table on the right : 3 * 4 if not already"""
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.blit_image()

    def trigger_effect(self, context: GameContext):
        if context.marker_placed:
            table = context.table

            if not table.extended:
                context.extend_table = True

            else:
                right_squares = []
                upgraded_squares = []
                right_squares.append(table.get_square(9))
                right_squares.append(table.get_square(10))
                right_squares.append(table.get_square(11))
                for square in right_squares:
                    if isinstance(square, DefaultSquare) and not square.has_marker():
                        upgraded_squares.append(square)

                if upgraded_squares != []:
                    if len(upgraded_squares) == 1:
                        selected = upgraded_squares[0]
                    else:
                        selected = random.choices(upgraded_squares)[0]

                    new_square = generate_random_square()
                    while type(new_square) in (TableSquare, StoneSquare):
                        new_square = generate_random_square()
                        
                    context.add_changed_square(selected, generate_random_square())
                    

        return context



class StoneSquare(Square):
    """Block one square permenently for 1 game """
    def __init__(self, pos=(0, 0)):
        super().__init__(pos)
        self.blit_image()
        self.blueprint = False
        self.counting = False
        self.placable = get_all_squares()
        self.placable.remove(type(self))

    def can_place(self):
        return False
