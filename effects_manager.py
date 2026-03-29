from effect import *

class EffectsManager:
    def __init__(self, game):
        self.effects : list[Effect] = []
        self.stopped_effects = []
        self.game = game

    def update(self, dt):
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



    def add_effect(self, effect : Effect):
        self.effects.append(effect)
        effect.start(self.game)
