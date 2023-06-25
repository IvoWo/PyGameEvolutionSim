from BasicLiving import BasicLiving

class PlantClass(BasicLiving):
    def __init__(self, position: tuple[int, int], SreenSize: tuple[int, int], OwnGroup, mutationRate):
        super().__init__(position, 'Pictures/plant.png', SreenSize, OwnGroup, mutationRate)

    # Reproduction Stats
    # MinDistanceToParent = 30
    # MaxDistanceToParent = 60

    def reproduce(self):
            super().reproduce(PlantClass(self.calcChildPosition(), self._ScreenSize,self._OwnGroup, self._mutationRate))
            # super().reproduce()

    def update(self, lightFactor= 0.4):
        super().update(lightFactor=lightFactor)

    def eat(self, lightFactor):
        self._CurrentEnergy += lightFactor