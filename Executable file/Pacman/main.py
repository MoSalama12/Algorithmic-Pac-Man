# Libraries
import pygame
import random


# Project Files
from data import *
import algorithms

pygame.init()

mapDirections = {
    "chaseUp" : [0, -1],
    "chaseDown" : [0, 1],
    "chaseLeft" : [-1, 0],
    "chaseRight" : [1, 0]
    }

class Monster:
    def __init__(self, tile, col, row, trait , color , timer):
        self.tile = tile
        self.col = col
        self.row = row
        self.worldXPosition = self.tile[self.row][self.col].col
        self.worldYPosition = self.tile[self.row][self.col].row
        self.path = algorithms.aStar(tilesRepresentation,(self.row,self.col),(11,13))
        self.trait = trait
        self.direction = -2
        self.color = color
        self.baseColor = color
        self.isFrightened = False
        self.timer = timer
        self.killed = False

    def highlightPath(self, surface):
        for i in range(1, len(self.path) - 1):
            pygame.draw.line(surface, self.color, (self.tile[self.path[i][0]][self.path[i][1]].col, self.tile[self.path[i][0]][self.path[i][1]].row),
                            (self.tile[self.path[i + 1][0]][self.path[i + 1][1]].col, self.tile[self.path[i + 1][0]][self.path[i + 1][1]].row) )

    def setPosition(self , col , row):
        self.col = col
        self.row = row
        self.worldXPosition = self.tile[self.row][self.col].col
        self.worldYPosition = self.tile[self.row][self.col].row

    def resetColor(self):
        self.color = self.baseColor

    def setDirectionBasedOnPath(self):
        if len(self.path) >= 3:
            if self.path[1][1] > self.path[2][1]: # up
                self.direction = 2
            elif self.path[1][1] < self.path[2][1]: # down
                self.direction = -2
            elif self.path[1][0] > self.path[2][0]: # right
                self.direction = -1
            elif self.path[1][0] < self.path[2][0]: # left
                self.direction = 1

    def facingWall(self, nextDirection):
        nextTile = None
        if nextDirection == 1: #up
            nextTile = self.tile[self.row - 1][self.col]
        elif nextDirection == -1: #down
            nextTile = self.tile[self.row + 1][self.col]
        elif nextDirection == 2: #left
            nextTile = self.tile[self.row][self.col - 1]
        else:
            nextTile = self.tile[self.row][self.col + 1] #right
        return nextTile.isWall

    def move(self, level, playerPosition = None):
        global corners

        if self.killed and self.row == 15 and self.col == 11  :
            self.killed = False
            self.isFrightened = False
            self.path = algorithms.aStar(tilesRepresentation,(self.row,self.col),(11,13))
            self.direction = -2
            self.resetColor()

        self.updatePath(level, playerPosition)
        if level == 1 and len(self.path) == 0 and not self.killed :
            availableDirections = [1, -1, 2, -2]
            availableDirections.remove(-self.direction)
            nextDirection = self.direction
            for corner in corners:
                if self.col == corner[0] and self.row == corner[1]:
                    nextDirection = availableDirections[random.randint(0, 2)]
                    while self.facingWall(nextDirection):
                        nextDirection = availableDirections[random.randint(0, 2)]
            self.direction = nextDirection
            if self.direction == 1 and not self.tile[self.row - 1][self.col].isWall: # left
                self.worldYPosition = self.tile[self.row - 1][self.col].row
                self.row -= 1
            elif self.direction == -1 and not self.tile[self.row + 1][self.col].isWall: # right
                self.worldYPosition = self.tile[self.row + 1][self.col].row
                self.row += 1
            elif self.direction == 2 and not self.tile[self.row][self.col - 1].isWall: #up
                self.worldXPosition = self.tile[self.row][self.col - 1].col
                self.col -= 1
            elif self.direction == -2 and not self.tile[self.row][self.col + 1].isWall: #down
                self.worldXPosition = self.tile[self.row][self.col + 1].col
                self.col += 1
        else:
            if len(self.path) == 1 and level == 1 and not self.killed:
                self.path = []
            elif level == 1 and not self.killed:
                self.path.pop(0)

            if len(self.path) > 1:
                self.worldXPosition = self.tile[self.path[1][0]][self.path[1][1]].col
                self.worldYPosition = self.tile[self.path[1][0]][self.path[1][1]].row

                self.col = self.path[1][1]
                self.row = self.path[1][0]
            
    def isInsideCage(self):
        return self.row >= 12 and self.row <= 16 and self.col >= 10 and self.col <= 17
            
    def getNearestCorner(self, playerPosition):
        global tilesRepresentation, mapDirections
        destination = None
        shouldRun = True
        currentPosition = playerPosition.copy()
        while shouldRun:
            if tilesRepresentation[currentPosition[0]][currentPosition[1]] == 'W':
                break
            currentPosition[0] = currentPosition[0] + mapDirections[self.trait][1]
            currentPosition[1] = currentPosition[1] + mapDirections[self.trait][0]
            for corner in corners:
                if currentPosition[1] == corner[0] and currentPosition[0] == corner[1]:
                    destination = currentPosition
                    shouldRun = False
                    break;
            
        return destination

    def isBetweenCornerAndPlayer(self, corner, playerPosition):
        if self.trait == "chaseUp" and self.row >= corner[0] and self.row <= playerPosition[0] and self.col == corner[1] and self.col == playerPosition[1]\
        or self.trait == "chaseDown" and self.row <= corner[0] and self.row >= playerPosition[0] and self.col == corner[1] and self.col == playerPosition[1]\
        or self.trait == "chaseLeft" and self.col >= corner[1] and self.col <= playerPosition[1] and self.row == corner[0] and self.row == playerPosition[0]\
        or self.trait == "chaseRight" and self.col <= corner[1] and self.col >= playerPosition[1] and self.row == corner[0] and self.row == playerPosition[0]:
            return True
        return False

    def updatePath(self,level,playerPosition):
        global corners

        if self.killed :
            self.path = algorithms.bfs((self.row,self.col),(15,11))
        elif level == 2:
            if (len(self.path) == 0):
                self.path = algorithms.dfs((self.row,self.col),playerPosition)
            else:
                self.path.pop(0)
        elif level == 3:
            self.path = algorithms.bfs((self.row,self.col),playerPosition)
        elif level == 4:
            nearestCorner = self.getNearestCorner(playerPosition)
            if nearestCorner is None or self.isBetweenCornerAndPlayer(nearestCorner, playerPosition):
                self.path = algorithms.aStar(tilesRepresentation,(self.row,self.col),playerPosition)
            else:
                self.path = algorithms.aStar(tilesRepresentation,(self.row,self.col),nearestCorner)
            
                
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.worldXPosition, self.worldYPosition), 7)

class PacMan:
    def __init__(self, tile):
        self.tiles = tile
        self.col = 13
        self.row = 23
        self.worldXPosition = self.tiles[self.row][self.col].col
        self.worldYPosition = self.tiles[self.row][self.col].row
        self.direction = 0
        self.nextDirection = None

        # Close the gate
        self.tiles[12][13].isWall = True
        self.tiles[12][14].isWall = True

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), (self.worldXPosition,self.worldYPosition), 7)

    def setPosition(self , col , row):
        self.col = col
        self.row = row
        self.worldXPosition = self.tiles[self.row][self.col].col
        self.worldYPosition = self.tiles[self.row][self.col].row

    def update(self, keys):
        if keys[pygame.K_UP]:
            if not self.tiles[self.row - 1][self.col].isWall:
                self.direction = 1
                self.nextDirection = None
            elif self.direction != self.nextDirection:
                self.nextDirection = 1
        if keys[pygame.K_DOWN]:
            if not self.tiles[self.row+1][self.col].isWall:
                self.direction = 2
                self.nextDirection = None
            elif self.direction != self.nextDirection:
                self.nextDirection = 2

        if keys[pygame.K_LEFT]:
            if not self.tiles[self.row][self.col-1].isWall:
                self.direction = 3
                self.nextDirection = None
            elif self.direction != self.nextDirection:
                self.nextDirection = 3

        if keys[pygame.K_RIGHT]:
            if not self.tiles[self.row][self.col+1].isWall:
                self.direction = 4
                self.nextDirection = None
            elif self.direction != self.nextDirection:
                self.nextDirection = 4

    def updateDirection(self):
        if ((self.nextDirection == 1 and not self.tiles[self.row-1][self.col].isWall) or\
            (self.nextDirection == 2 and not self.tiles[self.row+1][self.col].isWall) or\
            (self.nextDirection == 3 and not self.tiles[self.row][self.col-1].isWall) or\
            (self.nextDirection == 4 and not self.tiles[self.row][self.col+1].isWall)):
                self.direction = self.nextDirection
                self.nextDirection = None


    def move(self):
        self.updateDirection()
        if self.direction == 1 and not self.tiles[self.row-1][self.col].isWall:
            self.worldYPosition = self.tiles[self.row-1][self.col].row
            self.row -= 1

        if self.direction == 2 and not self.tiles[self.row+1][self.col].isWall :
            self.worldYPosition = self.tiles[self.row+1][self.col].row
            self.row += 1

        if self.direction == 3 and not self.tiles[self.row][self.col-1].isWall :
            self.worldXPosition = self.tiles[self.row][self.col-1].col
            self.col -= 1

        if self.direction == 4 and not self.tiles[self.row][self.col+1].isWall :
            self.worldXPosition = self.tiles[self.row][self.col+1].col
            self.col += 1

class Tile:
    def __init__(self, col, row):
        self.row = row
        self.col = col
        self.isCoin = False
        self.isWall = False
        self.isFrightenedCoin = False
        self.isEmptySpace = False

    def draw(self, surface):
        if self.isCoin:
            pygame.draw.circle(surface, (255, 255, 0), (self.col, self.row), 1)

        elif self.isFrightenedCoin:
            pygame.draw.circle(surface, (255, 0, 0), (self.col, self.row), 5)

class App:
    def __init__(self):
        # State
        self.screen = pygame.display.set_mode((Width, Height))
        pygame.display.set_caption('Pac-Man')
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "settings"
        self.tiles = []

        self.score = 0
        self.level = 1
        self.lives = 3
        self.timer = 0
        self.font = pygame.font.SysFont('Arial', 20)
        self.readyFont = pygame.font.SysFont('Comic Sans MS', 50)

        for i in range(31):
            self.tiles.append([Tile(0, 0) for c in range(0, 28)])

        self.background = pygame.image.load("map.jpg")

        self.showPath = False
        self.showCorners = False
        self.showGrid = False

        # initialize tiles
        for col in range(28):
            for row in range(31):
                self.tiles[row][col] = Tile(16 * col + 8, 16 * row + 8)
                if tilesRepresentation[row][col] == 'W':
                    self.tiles[row][col].isWall = True

                elif tilesRepresentation[row][col] == 'F':
                    self.tiles[row][col].isFrightenedCoin = True

                elif tilesRepresentation[row][col] == 'C':
                    self.tiles[row][col].isCoin = True

                elif tilesRepresentation[row][col] == 'E':
                    self.tiles[row][col].isEmptySpace = True
        
        self.player = PacMan(self.tiles)
        self.monsters = [
            Monster(self.tiles, 11, 15, "chaseUp",       (255, 105, 180), 5),
            Monster(self.tiles, 13, 15, "chaseDown",    (52, 235, 235), 10),
            Monster(self.tiles, 14, 15, "chaseLeft",   (255, 0, 0), 15),
            Monster(self.tiles, 16, 15, "chaseRight",   (235, 152, 52), 20),
        ]


    def run(self):
        while self.running:
            self.events()
            if self.state == 'playing' or self.state == "ready" or self.state == "settings":
                self.draw()
            else:
                self.running = False
            self.clock.tick(10)

        pygame.quit()

    def draw (self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.background, (0, 0))

        # Show Corners
        if self.showCorners :
            for corner in corners:
                pygame.draw.circle(self.screen, (0, 0, 150), (self.tiles[corner[1]][corner[0]].col , self.tiles[corner[1]][corner[0]].row), 10)

        # Show Grid
        if self.showGrid :
            for y in range(0, 496, 16):
                pygame.draw.line(self.screen, (180, 160, 140), (0, y), (448, y))
            for x in range(0, 448, 16):
                pygame.draw.line(self.screen, (180, 160, 140), (x, 0), (x, 496))

        if (self.state == "ready"):
            self.screen.blit( self.readyFont.render("Press Any Key", False, (255, 255, 0)), ((Width/2)-150,Height/2))

        self.screen.blit( self.font.render('Score: ' + str(self.score), False, (255, 255, 255)), (10,Height-25))
        self.screen.blit( self.font.render('Level: ' + str(self.level), False, (255, 255, 255)), (Width-65,Height-25))
        for i in range(self.lives):
            pygame.draw.circle(self.screen, (255, 255, 0), (200+(i*20),Height-12), 7)

        for col in range(28):
            for row in range(31):
                self.tiles[row][col].draw(self.screen)
        
        for element in self.monsters + [self.player] :
            if self.showPath and element != self.player:
                element.highlightPath(self.screen)
            element.draw(self.screen)
        if self.state == "settings":
            font = pygame.font.SysFont('Arial', 30)
            self.screen.blit(self.font.render("Do you want to highlight ghosts paths?", True, (255, 255, 0)), ((Width / 2) - 150, Height / 2))
            pygame.draw.rect(self.screen, (0, 255, 0), ((Width // 2) - 145, (Height // 2) + 55, 100, 50))
            pygame.draw.rect(self.screen, (255, 0, 0), ((Width // 2) + 35, (Height // 2) + 55, 100, 50))
            self.screen.blit(font.render("Yes", True, (0, 0, 0)), ((Width // 2) - 115, (Height // 2) + 60))
            self.screen.blit(font.render("No", True, (0, 0, 0)), ((Width // 2) + 70, (Height // 2) + 60))

        pygame.display.update()

    def isLevelFinished(self):
        return (self.score / 242)  == self.level

    def resetGame (self,resetTiles = True):
        # Reset state
        self.state = "ready"

        #Reset tiles
        if resetTiles :
            for col in range(28):
                for row in range(31):
                    if tilesRepresentation[row][col] == 'F':
                        self.tiles[row][col].isFrightenedCoin = True

                    elif tilesRepresentation[row][col] == 'C':
                        self.tiles[row][col].isCoin = True

                    elif tilesRepresentation[row][col] == 'E':
                        self.tiles[row][col].isEmptySpace = True

        # Reset Player
        self.player = PacMan(self.tiles)

        # Reset Monsters
        self.monsters = [
            Monster(self.tiles, 11, 15, "chaseUp",       (255, 105, 180), 5),
            Monster(self.tiles, 13, 15, "chaseDown",    (52, 235, 235), 10),
            Monster(self.tiles, 14, 15, "chaseLeft",   (255, 0, 0), 15),
            Monster(self.tiles, 16, 15, "chaseRight",   (235, 152, 52), 20),
        ]

    def inCollision (self,monster):
        # Collision occurred between player and monster
        if monster.col == self.player.col and monster.row == self.player.row :
            # in Frightened state
            if self.timer != 0 and monster.isFrightened:
                monster.killed = True
            else:
                self.resetGame(False)
                self.lives -= 1
                # Game over
                if self.lives == 0:
                    self.resetGame()
                    self.lives = 3
                    self.level = 1
                    self.score = 0

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP and self.state == "settings":
                pos = pygame.mouse.get_pos()
                if pos[0] >= (Width // 2) - 150 and pos[0] <= (Width // 2) - 50 and pos[1] >=(Height // 2) + 50 and pos[1] <= (Height // 2) + 100:
                    self.showPath = True
                    self.state = "ready"
                elif pos[0] >= (Width // 2) + 30 and pos[0] <= (Width // 2) + 130 and pos[1] >=(Height // 2) + 50 and pos[1] <= (Height // 2) + 100:
                    self.showPath = False
                    self.state = "ready"

            self.player.update(pygame.key.get_pressed())
            if self.player.direction != 0 and self.state == "ready":
               self.state = "playing"

        if self.state == "playing":
            
            self.player.move()

            for i in range(len(self.monsters)):
                self.inCollision(self.monsters[i])

                if self.monsters[i].timer != 0:
                    self.monsters[i].timer -= 1
                elif not self.monsters[i].isFrightened:
                    self.monsters[i].move(self.level, [self.player.row,self.player.col])
                else:
                    self.monsters[i].path.clear()
                    self.monsters[i].move(1) 

                self.inCollision(self.monsters[i])

                

            
            # Teleport
            for element in self.monsters + [self.player]:
                if element.col == 1 and element.row == 14 :
                    element.setPosition(26,14)
                elif element.col == 26 and element.row == 14:
                    element.setPosition(1,14)

            # Refresh Tiles

            # Coin
            if self.tiles[self.player.row][self.player.col].isCoin:
                self.tiles[self.player.row][self.player.col].isCoin = False
                self.tiles[self.player.row][self.player.col].isEmptySpace = True
                self.score += 1

            # FrightenedCoin
            if self.tiles[self.player.row][self.player.col].isFrightenedCoin :
                self.tiles[self.player.row][self.player.col].isFrightenedCoin = False
                self.tiles[self.player.row][self.player.col].isEmptySpace = True
                self.timer = 50
                for monster in self.monsters:
                    if not monster.isInsideCage() and not monster.killed:
                        monster.isFrightened = True
                        monster.color = (50, 50, 255)
                        monster.setDirectionBasedOnPath()
            if self.timer != 0:
                self.timer -= 1
                if self.timer == 0:
                    for i in range(len(self.monsters)):
                        self.monsters[i].isFrightened = False
                        self.monsters[i].resetColor()
            # Check if level is finished
            if self.isLevelFinished(): 
                if self.level != 4:
                    self.level += 1
            
                self.resetGame()

game = App()
game.run()