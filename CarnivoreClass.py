import pygame
from AnimalClass import AnimalClass

class CarnivoreClass(AnimalClass):
    def __init__(self, position: tuple[int, int], SreenSize: tuple[int, int], OwnGroup, mutationRate):
        super().__init__(position, 'Pictures/carnivore1.png', SreenSize, OwnGroup, mutationRate)

    AttackDamage = 5
    Movementspeed = 10

    def collisionBehavior(self):
        pygame.sprite.collide_circle()

    def eat(self, foodGroup):
        if pygame.sprite.spritecollide(self, foodGroup, False):
            for food in pygame.sprite.spritecollide(self, foodGroup, False):
                if self._CurrentEnergy <= self.MaxEnergy:
                    self._CurrentEnergy += (self.ConsumeSpeed * self.ConsumeEffiency)