import pygame as pg
import math
import random
from dialoge import *
from settings import *

width = 16
height = 16

class Spritesheet:
    def __init__(self, file):
        self.sheet = pg.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pg.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(RED)
        return sprite

class Sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite().__init__()
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.spritesheet.get_sprite(0, 0, self.width, self.height)
 
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Entity(Sprite):
    def __init__(self, game, x, y):
        Sprite.__init__(self, game, x, y)

        self.change_x = 0
        self.change_y = 0
        
        self.facing = 'down'
        self.animation_loop = 1        

class Item(Sprite):
    def __init__(self, game, x, y):
        Sprite.__init__(self, game, x, y)

        self.name = 'name'

    def collide_player(self):
        hits = pg.sprite.spritecollide(self, self.game.player_sprites, False)
        if hits:
            self.game.inventory.append(self.name)
            self.kill()

class Player(Entity): 
    def __init__(self, game, x, y):
        Entity.__init__(self, game, x, y)
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.player_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.spritesheet.get_sprite(0, 64, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animation = [self.game.spritesheet.get_sprite(0, 64, self.width, self.height),
                        self.game.spritesheet.get_sprite(16, 64, self.width, self.height),
                        self.game.spritesheet.get_sprite(32, 64, self.width, self.height)]

        self.right_animation = [self.game.spritesheet.get_sprite(0, 80, self.width, self.height),
                        self.game.spritesheet.get_sprite(16, 80, self.width, self.height),
                        self.game.spritesheet.get_sprite(32, 80, self.width, self.height)]

        self.left_animation = [self.game.spritesheet.get_sprite(0, 96, self.width, self.height),
                        self.game.spritesheet.get_sprite(16, 96, self.width, self.height),
                        self.game.spritesheet.get_sprite(32, 96, self.width, self.height)]

        self.up_animation = [self.game.spritesheet.get_sprite(0, 112, self.width, self.height),
                        self.game.spritesheet.get_sprite(16, 112, self.width, self.height),
                                self.game.spritesheet.get_sprite(32, 112, self.width, self.height)]

    def update(self):
        self.movment()
        self.animate()

        self.rect.x += self.change_x
        self.collide_blocks('x')
        self.rect.y += self.change_y
        self.collide_blocks('y')

        self.change_x = 0
        self.change_y = 0

        if self.rect.x < screen_x/2 - TILESIZE/2:
            #self.game.player_position_x += screen_x/2 - self.rect.x
            for sprite in self.game.all_sprites:
                sprite.rect.x += screen_x/2 - self.rect.x

        if self.rect.x > screen_x/2 - TILESIZE/2:
            #self.game.player_position_x -= screen_x/2 - self.rect.x
            for sprite in self.game.all_sprites:
                sprite.rect.x -= self.rect.x - screen_x/2 + TILESIZE/2

        if self.rect.y < screen_y/2 - TILESIZE/2:
            #self.game.player_position_y += screen_x/2 - self.rect.x
            for sprite in self.game.all_sprites:
                sprite.rect.y += screen_y/2 - self.rect.y

        if self.rect.y > screen_y/2 - TILESIZE/2:
            #self.game.player_position_y -= screen_x/2 - self.rect.x
            for sprite in self.game.all_sprites:
                sprite.rect.y -= self.rect.y - screen_y/2 + TILESIZE/2
                
    def movment(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.change_x -= PLAYER_SPEED
            self.game.player_position_x -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pg.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.change_x += PLAYER_SPEED
            self.game.player_position_x += PLAYER_SPEED
            self.facing = 'right'
        if keys[pg.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.change_y -= PLAYER_SPEED
            self.game.player_position_y -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pg.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.change_y += PLAYER_SPEED
            self.game.player_position_y += PLAYER_SPEED
            self.facing = 'down'

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pg.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.change_x > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    self.game.player_position_x -= PLAYER_SPEED
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.change_x < 0:
                    self.game.player_position_x += PLAYER_SPEED
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
        if direction == 'y':
            hits = pg.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.change_y > 0:
                    self.rect.y = hits[0].rect.top - self.rect. height
                    self.game.player_position_y -= PLAYER_SPEED
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.change_y < 0:
                    self.rect.y = hits[0].rect.bottom 
                    self.game.player_position_y += PLAYER_SPEED
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def animate(self):
        if self.facing == "down":
            if self.change_y == 0:
                self.image = self.game.spritesheet.get_sprite(0, 64, self.width, self.height)

            else:
                self.image = self.down_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.change_x == 0:
                self.image = self.game.spritesheet.get_sprite(0, 80, self.width, self.height)

            else:
                self.image = self.right_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.change_x == 0:
                self.image = self.game.spritesheet.get_sprite(0, 96, self.width, self.height)

            else:
                self.image = self.left_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.change_y == 0:
                self.image = self.game.spritesheet.get_sprite(0, 112, self.width, self.height)

            else:
                self.image = self.up_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Npc(Entity):
    def __init__(self, game, x, y):
        Entity.__init__(self, game, x, y)
        self._layer = NPC_LAYER
        self.facing = random.choice(['left', 'right', 'up', 'down'])
        self.max_travel = 64
        self.animation_loop = 0
        self.movement_loop = 0
        
    def update(self):
        
        self.movement()

        self.collide_blocks(self.facing)
        self.collide_player()
        self.animate()

        self.rect.x += self.change_x
        self.collide_blocks('x')
        self.rect.y += self.change_y
        self.collide_blocks('y')

        self.change_x = 0
        self.change_y = 0

    def movement(self):

        if self.facing == 'left':
            self.change_x -= NPC_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'
            
        if self.facing == 'right':
            self.change_x += NPC_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

        if self.facing == 'up':
            self.change_y -= NPC_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'down'
            
        if self.facing == 'down':
            self.change_y += NPC_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'up'

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pg.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.change_x > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.change_x < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pg.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.change_y > 0:
                    self.rect.y = hits[0].rect.top - self.rect. height
                if self.change_y < 0:
                    self.rect.y = hits[0].rect.bottom 
            
    def animate(self):
        if self.facing == "left":
            if self.change_x == 0:
                self.image = self.game.spritesheet.get_sprite(32, 80, self.width, self.height)

            else:
                self.image = self.left_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == "right":
            if self.change_x == 0:
                self.image = self.game.spritesheet.get_sprite(32, 80, self.width, self.height)

            else:
                self.image = self.right_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == "up":
            if self.change_y == 0:
                self.image = self.game.spritesheet.get_sprite(32, 112, self.width, self.height)

            else:
                self.image = self.up_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

        if self.facing == "down":
            if self.change_y == 0:
                self.image = self.game.spritesheet.get_sprite(32, 112, self.width, self.height)

            else:
                self.image = self.down_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 2:
                    self.animation_loop = 0

class Door(Sprite):
    def __init__(self, game, x, y):
        Sprite.__init__(self, game, x, y)
        self.game = game
        self._layer = GROUND_LAYER
        #.groups = self.game.all_sprites, self.game.door_sprites
        #pg.sprite.Sprite.__init__(self, self.groups)
    
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE + TILESIZE/2

    def collide_doors(self):
            hits = pg.sprite.spritecollide(self, self.game.player_sprites, True)
            if hits:
                for sprite in self.game.all_sprites:
                    sprite.kill()
                
                self.game.next_map()
                self.kill()

class Door_Back(Sprite):
    pass

class Villager(Npc):
    def __init__(self, game, x, y):
        Npc.__init__(self, game, x, y)
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.npc_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.big_width = 96
        self.big_height = 128

        self.image = self.game.spritesheet.get_sprite(32, 64, self.width, self.height)
        
        self.handled = False
        self.dialoge_list = [villager_dialoge_1, villager_dialoge_2, villager_dialoge_3, villager_dialoge_4, villager_dialoge_5, villager_dialoge_6]

        self.down_animation = [self.game.spritesheet.get_sprite(0, 128, self.width, self.height),
                        self.game.spritesheet.get_sprite(16, 128, self.width, self.height),
                        self.game.spritesheet.get_sprite(32, 128, self.width, self.height)]

        self.right_animation = [self.game.spritesheet.get_sprite(0, 144, self.width, self.height),
                        self.game.spritesheet.get_sprite(16, 144, self.width, self.height),
                        self.game.spritesheet.get_sprite(32, 144, self.width, self.height)]

        self.left_animation = [self.game.spritesheet.get_sprite(0, 160, self.width, self.height),
                        self.game.spritesheet.get_sprite(16, 160, self.width, self.height),
                        self.game.spritesheet.get_sprite(32, 160, self.width, self.height)]

        self.up_animation = [self.game.spritesheet.get_sprite(0, 176, self.width, self.height),
                        self.game.spritesheet.get_sprite(16, 176, self.width, self.height),
                        self.game.spritesheet.get_sprite(32, 176, self.width, self.height)]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        
        self.movement()

        self.collide_blocks(self.facing)
        self.collide_player()
        self.animate()

        self.rect.x += self.change_x
        self.collide_blocks('x')
        self.rect.y += self.change_y
        self.collide_blocks('y')

        self.change_x = 0
        self.change_y = 0


    def collide_player(self):
        hits = pg.sprite.spritecollide(self, self.game.player_sprites, False)
        if hits and not self.handled:
            self.game.dialoge(self)
            self.handled = True
        elif not hits:
            self.handled = False

class Village_elder(pg.sprite.Sprite):
    pass

class Goblin(Npc):
    def __init__(self, game, x, y):
        Npc.__init__(self, game, x ,y)
        self.game = game
        self.groups = self.game.all_sprites, self.game.npc_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.big_width = 96
        self.big_height = 128

        self.change_x = 0
        self.change_y = 0
        
        self.facing = random.choice(['left', 'right', 'up', 'down'])
        self.max_travel = random.randint(16, 64)
        self.animation_loop = 0
        self.movement_loop = 0

        self.strength = random.uniform(0.5, 1.5)
        self.health = int(100 * self.strength)

        if self.strength < 1:
            self.big_image = self.game.spritesheet.get_sprite(96, 64, self.big_width, self.big_height)
        elif self.strength >= 1:
            self.big_image = self.game.spritesheet.get_sprite(192,64, self.big_width, self.big_height)

        self.big_image_position = (144, 8)

        self.image = self.game.spritesheet.get_sprite(32, 64, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animation = [self.game.spritesheet.get_sprite(48, 64, self.width, self.height),
                        self.game.spritesheet.get_sprite(64, 64, self.width, self.height),
                        self.game.spritesheet.get_sprite(80, 64, self.width, self.height)]

        self.right_animation = [self.game.spritesheet.get_sprite(48, 80, self.width, self.height),
                        self.game.spritesheet.get_sprite(64, 80, self.width, self.height),
                        self.game.spritesheet.get_sprite(80, 80, self.width, self.height)]

        self.left_animation = [self.game.spritesheet.get_sprite(48, 96, self.width, self.height),
                        self.game.spritesheet.get_sprite(64, 96, self.width, self.height),
                        self.game.spritesheet.get_sprite(80, 96, self.width, self.height)]

        self.up_animation = [self.game.spritesheet.get_sprite(48, 112, self.width, self.height),
                        self.game.spritesheet.get_sprite(64, 112, self.width, self.height),
                        self.game.spritesheet.get_sprite(80, 112, self.width, self.height)]

    def update(self):
        
        self.movement()
        self.collide_blocks(self.facing)
        self.collide_player()
        self.animate()
        self.die()

        self.rect.x += self.change_x
        self.collide_blocks('x')
        self.rect.y += self.change_y
        self.collide_blocks('y')

        self.change_x = 0
        self.change_y = 0

    def collide_player(self):
        hits = pg.sprite.spritecollide(self, self.game.player_sprites, False)
        if hits and not self.game.combat_state:
            self.game.combat_state = True
            self.game.combat(self)

    def attack(self):
        self.damage = int(random.randint(10, 50))
        self.game.health -= int(self.damage * self.strength)

    def die(self):
        if self.health <= 0:
            self.game.combat_state = False
            self.kill()

class Health_potion(Item):
    def __init__(self, game, x, y):
        Item.__init__(self, game, x, y)
        self._layer = GROUND_LAYER
        self.groups = game.all_sprites, game.ground_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.name = 'Health_poton'
        self.image = self.game.spritesheet.get_sprite(0, 48, self.width, self.height)

    def update(self):
        self.collide_player()

class Grass(Sprite):
   def __init__(self, game, x, y):
        Sprite.__init__(self, game, x, y)
        self._layer = GROUND_LAYER
        self.groups = game.all_sprites, game.ground_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.spritesheet.get_sprite(0, 0, self.width, self.height)

class Grass_door(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.door_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE - TILESIZE/2
        self.width = TILESIZE
        self.height = TILESIZE + TILESIZE/2
        
        self.image = self.game.spritesheet.get_sprite(80, 16, self.width, self.height)
      
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.collide_doors()


    def collide_doors(self):
            hits = pg.sprite.spritecollide(self, self.game.player_sprites, True)
            if hits:
                for sprite in self.game.all_sprites:
                    sprite.kill()
                
                self.game.next_map()
                self.kill()

class Grass_door_back(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.door_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE - TILESIZE/2
        self.width = TILESIZE
        self.height = TILESIZE + TILESIZE/2
        
        self.image = self.game.spritesheet.get_sprite(80, 16, self.width, self.height)
      
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.collide_doors()

    def collide_doors(self):
            hits = pg.sprite.spritecollide(self, self.game.player_sprites, True)
            if hits:
                for sprite in self.game.all_sprites:
                    sprite.kill()
                self.game.previus_map()
                self.kill()

class Dirt(Sprite):
   def __init__(self, game, x, y):
        Sprite.__init__(self, game, x, y)
        self._layer = GROUND_LAYER
        self.groups = game.all_sprites, game.ground_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.spritesheet.get_sprite(16, 0, self.width, self.height)

class Brick(Sprite):
   def __init__(self, game, x, y):
        Sprite.__init__(self, game, x, y)
        self._layer = BLOCK_LAYER
        self.groups = game.all_sprites, game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.spritesheet.get_sprite(32, 0, self.width, self.height)

class Brick_Wall(Sprite):
       def __init__(self, game, x, y):
        Sprite.__init__(self, game, x, y)
        self._layer = BLOCK_LAYER
        self.groups = game.all_sprites, game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.spritesheet.get_sprite(48, 0, self.width, self.height)

class Rock_wall(Sprite):
    def __init__(self, game, x, y):
        Sprite.__init__(self, game, x, y)
        self._layer = BLOCK_LAYER
        self.groups = game.all_sprites, game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.spritesheet.get_sprite(32, 16, self.width, self.height)

class Rock_door(Door):
    def __init__(self, game, x, y):
        Door.__init__(self, game, x, y)
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.door_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.image = self.game.spritesheet.get_sprite(96, 16, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        self.collide_doors()

class Rock_door_back(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.door_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE - TILESIZE/2
        self.width = TILESIZE
        self.height = TILESIZE + TILESIZE/2
        
        self.image = self.game.spritesheet.get_sprite(96, 16, self.width, self.height)
      
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.collide_doors()

    def collide_doors(self):
            hits = pg.sprite.spritecollide(self, self.game.player_sprites, True)
            if hits:
                for sprite in self.game.all_sprites:
                    sprite.kill()
                self.game.previus_map()
                self.kill()

class Buch(pg.sprite.Sprite):
   def __init__(self, game, x, y):
        Sprite.__init__(self, game, x, y)
        self._layer = BLOCK_LAYER
        self.groups = game.all_sprites, game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.spritesheet.get_sprite(16, 16, self.width, self.height)

class Brick_door(Door):
    def __init__(self, game, x, y):
        Door.__init__(self, game, x, y)
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.door_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.spritesheet.get_sprite(0, 24, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.collide_doors()

class House(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = 48
        self.height = 64

        self.image = self.game.spritesheet.get_sprite(320, 16, self.width, self.height)
 
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Door_Back(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.door_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE - TILESIZE/2
        self.width = TILESIZE
        self.height = TILESIZE + TILESIZE/2
        
        self.image = self.game.spritesheet.get_sprite(0, 16, self.width, self.height)
      
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.collide_doors()

    def collide_doors(self):
            hits = pg.sprite.spritecollide(self, self.game.player_sprites, True)
            if hits:
                for sprite in self.game.all_sprites:
                    sprite.kill()
                self.game.previus_map()
                self.kill()

class House_Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.spritesheet.get_sprite(64, 0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Carpet(pg.sprite.Sprite):
   def __init__(self, game, x, y):
        Sprite.__init__(self, game, x, y)
        self._layer = GROUND_LAYER
        self.groups = game.all_sprites, game.ground_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.spritesheet.get_sprite(80, 0, self.width, self.height)

class House_door(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.door_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE  - TILESIZE/2
        self.width = TILESIZE
        self.height = TILESIZE + TILESIZE
        
        self.image = self.game.spritesheet.get_sprite(64, 16, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        self.collide_doors()


    def collide_doors(self):
            hits = pg.sprite.spritecollide(self, self.game.player_sprites, True)
            if hits:
                for sprite in self.game.all_sprites:
                    sprite.kill()
                self.game.house_map()
                self.kill()

class House_Door_Back(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.door_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE - TILESIZE/2
        self.width = TILESIZE
        self.height = TILESIZE + TILESIZE/2
        
        self.image = self.game.spritesheet.get_sprite(64, 16, self.width, self.height)
      
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.collide_doors()

    def collide_doors(self):
            hits = pg.sprite.spritecollide(self, self.game.player_sprites, True)
            if hits:
                for sprite in self.game.all_sprites:
                    sprite.kill()
                self.game.house_map_back()
                self.kill()

class Text:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pg.font.Font('Arial.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.fg = fg
        self.bg = bg

        self.image = pg.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.image.set_colorkey(RED)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, False, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pg.font.Font('Arial.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.fg = fg
        self.bg = bg

        self.image = pg.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, False, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)
        self.image.set_colorkey(RED)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed:
                return True
            else:
                 return False
        else:
            return False

class Dialoge_box(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.ui_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x
        self.y = y
        self.width = 256
        self.height = 32

        self.image = self.game.spritesheet.get_sprite(0, 192, self.width, self.height)
 
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class UI_button(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, fg, content, fontsize):
        super().__init__()
        self.font = pg.font.Font('Arial.ttf', fontsize)
        self.content = content

        self.game = game
        self._layer = UI_LAYER
        self.groups = self.game.all_sprites, self.game.ui_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.fg = fg

        self.image = self.game.spritesheet.get_sprite(0, 224, self.width, self.height)

        self.text = self.font.render(self.content, False, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed:
                return True
            else:
                return False
        else:
            return False