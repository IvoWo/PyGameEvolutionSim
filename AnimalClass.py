from BasicLiving import BasicLiving
import pygame
import random
import math
import numpy as np

class AnimalClass(BasicLiving):
    def __init__(self, position: tuple[int, int], pictureFilePath, SreenSize: tuple[int, int], OwnGroup, mutationRate):
        super().__init__(position,  pictureFilePath ,SreenSize, OwnGroup, mutationRate)
    # Stats:
    
    # energy related Stats:
    ConsumeEffiency = 2
    ConsumeSpeed = 0.5
    # idea: dict of food Types (foodGroups) with consume effiency stat, sum of effiency stat = 1

    # cost of living Stats
    CostOfMoving = 0.05
    
    # Reproduction Stats
    # MinDistanceToParent = 30
    # MaxDistanceToParent = 50

    # fighting Stats
    AttackDamage = 0
    Health = 100
    Defense = 10

    # Movement stats
    Movementspeed = 2
    MaxTurnAngle =  30
    _Direction = np.array([Movementspeed,0])

    # Behavior controlling Stats
    # Fear = 10
    # Hunger = 10
    # Aggression = 10
    SenseRange = 150
    Senseradius = 90

    def update(self, foodGroup, enemyGroup):
        if self._Alive:
            self.moveBehavior(foodGroup)
            self.attack(enemyGroup=enemyGroup)
        super().update(foodGroup=foodGroup)

    def search(self):
        # keycontroll
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_UP]:
        #     self.rect.y -= self.Movementspeed
        # if keys[pygame.K_DOWN]:
        #     self.rect.y += self.Movementspeed
        # if keys[pygame.K_LEFT]:
        #     self.rect.x -= self.Movementspeed
        # if keys[pygame.K_RIGHT]:
        #     self.rect.x += self.Movementspeed
        TurnAngle = random.uniform(-self.MaxTurnAngle, self.MaxTurnAngle)
        RadAngle1 = np.deg2rad(TurnAngle)
        rot = np.array([[math.cos(RadAngle1), -math.sin(RadAngle1)], [math.sin(RadAngle1), math.cos(RadAngle1)]])
        self._Direction = np.dot(rot, self._Direction)
        
        if  calcLengthOfVector(self._Direction) < abs(self.Movementspeed):
            self._Direction = scaleVectorToLength(self._Direction, self.Movementspeed)

        self.move(self._Direction)
    
    def move(self, movementVector : tuple[int, int]):
        if  calcLengthOfVector(movementVector) > self.Movementspeed:
            movementVector = scaleVectorToLength(movementVector, self.Movementspeed)
        self.rect.center = np.add(self.rect.center, movementVector)

    def goToFood(self, foodGroup: pygame.sprite.Group):
        minDistance = self.SenseRange
        minVector = ()
        for Food in foodGroup:
            VectorToFood = np.subtract(Food.rect.center, self.rect.center)
            DistanceToCurrentFood = calcLengthOfVector(VectorToFood)
            if DistanceToCurrentFood <= minDistance: 
                minDistance = DistanceToCurrentFood
                minVector = VectorToFood
        if len(minVector) != 0:
            self.move(minVector)
            return True
        return False

    def moveBehavior(self, foodGroup):
        if self.goToFood(foodGroup):
            pass
        else: self.search()
        self._CurrentEnergy -= self.CostOfMoving    

    # TO DO: max Energy from eating is foodEnergy
    #        max.Current Energy is exactly MaxEnergy
    def eat(self, foodGroup: pygame.sprite.Group):
        if pygame.sprite.spritecollide(self, foodGroup, False):
            # print('eating....')
            pygame.sprite.spritecollide(self, foodGroup, False)[0]._CurrentEnergy -= self.ConsumeSpeed
            if self._CurrentEnergy <= self.MaxEnergy:
                self._CurrentEnergy += (self.ConsumeSpeed * self.ConsumeEffiency)
            # print('Energy= ', self._CurrentEnergy)
            # print('food-energy= ', pygame.sprite.spritecollide(self, foodGroup, False)[0]._CurrentEnergy)

    def attack(self, enemyGroup: pygame.sprite.Group):
        if pygame.sprite.spritecollide(self, enemyGroup, False):
            for sprite in pygame.sprite.spritecollide(self, enemyGroup, False):
                sprite.Health -= self.AttackDamage
                self._CurrentEnergy -= self.CostOfMoving + self.AttackDamage * 0.1
   
    def identify(self, allSprites:pygame.sprite.Group):
        viewVector1 = np.add(self.rect.center, scaleVectorToLength(rotateVectorByDegree(self._Direction, self.Senseradius/2), self.SenseRange))
        viewVector2 = np.add(self.rect.center, scaleVectorToLength(rotateVectorByDegree(self._Direction, -self.Senseradius/2), self.SenseRange))
        for sprite in allSprites:
            if point_in_triangle(sprite.rect.center, self.rect.center, viewVector1, viewVector2):
                return sprite._OwnGroup

    def reproduce(self):
        super().reproduce(AnimalClass(self.calcChildPosition(),self._pictureFilePath, self._ScreenSize,self._OwnGroup, self._mutationRate))
        # super().reproduce()

def calcLengthOfVector(Vector):
    length = abs(np.sqrt(Vector.dot(Vector)))
    return length

def scaleVectorToLength(Vector, length):
    Vector = np.multiply(Vector ,(abs(length) / calcLengthOfVector(Vector)))
    return Vector

def rotateVectorByDegree(Vector, Degree): 
    RadAngle = np.deg2rad(Degree)
    rot = np.array([[math.cos(RadAngle), -math.sin(RadAngle)], [math.sin(RadAngle), math.cos(RadAngle)]])
    Vector = np.dot(rot, Vector)
    return Vector

def point_in_triangle(p, v1, v2, v3):
    """Checks whether a point is within the given triangle

    The function checks, whether the given point p is within the triangle defined by the the three corner point v1,
    v2 and v3.
    This is done by checking whether the point is on all three half-planes defined by the three edges of the triangle.
    :param p: The point to be checked (tuple with x any y coordinate)
    :param v1: First vertex of the triangle (tuple with x any y coordinate)
    :param v2: Second vertex of the triangle (tuple with x any y coordinate)
    :param v3: Third vertex of the triangle (tuple with x any y coordinate)
    :return: True if the point is within the triangle, False if not
    """
    def _test(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    b1 = _test(p, v1, v2) < 0.0
    b2 = _test(p, v2, v3) < 0.0
    b3 = _test(p, v3, v1) < 0.0

    return (b1 == b2) and (b2 == b3) 

def vectorBetweenPoints(p1, p2):
    return np.subtract(p1, p2)
