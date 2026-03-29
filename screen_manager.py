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