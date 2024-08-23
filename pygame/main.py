import pygame as pg
import csv
import os
import sys
from settings import *
from assets import *
from map import *

#Test

class game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((screen_x, screen_y))

        self.fullscreen = False
        self.clock = pg.time.Clock()
        self.running = True

        self.max_health = 200
        self.player_position_x = 0
        self.player_position_y = 0
        self.last_position_x = [0, 0, 0, 0, 0, 0]
        self.last_position_y = [0, 0, 0, 0, 0, 0]

        self.font = pg.font.Font('Arial.ttf', 32)

        self.combat_state = False
        self.dialoge_state = True

        self.current_map = 0

        self.spritesheet = Spritesheet('spritesheet.png')

    def create_tilemap(self, map):
        y = 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0':
                    Grass(self, x , y)
                if tile == '1':
                    Dirt(self, x, y)
                if tile == '2':
                    Brick(self, x, y)
                if tile == '3':
                    Brick_Wall(self, x, y)
                if tile == '4':
                    Buch(self, x, y)
                if tile == '5':
                    Door(self, x, y)
                if tile == '6':
                    Door_Back(self, x, y)
                if tile == '7':
                    House_Wall(self, x, y)
                if tile == '8':
                    House_door(self, x, y)
                if tile == '9':
                    Carpet(self, x, y)
                if tile == '10':
                    House_Door_Back(self, x, y)
                if tile == '11':
                    House(self, x, y)

                x += 1
            y += 1

    def spawn_npc(self, map):
        y = 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '1':
                    Villager(self, x, y)
                if tile == '2':
                    Goblin(self, x, y)

                x += 1
            y += 1

    def new(self):
        self.playing = True

        self.health = self.max_health
        
        self.inventory = []

        first_map = 0
        self.current_map = first_map

        self.all_sprites = pg.sprite.LayeredUpdates()
        self.ground_sprites = pg.sprite.LayeredUpdates()
        self.blocks = pg.sprite.LayeredUpdates()
        self.player_sprites = pg.sprite.LayeredUpdates()
        self.enemy_sprites = pg.sprite.LayeredUpdates()
        self.door_sprites = pg.sprite.LayeredUpdates()
        self.ui_sprites = pg.sprite.LayeredUpdates()

        self.create_tilemap(maps_list[first_map])
        Player(self, player_next_spawns_x[first_map], player_next_spawns_y[first_map])
        #self.create_tilemap(map4_list)
        #print("creating tile map")
            
    def events(self):

        self.mouse_pressed = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F11 and self.fullscreen == False:
                    self.fullscreen = True
                    self.screen = pg.display.set_mode((256, 160), pg.SCALED | pg.FULLSCREEN)
                elif event.key == pg.K_F11 and self.fullscreen == True:
                    self.fullscreen = False
                    self.screen = pg.display.set_mode((256, 160)) 
                elif event.key == pg.K_ESCAPE and self.combat_state == True:
                    self.combat_state = False
                

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_pressed = True

        self.mouse_pos = pg.mouse.get_pos()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(TPS)
        pg.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
            print(self.player_position_x, self.player_position_y)
            print(self.last_position_x, self.last_position_y)
            print(self.current_map)

    def intro_screen(self):
        intro = True

        title = self.font.render('Game', False, BLUE)
        title_rect = title.get_rect(x=10, y=10)

        play_button = Button(10, 50, 100, 50, BLUE, BLACK, 'Play', 32)

        while intro and self.running:
            self.events()

            if play_button.is_pressed(self.mouse_pos, self.mouse_pressed):
                intro = False
                self.playing = True
                self.health = self.max_health
                self.new()

            self.screen.fill(BLACK)
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(TPS)
            pg.display.update()

    def game_over_screen(self):
        intro = True

        title = self.font.render('Game over', True, BLUE)
        title_rect = title.get_rect(x=10, y=10)

        play_button = Button(10, 50, 100, 50, BLUE, BLACK, 'Restart', 32)

        while intro and self.running:
            self.events()

            if play_button.is_pressed(self.mouse_pos, self.mouse_pressed):
                intro = False
                self.playing = True
                self.health = self.max_health
                self.new()

            self.screen.fill(BLACK)
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(TPS)
            pg.display.update()

    def player_die(self):
        dead = True
        self.playing = False

        while self.running and not self.playing:
            self.game_over_screen()
            dead = False

    def next_map(self):

        self.last_position_x[self.current_map] = int(self.player_position_x)
        self.last_position_y[self.current_map] = int(self.player_position_y)
    
        self.current_map += 1
        
        self.create_tilemap(maps_list[self.current_map])
        self.spawn_npc(maps_spawn_list[self.current_map])
        Player(self, player_next_spawns_x[self.current_map], player_next_spawns_y[self.current_map])

        self.player_position_x = 0
        self.player_position_y = 0

    def previus_map(self):
        self.current_map -= 1
        
        #self.player_position_x = self.last_position_x[self.current_map]
        #self.player_position_y = self.last_position_y[self.current_map]

        self.create_tilemap(maps_list[self.current_map])
        self.spawn_npc(maps_spawn_list[self.current_map])
        #Player(self, player_next_spawns_x[self.current_map], player_next_spawns_y[self.current_map])
        Player(self, self.last_position_x[self.current_map] + player_next_spawns_x[self.current_map], self.last_position_y[self.current_map] + player_next_spawns_y[self.current_map] + 16)
        

        
    def house_map(self):
        self.last_position_x[self.current_map] = int(self.player_position_x)
        self.last_position_y[self.current_map] = int(self.player_position_y)
        
        self.create_tilemap(house_list)
        self.spawn_npc(house_spawn_list)
        Player(self, 48, 64)

        self.player_position_x = 0
        self.player_position_y = 0
        
    def house_map_back(self):
        #self.player_position_x = self.last_position_x[self.current_map]
        #self.player_position_y = self.last_position_y[self.current_map]

        self.create_tilemap(maps_list[self.current_map])
        self.spawn_npc(maps_spawn_list[self.current_map])
        #Player(self, player_next_spawns_x[self.current_map], player_next_spawns_y[self.current_map])
        Player(self, self.last_position_x[self.current_map] + player_next_spawns_x[self.current_map], self.last_position_y[self.current_map] + player_next_spawns_y[self.current_map] + 16)
        
        
    def dialoge(self, sprite):
        self.dialoge_state = True
        
        current_dialoge = 0

        dialoge_box = Dialoge_box(self, 0, 128)
        dialoge_text = Text(16, 128, 240, 16, BLUE, RED, str(sprite.dialoge_list[current_dialoge]), 12)

        next_dialoge = UI_button(self, 240, 144, TILESIZE, TILESIZE, BLACK, '>', 32)
        previus_dialoge = UI_button(self, 0, 144, TILESIZE, TILESIZE, BLACK, '<', 32)

        while self.dialoge_state and self.running:
            self.events()
            self.screen.blit(dialoge_box.image, dialoge_box.rect)
            self.screen.blit(dialoge_text.image, dialoge_text.rect)
            self.screen.blit(previus_dialoge.image, previus_dialoge.rect)
            self.screen.blit(next_dialoge.image, next_dialoge)
            pg.display.update()
            #print('working')

            if next_dialoge.is_pressed(self.mouse_pos, self.mouse_pressed):
                #print('prssed')
                current_dialoge += 1
                try:
                    dialoge_text = Text(16, 128, 240, 16, BLUE, RED, str(sprite.dialoge_list[current_dialoge]), 12)
                except IndexError:
                    self.dialoge_state = False
                    dialoge_box.kill()
                    previus_dialoge.kill()
                    next_dialoge.kill()

    def combat(self, sprite):

        attack_button = Button(10, 50, 100, 50, BLUE, BLACK, 'Attack', 32)

        health = Text(0, 0, 32, 16, BLUE, RED, str(self.health), 16)
        enemy_health = Text(144, 0, 32, 16, BLUE, RED, str(sprite.health), 16)

        while self.combat_state and self.running:
            self.events()
            self.screen.fill(BLACK)
            self.screen.blit(sprite.big_image, sprite.big_image_position)
            self.screen.blit(attack_button.image, attack_button.rect)
            self.screen.blit(enemy_health.image, enemy_health.rect)
            self.screen.blit(health.image, health.rect)
            pg.display.update()

            if attack_button.is_pressed(self.mouse_pos, self.mouse_pressed):
                self.damage = random.uniform(40, 50)
                self.damage = int(self.damage)
                sprite.health -= self.damage

                sprite.attack()

                health = Text(0, 0, 32, 16, BLUE, RED, str(self.health), 16)
                enemy_health = Text(144, 0, 32, 16, BLUE, RED, str(sprite.health), 16)

            if sprite.health <= 0.0:
                sprite.die()
            if self.health <= 0:
                self.combat_state = False
                self.playing = False
                self.player_die()

g = game()
g.intro_screen()
while g.running:
    g.main()
    
pg.quit()
sys.exit()