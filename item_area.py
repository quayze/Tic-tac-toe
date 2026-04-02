import pygame
from item import Item
from pygame import Vector2
from drawable import *

class ItemArea:
    def __init__(self, width, pos, game, max_items = 1):
        self.items_inventory : list[Item] = []
        self.items_anchors = []
        self.pos = pos
        self.slots = max_items
        self.max_items = max_items
        self.game = game

        #surface de la zone
        self.surface = pygame.Surface((width, 200)).convert()
        self.rect = self.surface.get_rect(center = self.pos)
        self.left_pos = self.rect.left
        self.y_pos = self.rect.centery
        self.right_pos = self.rect.right

        #gère l'action avec le joueur
        self.usable = True
        self.selected_object = None


    def add_item(self, item : Item):
        if item.negative: self.max_items += 1
        if len(self.items_inventory) > self.max_items:
            item.kill()
            return
        self.items_inventory.append(item)
        self.game.add_object(item)
        self.set_anchors()

    def delete_item(self, item : Item):
        if item in self.items_inventory:
            self.items_inventory.remove(item)
            if item.negative: self.max_items -= 1
            item.kill()
            self.set_anchors()

    def can_add(self, negative = False):
        max = self.max_items + 1 if negative else self.max_items
        return len(self.items_inventory) < max

    
    def set_anchors(self):
        self.get_anchors()

        for i, item in enumerate(self.items_inventory):
            item.set_anchor(self.items_anchors[i])

    def check_anchors(self):
        if self.selected_object is not None:
            available_positions = self.items_anchors.copy()
            closest_anchor = min(
            available_positions,
            key=lambda anchor: self.selected_object.pos.distance_to(anchor)
            )
            index = self.items_anchors.index(closest_anchor)
            self.items_inventory.remove(self.selected_object)
            self.items_inventory.insert(index, self.selected_object)
            self.set_anchors()




    def get_anchors(self):
        self.items_anchors = []
        if self.items_inventory == []:
            return
        
        item_center = self.items_inventory[0].get_rect().width//2

        left = self.left_pos + item_center if self.left_pos + item_center < self.right_pos else self.left_pos
        right = self.right_pos - item_center if self.right_pos - item_center > self.left_pos else self.right_pos

        item_number = len(self.items_inventory)
        span = right - left


        # si le board contient une seule carte elle part au milieu
        if item_number == 1:
            self.items_anchors.append(Vector2(left + span/2, self.y_pos))

        # si la main contient deux cartes elles sont placées loin l'une de l'autre
        elif item_number == 2:
            real_span = self.right_pos - self.left_pos 
            x_offset = max(item_center, real_span/4)
            self.items_anchors.append(Vector2(self.left_pos + x_offset, self.y_pos))
            self.items_anchors.append(Vector2(self.right_pos - x_offset, self.y_pos))

        # si la main contient trois cartes ou plus, la première et la dernière sont placés aux extrémités et les autres s'adapent au nombre total
        else:
            x_offset = span / (item_number - 1)
            for idx in range(item_number):
                self.items_anchors.append(Vector2(left + x_offset*idx, self.y_pos))


    def handle_mouse(self, mouse_pos):
        if not self.usable:
            return
        
        if self.selected_object is not None:
            self.selected_object.handle_mouse(mouse_pos)
            if self.selected_object is not None and self.selected_object.state == 'idle':
                self.selected_object = None
            return
        for item in self.items_inventory[::-1]:
            if item.get_rect().collidepoint(mouse_pos) and not pygame.mouse.get_pressed()[0]:
                self.selected_object = item

    def update(self, dt):
        for item in self.items_inventory:
            item.update(dt)
        self.check_anchors()
    
    def set_callback(self, callback):
        for item in self.items_inventory:
            item.on_release = callback

    def get_selected(self):
        return self.selected_object

    def delete(self):
        self.delete_item(self.selected_object)
        self.selected_object = None

    def delete_callback(self):
        for item in self.items_inventory:
            item.on_release = None