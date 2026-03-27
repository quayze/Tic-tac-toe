class Drawable:
    def __init__(self, z):
        self.alive = True
        self.z = z

    def kill(self):
        self.alive = False

    def draw(self, screen):
        raise NotImplementedError