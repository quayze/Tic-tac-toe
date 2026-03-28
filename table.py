import pygame
from case import *
from bonus_case import *
from marker import Marker
from context import GameContext
import random
from random_case import *
from drawable import *

class Table(Drawable):
    def __init__(self, game):
        super().__init__(1)
        self.center = pygame.Vector2(WIDTH//2, HEIGHT//2)
        self.game = game
        self.game.add_object(self)
        self.cases_list = []
        self.reset_cases()

    
    
    def reset_cases(self):
        for case in self.cases_list:
            if case.marker is not None:
                self.game.remove_object(case.marker)

        self.cases_list = []
        test_case = Case((0, 0))
        offset = TableConfig.OFFSET
        case_mid_size = test_case.rect.width//2

        center_offset = case_mid_size*2 + offset
        topleft = self.center + pygame.Vector2(-center_offset, -center_offset)
        
        for y in range(0, 3):
            for x in range(0, 3):
                current_topleft = topleft + pygame.Vector2(center_offset*x, center_offset*y)
                self.cases_list.append(get_random_case(current_topleft))


    
    
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
                return 'win', reference_case.owner
            
            
        for case in self.cases_list:
            empty_case = isinstance(case, EmptyCase) is True
            if case.get_marker() is None and not empty_case:

                empty_cases = [c for c in self.cases_list if c.get_marker() is None and not isinstance(c, EmptyCase)]
                chain_owners = set(c.owner for c in empty_cases if isinstance(c, ChainCase) and c.owner is not None)
                if all(isinstance(c, ChainCase) for c in empty_cases) and len(chain_owners) == 1:
                    return 'win', case.owner
                
                return 'ongoing', None
            
        return 'draw', None
    
    def trigger_abilities(self, context):
        for case in self.cases_list:
            context = case.trigger_effect(context)
        return context

    def trigger_end_round_ablility(self, context):
        context.end_round = True
        for case in self.cases_list:
            context = case.trigger_effect(context)
        return context
    
    
    def try_place_case(self, item):
        nearest_case : Case = self.nearest_case(item.get_pos())
        if nearest_case is not None : 
            if isinstance(nearest_case, DefaultCase) and nearest_case.can_place():
                return self.get_index(nearest_case)
        return None
    
    def try_place_marker(self, marker, context : GameContext):
        nearest_case : Case = self.nearest_case(marker.get_pos())
        if nearest_case is not None :
            context.try_place = True
            nearest_case.trigger_effect(context)
            if nearest_case.can_place() is True:
                context.try_place = False
                return nearest_case, context
        return None, context

    
    def place_marker(self, marker, context : GameContext, case : Case):
        current_case : Case = case
        current_case.place_marker(marker)
        context.marker_placed = True
        context = current_case.trigger_effect(context)
        context.marker_placed = False
        return context

        
    def update(self, dt):
        for case in self.cases_list:
            case.update(dt)        

    def draw(self, surface):
        for case in self.cases_list:
            case.draw(surface)

    def get_index(self, case : Case):
        return self.cases_list.index(case)
    
    def get_case(self, index):
        if 0 <= index < len(self.cases_list):
            return self.cases_list[index]
        else:
            return
    def get_case_list(self):
        return self.cases_list
    
    def apply_context(self, context : GameContext):
        for case, new_case in context.changed_case.items():
            new_case : Case = new_case
            index = self.get_index(case)
            self.change_case(new_case, index)
            
        for case, marker in context.changed_markers.items():
            if marker is None:
                self.game.remove_object(case.marker)
                case.set_marker()
                
            elif case.can_place():
                case.place_marker(marker)
                self.game.add_object(marker)

        context.changed_markers = {}
        context.changed_case = {}
        return context
    
    def change_case(self, case : Case, index : int):
        old_case : Case = self.cases_list[index]
        case.set_pos(old_case.get_pos())
        self.cases_list[index] = case

    def get_side(self, index, side_name):
        if side_name == 'left':
            return self.get_case(index -1) if index not in [0, 3, 6] else None

        elif side_name == 'right':
            return self.get_case(index +1) if index not in [2, 5, 8] else None
        
        elif side_name == 'top':
            return self.get_case(index -3)
        
        elif side_name == 'bottom':
            return self.get_case(index +3)
    
                


        
        