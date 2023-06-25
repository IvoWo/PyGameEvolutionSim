import pygame
from sys import exit
import AnimalClass
import PlantClass
import random

pygame.init()
ScreenSize = (600, 600 )
screen = pygame.display.set_mode(ScreenSize)
pygame.display.set_caption('Pixellife')
clock = pygame.time.Clock()
PauseGame = False

mutationRate = 0.05

# instanciate groups
herbivoreGroup = pygame.sprite.Group()
carnivoreGroup = pygame.sprite.Group()
plantGroup = pygame.sprite.Group()
groupList = [plantGroup, carnivoreGroup, herbivoreGroup]
# animalGroupList = [carnivoreGroup, herbivoreGroup]


# load background image
background_surf = pygame.transform.rotozoom(pygame.image.load('Pictures\ground.jpg').convert_alpha(), 0, 2)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            PauseGame = not PauseGame
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(' \n this mouseclick: \n')
            MousePosition = pygame.mouse.get_pos()
            for group in groupList:
                    for s in [s for s in group if s.rect.collidepoint(MousePosition)]:
                        s.getAttributes()

    if PauseGame:
        pass
    else:
        if not plantGroup:
            Position = tuple(random.randint(10, ScreenSize[0]) for i in range(2))
            plantGroup.add(PlantClass.PlantClass(Position, ScreenSize, plantGroup, mutationRate))
        if not herbivoreGroup:
            Position = tuple(random.randint(10, ScreenSize[0]) for i in range(2))
            herbivoreGroup.add(AnimalClass.AnimalClass(Position, 'Pictures/herbivore1.png', ScreenSize, herbivoreGroup, mutationRate))
        if not carnivoreGroup: 
            Position = tuple(random.randint(10, ScreenSize[0]) for i in range(2))
            carnivoreGroup.add(AnimalClass.AnimalClass(Position,'Pictures/carnivore1.png', ScreenSize, carnivoreGroup, mutationRate))

        if len(plantGroup) > 50:
            for sprite in plantGroup.sprites()[50:]:
                sprite.kill()
        if len(herbivoreGroup) > 20:
            for sprite in herbivoreGroup.sprites()[20:]:
                sprite.kill()
        if len(carnivoreGroup) > 15:
            for sprite in carnivoreGroup.sprites()[15:]:
                sprite.kill()

        # collision_dict = pygame.sprite.groupcollide(herbivoreGroup, carnivoreGroup, False, False)
        # for spriteOne in collision_dict.keys():
        #     distance = AnimalClass.vectorBetweenPoints(spriteOne.rect.center, collision_dict.get(spriteOne)[0].rect.center)
        #     spriteOne.rect.center = AnimalClass.vectorBetweenPoints(spriteOne.rect.center, distance)
        #     collision_dict.get(spriteOne)[0].rect.center = AnimalClass.vectorBetweenPoints(collision_dict.get(spriteOne)[0].rect.center , - distance)
            # spriteTuple[1].rect.x -= 2
        
        # for group in animalGroupList:
        #     for animal in group:
        #         pygame.sprite.DirtySprite
        

        screen.blit(background_surf, (0,0))

        # animate groups
        plantGroup.draw(screen)
        herbivoreGroup.draw(screen)
        carnivoreGroup.draw(screen)
        herbivoreGroup.update(plantGroup, carnivoreGroup)
        carnivoreGroup.update(herbivoreGroup, herbivoreGroup)
        plantGroup.update()

    pygame.display.update()
    clock.tick(60)

