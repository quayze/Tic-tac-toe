import pygame
from square import *
from bonus_squares import *
from marker import Marker
from context import GameContext
import random
from random_square import *
from drawable import *
from effect import *
from effect_group import *

class Table(Drawable):
    def __init__(self, game):
        super().__init__(1)
        self.center = pygame.Vector2(WIDTH//2, HEIGHT//2)
        self.game = game
        self.curr_effects = EffectGroup()
        self.game.add_object(self)
        self.squares_list = []

        self.extended = False


    def spawn_squares(self):
        self.squares_list.clear()
        test_square = Square()
        offset = TableConfig.OFFSET
        square_mid_size = test_square.rect.width//2
        center_offset = square_mid_size*2 + offset
        topleft = self.center + pygame.Vector2(-center_offset, -center_offset)
        for y in range(0, 3):
            for x in range(0, 3):
                current_topleft = topleft + pygame.Vector2(center_offset*x, center_offset*y)
                self.squares_list.append(DefaultSquare(current_topleft))


    def reset_squares(self, context : GameContext):
        # Reset all markers
        for square in self.squares_list:
            if square.marker is not None:
                self.game.remove_object(square.marker)

        #save all old squares
        old_squares = self.squares_list.copy()
        #reset
        self.squares_list = []

        test_square = Square()
        offset = TableConfig.OFFSET
        square_mid_size = test_square.rect.width//2

        center_offset = square_mid_size*2 + offset
        topleft = self.center + pygame.Vector2(-center_offset, -center_offset)
        
        for y in range(0, 3):
            for x in range(0, 3):
                current_topleft = topleft + pygame.Vector2(center_offset*x, center_offset*y)
                self.squares_list.append(DefaultSquare(current_topleft))

        breaking_squares = []
        for i, square in enumerate(old_squares):
            if isinstance(square, StoneSquare):
                self.squares_list[i] = square
            else:
                breaking_squares.append(square)


        context = self.break_squares(context, breaking_squares)
        old_squares.clear()


        self.extended = False

        return context
                    
    
    def nearest_square(self, pos):
        min_square = self.squares_list[0]
        min = min_square.get_pos().distance_to(Vector2(pos)) 
        for square in self.squares_list:
            if square.get_pos().distance_to(Vector2(pos)) < min:
                min = square.get_pos().distance_to(Vector2(pos))
                min_square = square
        if Vector2(min_square.get_pos()).distance_to(Vector2(pos)) > 200:
            return None
        return min_square
    

    
    
    def get_result(self):
        for result in TableConfig.WINNING_COMBINATION:
            first_index = result[0]
            reference_square =  self.squares_list[first_index].get_marker()
            win = True
            if reference_square is None:
                win = False
            if win:
                for index in result:
                    square = self.squares_list[index]
                    if square.get_marker() is None:
                        win = False
                    elif square.get_marker().owner != reference_square.owner:
                        win = False
            if win:
                return 'win', reference_square.owner, [self.get_square(index) for index in result]
            
        if self.extended:
            for result in TableConfig.EXETEND_WIN_COMBINATION:
                first_index = result[0]
                reference_square =  self.squares_list[first_index].get_marker()
                win = True
                if reference_square is None:
                    win = False
                if win:
                    for index in result:
                        square = self.squares_list[index]
                        if square.get_marker() is None:
                            win = False
                        elif square.get_marker().owner != reference_square.owner:
                            win = False
                if win:
                    return 'win', reference_square.owner, [self.get_square(index) for index in result]
            
            
        for square in self.squares_list:
            empty_square = square.counting is False
            if square.get_marker() is None and not empty_square:      
                return 'ongoing', None, None
        return 'draw', None, None
    
    def trigger_abilities(self, context):
        for square in self.squares_list:
            context = square.trigger_effect(context)
        return context

    def trigger_end_round_ablility(self, context):
        context.end_round = True
        for square in self.squares_list:
            context = square.trigger_effect(context)
        return context
    
    
    def try_place_square(self, item : SquareItem):
        nearest_square : Square = self.nearest_square(item.get_pos())
        if nearest_square is not None :
            square : Square = item.get_object()
            if type(nearest_square) in square.placable and nearest_square.can_place():
                return self.get_index(nearest_square)
        return None
    
    def try_place_marker(self, marker, context : GameContext):
        nearest_square : Square = self.nearest_square(marker.get_pos())
        if nearest_square is not None :
            context.try_place = True
            nearest_square.trigger_effect(context)
            if nearest_square.can_place() is True:
                context.try_place = False
                return nearest_square, context
        return None, context

    
    def place_marker(self, marker, context : GameContext, square : Square):
        current_square : Square = square
        current_square.place_marker(marker)
        context.marker_placed = True
        context = current_square.trigger_effect(context)
        context.marker_placed = False
        self.game.add_effect(SoundEffect(sound_path= SFX.POP))
        return context
    
    def place_square(self, square : Square, old_square_index : int, context : GameContext):
        old_square = self.get_square(old_square_index)
        self.change_square(square, old_square_index)
        context.add_effect(PlaceSquareEffect(old_square.get_pos(), square.rarity))
        
        full_stone = True
        for square in self.squares_list:
            if not isinstance(square, StoneSquare):
                full_stone = False
        if full_stone == True:
            for square in self.squares_list:
                context.add_changed_square(square, DefaultSquare())
                context.add_effect(FallEffect(square.get_pos(), 1, square.surface, angle_offset= 70, speed= (800, 1200)))

            context.add_effect(SoundEffect(SFX.BREAKING))
            context.add_effect(ScreenShakeEffect(offset_x= 30, offset_y= 30))
        return context

        
    def update(self, dt):
        for square in self.squares_list:
            square.update(dt)        

    def draw(self, surface):
        for square in self.squares_list:
            square.draw(surface)

    def get_index(self, square : Square):
        return self.squares_list.index(square)
    
    def get_square(self, index):
        if 0 <= index < len(self.squares_list):
            return self.squares_list[index]
        else:
            return
    def get_square_list(self):
        return self.squares_list
    
    def apply_context(self, context : GameContext):
        if context.extend_table:
            self.add_squares()

        for square, new_square in context.changed_square.items():  
            new_square : Square = new_square
            index = self.get_index(square)
            self.change_square(new_square, index)
            
        for square, marker in context.changed_markers.items():
            if marker is None:
                square.remove_marker()
                
            elif square.can_place():
                square.place_marker(marker)
                self.game.add_object(marker)
            else:
                square.remove_marker()
                square.place_marker(marker)
                self.game.add_object(marker)

        context.changed_markers = {}
        context.changed_square = {}
        return context
    
    def change_square(self, square : Square, index : int):
        old_square : Square = self.squares_list[index]
        square.set_pos(old_square.get_pos())
        self.squares_list[index] = square

    def get_side(self, index, side_name):
        if side_name == 'left':
            if self.extended:
                if index == 9: return self.get_square(2)
                elif index == 10: return self.get_square(5)
                elif index == 11: return self.get_square(8)
            return self.get_square(index -1) if index not in [0, 3, 6] else None

        elif side_name == 'right':
            if self.extended:
                if index  in [9, 10, 11]:
                    return None
                elif index == 2: return self.get_square(9)
                elif index == 5: return self.get_square(10)
                elif index == 8: return self.get_square(11)
                else:
                    self.get_square(index +1)
            
            return self.get_square(index +1) if index not in [2, 5, 8] else None
        
        elif side_name == 'top':
            if self.extended and index in [11, 10, 9]:
                return self.get_square(index - 1)
            return self.get_square(index -3)
        
        elif side_name == 'bottom':
            if self.extended:
                if index in [11, 10, 9]:
                    return self.get_square(index + 1)
                elif index in [6, 7, 8]:
                    return None
            return self.get_square(index +3)
        
        
    def destroy(self, context : GameContext):
        
        context = self.break_squares(context, self.squares_list)
        self.squares_list.clear()

        return context
    
    def break_squares(self, context, squares_list):
        for square in squares_list:
            context.add_effect(
                FallEffect(
                square.get_pos(), amount= 1, surface= square.surface,
                speed= (800, 1300), angle_offset= 30, z_index= 2,
            ))
            if square.marker is not None:
                context.add_effect(
                    FallEffect(
                    square.get_pos(), amount= 1, surface= square.get_marker().image,
                    speed= (800, 1300), angle_offset= 30, z_index= 2
                ))      
                square.remove_marker()

        context.add_effect(SoundEffect(SFX.BREAKING))
        context.add_effect(ScreenShakeEffect(offset_x= 30, offset_y= 30))

        return context


    
    def add_squares(self):
        if self.extended:
            return
        right_square : Square = self.squares_list[2]
        last_center = right_square.get_pos()
        x_pos = last_center[0] + right_square.surface.get_width() + TableConfig.OFFSET
        y_pos = last_center[1]
        for idx in range(3):
            current_y_pos = y_pos + (right_square.surface.get_height() + TableConfig.OFFSET) * idx
            square = DefaultSquare((x_pos, current_y_pos))
            self.squares_list.append(square)
            
        self.extended = True


    def activate(self):
        self.game.add_object(self)

    def copy(self):
        table = Table(self.game)
        table.squares_list = self.squares_list
        return table
    
                


        
        