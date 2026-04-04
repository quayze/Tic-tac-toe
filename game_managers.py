from effect import *

class ScreenManager:
    def __init__(self):
        self.layers = {
            "background" : [],
            "game" : [],
        }
        self.deleted = []

    def draw(self, screen):
        self.draw_background(screen)
        self.draw_game(screen)

        self.remove_objects()

    
    def add_object(self, object):
        if object not in self.layers['game']:
            self.layers['game'].append(object)

    
    def add_removed_object(self, object):
        self.deleted.append(object)

    def remove_objects(self):
        for object in self.deleted:
            if object in self.layers['game']:
                self.layers['game'].remove(object)
        self.deleted.clear()


    def draw_background(self, screen):
        for el in sorted(self.layers['background'], key=lambda el: el.z):
            el.draw(screen)


    def draw_game(self, screen):
        for el in sorted(self.layers['game'], key=lambda el: el.z):
            el.draw(screen)
            if el.alive is False:
                self.add_removed_object(el)


class SoundManager:
    def __init__(self):
        self.master_volume = 1.0
        self.sfx_volume = 1.0
        self.music_volume = 1.0

    def play(self, sound_path):
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(self.sfx_volume * self.master_volume)
        sound.play()


class EffectsManager:
    def __init__(self, game):
        self.effects : list[Effect] = []
        self.waiting_effects : list[Effect] = []
        self.stopped_effects : list[Effect] = []
        self.game = game

    def update(self, dt):
        self.update_delayed_effects(dt)

        if self.effects == []:
            return
        
        for effect in self.effects:
            effect.update(dt)
            if not effect.alive:
                self.stopped_effects.append(effect)

        self.delete_effects()

    def delete_effects(self):
        if self.stopped_effects == []:
            return
        
        for effect in self.stopped_effects:
            self.effects.remove(effect)
        self.stopped_effects.clear()

    def update_delayed_effects(self, dt):
        if self.waiting_effects == []:
            return
        new_effects = []
        for effect in self.waiting_effects:
            effect.update_timer(dt)
            if effect.delay <= 0:
                new_effects.append(effect)

        for effect in new_effects:
            self.waiting_effects.remove(effect)
            self.start_effect(effect)



    def start_effect(self, effect : Effect):
        self.effects.append(effect)
        effect.start(self.game)


    def add_effect(self, effect : Effect):
        if effect.delay == 0:
            self.start_effect(effect)
        else:
            self.waiting_effects.append(effect)


