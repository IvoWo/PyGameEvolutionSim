import pygame
from random import randint, random
from numpy import add
import inspect
from copy import deepcopy

class BasicLiving(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], 
                 _pictureFilePath,
                 _ScreenSize: tuple[int, int],
                 _OwnGroup: pygame.sprite.Group, 
                 mutationRate):
        super().__init__()
        self._baseImage = pygame.image.load(_pictureFilePath).convert_alpha()
        self.image = self._baseImage
        self.rect = self.image.get_rect(center = position)
        self._OwnGroup = _OwnGroup
        self._ScreenSize = _ScreenSize
        self._pictureFilePath = _pictureFilePath
        self._mutationRate = mutationRate

    # State
    _Alive = True
    Health = 100

    # Energy Stats
    MaxEnergy = 100
    _CurrentEnergy = 50

    # Reproduction Stats
    CostOfReproduction = 40
    __MinDistanceToParent = 10
    _MaxDistanceToParent = 20

    # Phenotype
    SizeFactor = 1
    MinSize = 1

    def update(self, **kwargs):
        if self._Alive:
            self.eat(**kwargs)
            self.grow()
            self.reproduce()
            self.starve()
        self.vanish()
        self.stayOnScreen()
        self.die()
        if not self._Alive:
            self.decompose()

    def calcChildPosition(self):
        xDeviation = randint(self.__MinDistanceToParent, self._MaxDistanceToParent)
        yDeviation = randint(self.__MinDistanceToParent, self._MaxDistanceToParent)
        if random() < 0.5:
            xDeviation *= -1
        if random() < 0.5:
            yDeviation *= -1
        ChildPosition = add(self.rect.center, (xDeviation, yDeviation))
        return ChildPosition

    def reproduce(self):
        '''Adds an Instance of self.class to self._OwnGroup \n
           pass instance of self class as args'''
        if self._CurrentEnergy >= self.MaxEnergy:
            self._CurrentEnergy = self._CurrentEnergy - self.CostOfReproduction
            Child = deepcopy(self)
            Child.mutate(self._mutationRate)
            self._OwnGroup.add(Child)

    def eat(self):
        pass
        
    def grow(self):
        self.SizeFactor = abs(self.SizeFactor)
        if self.SizeFactor >= 3: self.SizeFactor = 3
        self.image = pygame.transform.scale_by(self._baseImage, abs(self.SizeFactor))
    
    def stayOnScreen(self):
        '''prevents from leaving the screen'''
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self._ScreenSize[0]:
            self.rect.right = self._ScreenSize[0]
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self._ScreenSize[1]:
            self.rect.bottom = self._ScreenSize[1]
    
    def vanish(self):
        if self._CurrentEnergy <= 0:
            self.kill()

    def die(self):
        if self.Health <= 0:
            self._Alive = False
    
    def starve(self):
        if self._CurrentEnergy <= abs(self.MaxEnergy) * 0.1:
            self._Alive = False
    
    def decompose(self):
        self._CurrentEnergy -= 0.2

    def mutate(self):
        for i in inspect.getmembers(self): 
            # to remove private and protected functions
            if not i[0].startswith('_')and not i[0].startswith('rect')and not i[0].startswith('image'):
                # To remove other methods that doesnot start with a underscore
                if not inspect.ismethod(i[1]):
                    if random() <= self._mutationRate:
                        changeFactor = (random() * 0.5)
                        if random() < 0.5:
                            changeFactor *= -1
                        changeFactor = 1 + changeFactor
                        newValue = i[1] * changeFactor
                        setattr(self, i[0], newValue)
                        # print('mutation occured: ', i, ' to ', newValue)

    def reproduce(self, ChildObject):
        if self._CurrentEnergy >= abs(self.MaxEnergy):
            self._CurrentEnergy = self._CurrentEnergy - self.CostOfReproduction
            setattr(ChildObject, '_CurrentEnergy', self.CostOfReproduction)
            for i in inspect.getmembers(self): 
                # to remove private and protected functions
                if not i[0].startswith('_')and not i[0].startswith('rect')and not i[0].startswith('image'):
                    # To remove other methods that doesnot start with a underscore
                    if not inspect.ismethod(i[1]):
                        setattr(ChildObject, i[0], i[1])
            ChildObject.mutate()
            self._OwnGroup.add(ChildObject)

    def getAttributes(self):
        print('---------Attributes---------')
        for i in inspect.getmembers(self): 
            # to remove private and protected functions
            if not i[0].startswith('_')and not i[0].startswith('rect')and not i[0].startswith('image'):
                # To remove other methods that doesnot start with a underscore
                if not inspect.ismethod(i[1]):
                    print(i)