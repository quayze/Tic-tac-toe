import pygame
from square import *
from bonus_squares import *
from marker import Marker
from context import GameContext
import random
from random_case import *
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
        self.cases_list = []

        self.extended = False


    def spawn_squares(self):
        self.cases_list.clear()
        test_case = Square()
        offset = TableConfig.OFFSET
        case_mid_size = test_case.rect.width//2
        center_offset = case_mid_size*2 + offset
        topleft = self.center + pygame.Vector2(-center_offset, -center_offset)
        for y in range(0, 3):
            for x in range(0, 3):
                current_topleft = topleft + pygame.Vector2(center_offset*x, center_offset*y)
                self.cases_list.append(get_random_case(current_topleft))


    def reset_cases(self, context : GameContext):
        # Reset all markers
        for case in self.cases_list:
            if case.marker is not None:
                self.game.remove_object(case.marker)

        #save all old cases
        old_cases = self.cases_list.copy()
        #reset
        self.cases_list = []

        test_case = Square()
        offset = TableConfig.OFFSET
        case_mid_size = test_case.rect.width//2

        center_offset = case_mid_size*2 + offset
        topleft = self.center + pygame.Vector2(-center_offset, -center_offset)
        
        for y in range(0, 3):
            for x in range(0, 3):
                current_topleft = topleft + pygame.Vector2(center_offset*x, center_offset*y)
                self.cases_list.append(get_random_case(current_topleft))

        breaking_squares = []
        for i, square in enumerate(old_cases):
            if isinstance(square, StoneSquare):
                self.cases_list[i] = square
            else:
                breaking_squares.append(square)


        context = self.break_squares(context, breaking_squares)
        old_cases.clear()


        self.extended = False

        return context
                    
    
    def nearest_case(self, pos):
        min_case = self.cases_list[0]
        min = min_case.get_pos().distance_to(Vector2(pos)) 
        for case in self.cases_list:
            if case.get_pos().distance_to(Vector2(pos)) < min:
                min = case.get_pos().distance_to(Vector2(pos))
                min_case = case
        if Vector2(min_case.get_pos()).distance_to(Vector2(pos)) > 200:
            return None
        return min_case
    

    
    
    def get_result(self):
        for result in TableConfig.WINNING_COMBINATION:
            first_index = result[0]
            reference_case =  self.cases_list[first_index].get_marker()
            win = True
            if reference_case is None:
                win = False
            if win:
                for index in result:
                    case = self.cases_list[index]
                    if case.get_marker() is None:
                        win = False
                    elif case.get_marker().owner != reference_case.owner:
                        win = False
            if win:
                return 'win', reference_case.owner, [self.get_case(index) for index in result]
            
        if self.extended:
            for result in TableConfig.EXETEND_WIN_COMBINATION:
                first_index = result[0]
                reference_case =  self.cases_list[first_index].get_marker()
                win = True
                if reference_case is None:
                    win = False
                if win:
                    for index in result:
                        case = self.cases_list[index]
                        if case.get_marker() is None:
                            win = False
                        elif case.get_marker().owner != reference_case.owner:
                            win = False
                if win:
                    return 'win', reference_case.owner, [self.get_case(index) for index in result]
            
            
        for case in self.cases_list:
            empty_case = case.counting is False
            if case.get_marker() is None and not empty_case:      
                return 'ongoing', None, None
        return 'draw', None, None
    
    def trigger_abilities(self, context):
        for case in self.cases_list:
            context = case.trigger_effect(context)
        return context

    def trigger_end_round_ablility(self, context):
        context.end_round = True
        for case in self.cases_list:
            context = case.trigger_effect(context)
        return context
    
    
    def try_place_case(self, item : SquareItem):
        nearest_case : Square = self.nearest_case(item.get_pos())
        if nearest_case is not None :
            square : Square = item.get_object()
            if type(nearest_case) in square.placable and nearest_case.can_place():
                return self.get_index(nearest_case)
        return None
    
    def try_place_marker(self, marker, context : GameContext):
        nearest_case : Square = self.nearest_case(marker.get_pos())
        if nearest_case is not None :
            context.try_place = True
            nearest_case.trigger_effect(context)
            if nearest_case.can_place() is True:
                context.try_place = False
                return nearest_case, context
        return None, context

    
    def place_marker(self, marker, context : GameContext, case : Square):
        current_case : Square = case
        current_case.place_marker(marker)
        context.marker_placed = True
        context = current_case.trigger_effect(context)
        context.marker_placed = False
        self.game.add_effect(SoundEffect(sound_path= SFX.POP))
        return context
    
    def place_square(self, square : Square, old_square_index : int, context : GameContext):
        old_square = self.get_case(old_square_index)
        self.change_case(square, old_square_index)
        context.add_effect(PlaceSquareEffect(old_square.get_pos(), square.rarity))
        
        full_stone = True
        for square in self.cases_list:
            if not isinstance(square, StoneSquare):
                full_stone = False
        if full_stone == True:
            for square in self.cases_list:
                context.add_changed_case(square, DefaultSquare())
                context.add_effect(FallEffect(square.get_pos(), 1, square.surface, angle_offset= 70, speed= (800, 1200)))

            context.add_effect(SoundEffect(SFX.BREAKING))
            context.add_effect(ScreenShakeEffect(offset_x= 30, offset_y= 30))
        return context

        
    def update(self, dt):
        for case in self.cases_list:
            case.update(dt)        

    def draw(self, surface):
        for case in self.cases_list:
            case.draw(surface)

    def get_index(self, case : Square):
        return self.cases_list.index(case)
    
    def get_case(self, index):
        if 0 <= index < len(self.cases_list):
            return self.cases_list[index]
        else:
            return
    def get_case_list(self):
        return self.cases_list
    
    def apply_context(self, context : GameContext):
        if context.extend_table:
            self.add_squares()

        for case, new_case in context.changed_case.items():  
            new_case : Square = new_case
            index = self.get_index(case)
            self.change_case(new_case, index)
            
        for case, marker in context.changed_markers.items():
            if marker is None:
                case.remove_marker()
                
            elif case.can_place():
                case.place_marker(marker)
                self.game.add_object(marker)
            else:
                case.remove_marker()
                case.place_marker(marker)
                self.game.add_object(marker)

        context.changed_markers = {}
        context.changed_case = {}
        return context
    
    def change_case(self, case : Square, index : int):
        old_case : Square = self.cases_list[index]
        case.set_pos(old_case.get_pos())
        self.cases_list[index] = case

    def get_side(self, index, side_name):
        if side_name == 'left':
            if self.extended:
                if index == 9: return self.get_case(2)
                elif index == 10: return self.get_case(5)
                elif index == 11: return self.get_case(8)
            return self.get_case(index -1) if index not in [0, 3, 6] else None

        elif side_name == 'right':
            if self.extended:
                if index  in [9, 10, 11]:
                    return None
                elif index == 2: return self.get_case(9)
                elif index == 5: return self.get_case(10)
                elif index == 8: return self.get_case(11)
                else:
                    self.get_case(index +1)
            
            return self.get_case(index +1) if index not in [2, 5, 8] else None
        
        elif side_name == 'top':
            if self.extended and index in [11, 10, 9]:
                return self.get_case(index - 1)
            return self.get_case(index -3)
        
        elif side_name == 'bottom':
            if self.extended:
                if index in [11, 10, 9]:
                    return self.get_case(index + 1)
                elif index in [6, 7, 8]:
                    return None
            return self.get_case(index +3)
        
        
    def destroy(self, context : GameContext):
        
        context = self.break_squares(context, self.cases_list)
        self.cases_list.clear()

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
        right_square : Square = self.cases_list[2]
        last_center = right_square.get_pos()
        x_pos = last_center[0] + right_square.surface.get_width() + TableConfig.OFFSET
        y_pos = last_center[1]
        for idx in range(3):
            current_y_pos = y_pos + (right_square.surface.get_height() + TableConfig.OFFSET) * idx
            square = DefaultSquare((x_pos, current_y_pos))
            self.cases_list.append(square)
            
        self.extended = True


    def activate(self):
        self.game.add_object(self)

    def copy(self):
        table = Table(self.game)
        table.cases_list = self.cases_list
        return table
    
                


        
        