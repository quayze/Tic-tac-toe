class ScreenManager:
    def __init__(self):
        self.layers = {
            "background" : [],
            "game" : [],
            "shop" : [],
            "main_menu" : [],
            "ui" : []
        }

    def draw(self, screen):
        self.draw_game(screen)

    
    def add_object(self, layer, object):
        if object not in self.layers[layer]:
            self.layers[layer].append(object)

    
    def remove_object(self, layer, object):
        if object not in self.layers[layer]:
            self.layers[layer].remove(object)



    def draw_game(self, screen):
        for el in sorted(self.layers['game'], key=lambda el: el.z):
            el.draw(screen)