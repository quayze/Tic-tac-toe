from effect import *
class EffectGroup:
    def __init__(self):
        self.active_effects : list[Effect] = []

    def add_effect(self, effect, game = None):
        if isinstance(effect, MultipleEffect):
            for sub_effect in effect.get_effect_list():
                self.active_effects.append(sub_effect)
        else:
            self.active_effects.append(effect)


        if game: game.add_effect(effect)



        

    def is_done(self):
        self.active_effects = [e for e in self.active_effects if e.alive]
        return len(self.active_effects) == 0