add_library('minim')
import os
import random
import time

PATH = os.getcwd()
RES_WIDTH = 1200
RES_HEIGHT = 600
hitbox_w = 75
hitbox_h = 145
GROUND = 560
#define number of slices
SCIENTIST_NUMBER_SLICES = [6, 8, 2, 2, 8, 1, 4, 7]
PHILOSOPHER_NUMBER_SLICES = [8, 8, 2, 2, 6, 1, 4, 6]
ARTIST_NUMBER_SLICES = [8, 8, 2, 2, 8, 1, 3, 7]
BUSINESS_NUMBER_SLICES = [10, 8, 3, 3, 7, 1, 3, 11]
ELECTRICAL_ENGINEER_NUMBER_SLICES = [10, 8, 3, 3, 7, 1, 3, 7]
THOMAS_POTSCH_NUMBER_SLICES = [11, 8, 4, 4, 6, 1, 4, 9]
FAISAL_ZEESHAN_NUMBER_SLICES = [6, 8, 2, 2, 6, 1, 4, 11]

back_image_numbers = ['1', '2', '3', '4', '5']

player = Minim(this) 

class Player(): # function of the player
    def __init__(self, x, y, control, img_w, img_h, num_slices, img_idle,
                                                                img_run,
                                                                img_jump,
                                                                img_fall,
                                                                img_attack,
                                                                img_block,
                                                                img_hit,
                                                                img_death, score = 0):
        self.g = GROUND
        self.res_w = RES_WIDTH
        self.res_h = RES_HEIGHT
        self.vx = 0
        self.vy = 1
        self.x = x
        self.y = y
        self.w = hitbox_w
        self.h = hitbox_h
        self.control = control
        self.slice = 0
        self.slice_hit = 0
        
        self.moving = False
        self.jump = False
        self.fall = False
        
        self.attack_x = 0
        self.attack_w = 0
        self.attack_check = False
        self.stun_check = False
        self.attack_time = 0
        self.attack_duration = 0.5
        self.stun_duration = 0.5
        self.health = 100
        self.alive = True
        self.death_animation_done = False
        
        self.attack_animation_done = False
        self.block_check = False
        self.jump_allowed_check = True
        
        self.score = score
        
        if self.control == 1:
            self.key_handler = {LEFT: False, RIGHT: False, UP:False, ',':False, '.':False}
            self.dir = LEFT
        elif control == 2:
            self.key_handler = {'a': False, 'd': False, 'w':False, '1':False, '2':False}
            self.dir = RIGHT
        
        self.img_w = img_w
        self.img_h = img_h
        self.num_slices = num_slices 
        self.img_idle = loadImage(PATH + img_idle)
        self.img_run = loadImage(PATH + img_run) 
        self.img_jump = loadImage(PATH + img_jump)
        self.img_fall = loadImage(PATH + img_fall)
        self.img_attack = loadImage(PATH + img_attack)
        self.img_block = loadImage(PATH + img_block)
        self.img_hit = loadImage(PATH + img_hit)
        self.img_death = loadImage(PATH + img_death)
        
        print(self.x, self.y)
    
    def gravity(self): # gravity while jumping
        if self.y + self.h >= self.g:
            self.vy = 0
        else:
            self.vy += 0.6   
            if self.y + self.h + self.vy > self.g:
                self.y = self.g - self.h
                self.vy = 0
                
    def update(self, other): # update
        if other.alive == False:
            self.y = self.g - self.h
            other.vx = 0
            other.vy = 0
            return
        
        self.gravity() 
        
        if self.health <= 0: # dies if no health
            self.health = 0
            self.alive = False

        self.moving = False
        self.jump = False
        self.fall = False
        
        if self.stun_check == True and time.time() - self.stun_start > self.stun_duration: # is stunned (stopped moving while being hit)
            self.stun_check = False
        
        if self.attack_check == False and self.block_check == False and self.stun_check == False: # can move while not being attacked, stunned and not blocking
            if self.control == 1:
                if self.key_handler[RIGHT] == True:
                    self.vx = 10
                    self.dir = RIGHT
                    self.moving = True
                elif self.key_handler[LEFT] == True:
                    self.vx = -10
                    self.dir = LEFT
                    self.moving = True
                else:
                    self.vx = 0
                
                if self.key_handler[UP] == True and self.y + self.h == self.g and self.jump_allowed_check != False:
                    self.slice = 0
                    self.vy = -15

                if self.key_handler[','] == True: 
                    self.slice = 0
                    self.attack(other)
                
                if self.key_handler['.'] == True:
                    self.slice = 0
                    self.block_check = True
                
            elif self.control == 2:
                if self.key_handler['d'] == True:
                    self.vx = 10
                    self.dir = RIGHT
                    self.moving = True
                elif self.key_handler['a'] == True:
                    self.vx = -10
                    self.dir = LEFT
                    self.moving = True
                else:
                    self.vx = 0
                    
                if self.key_handler['w'] == True and self.y + self.h == self.g and self.jump_allowed_check != False:
                    self.slice = 0
                    self.vy = -15
                    
                if self.key_handler['1'] == True:
                    self.slice = 0
                    self.attack(other)
                
                if self.key_handler['2'] == True:
                    self.slice = 0
                    self.block_check = True
         
        elif self.attack_check == True: # attack
            if self.y + self.h >= self.g:
                self.vx = 0
            if self.attack_check == True:
                if time.time() - self.attack_time > self.attack_duration:
                    self.attack_check = False
                    
        else:
            self.vx = 0
            
        self.tangibility(other) # stops overlapping each other
        
        if self.y + self.h <= other.y and self.x + self.w > other.x and self.x < other.x + other.w: # allows not overlapping from the above
            self.g = other.y
            other.jump_allowed_check = False
        else:
            self.g = GROUND
            other.jump_allowed_check = True
        
        if self.y + self.h == other.y: # slippes to sides if landed on top
            if (self.x + self.w)/2 < (other.x + other.w)/2:
                self.vx = -7
            else:
                self.vx = 7
        
        if self.stun_check == False: # allows stun
            self.x += self.vx
            self.x = max(0, min(self.res_w - self.w, self.x))
        elif other.dir == RIGHT: 
            self.x += 0.5
            self.x = max(0, min(self.res_w - self.w, self.x))
        elif other.dir == LEFT: 
            self.x += -0.5
            self.x = max(0, min(self.res_w - self.w, self.x))
        
        self.y += self.vy
        
        if self.vy < 0:
            self.jump = True
        
        elif self.vy > 0:
            self.fall = True
                
    def tangibility(self, other): # not overlapping
        if self.x < other.x + other.w and self.x + self.w > other.x:
            if self.y < other.y + other.h and self.y + self.h > other.y:
                if self.vx > 0 and self.x + self.w < other.x + other.w:
                    self.x = other.x - self.w
                if self.vx < 0 and self.x > other.x:
                    self.x = other.x + other.w
            
    def attack(self, other): # attack
        if self.y + self.h >= self.g:
            self.vx = 0
        self.attack_time = time.time()
        self.attack_check = True
        fill(0,230,0)
        
        if self.dir == RIGHT:
            self.attack_x = self.x + self.w/2
            self.attack_w = self.w * 2
        
        elif self.dir == LEFT:
            self.attack_x = self.x - (self.w*3)/2
            self.attack_w = self.w * 2

        fill(230, 0, 0)

        if self.attack_collision(other) == True and self.block(other) == False: # attack collision of hitboxes
            self.health -= 10
            other.stun_check = True
            other.stun_start = time.time()
            
            
    def attack_collision(self, other):
        if (self.attack_check == True) and (self.attack_x < other.x + other.w) and (self.attack_x + self.attack_w > other.x) and (self.y < other.y + other.h) and (self.y + self.h > other.y):
            return True
        else:
            return False
            
    def block(self, other): # provides block
        if other.block_check == True and ((self.dir == RIGHT and other.dir == LEFT and self.x < other.x) or (self.dir == LEFT and other.dir == RIGHT and self.x > other.x)):
            return True
        else:
            return False
    
    def display(self, other):
        if other.alive == False: 
            if self.death_animation_done == False:
                if self.dir == RIGHT:
                    image(self.img_death, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
                elif self.dir == LEFT:
                    image(self.img_death, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, (self.slice + 1) * self.img_w, 0, self.slice * self.img_w, self.img_h)
                if frameCount % 5 == 0:
                    self.slice += 1
                    if self.slice >= self.num_slices[7]:  
                        self.slice = self.num_slices[7] - 1  # Keep the frame at the last slice
                        self.death_animation_done = True
                        
            if self.death_animation_done == True:
                if self.dir == RIGHT:
                    image(self.img_death, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2,
                          self.img_w, self.img_h, (self.num_slices[7] - 1) * self.img_w, 0, self.num_slices[7] * self.img_w, self.img_h)
                
                elif self.dir == LEFT:
                    image(self.img_death, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2,
                          self.img_w, self.img_h, self.num_slices[7] * self.img_w, 0, (self.num_slices[7] - 1) * self.img_w, self.img_h)
                    self.gravity()
            return

        elif other.attack_collision(self) == True and self.block_check == False:

            if other.dir == self.dir:
                if other.dir == RIGHT:
                    self.dir = LEFT
                elif other.dir == LEFT:
                    self.dir = RIGHT

            if other.dir != self.dir:
                if self.dir == RIGHT:
                    image(self.img_hit, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
                elif self.dir == LEFT:
                    image(self.img_hit, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, (self.slice + 1) * self.img_w, 0, self.slice * self.img_w, self.img_h)
            if frameCount % 5 == 0:
                self.slice = (self.slice + 1) % self.num_slices[6]
                print(self.slice)

        elif self.block_check == True:
            if other.attack_collision(self) == True:
                if other.dir == self.dir:
                    if other.dir == RIGHT:
                        self.dir = LEFT
                    elif other.dir == LEFT:
                        self.dir = RIGHT
            if self.dir == RIGHT:
                image(self.img_block, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
            elif self.dir == LEFT:
                image(self.img_block, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, (self.slice + 1) * self.img_w, 0, self.slice * self.img_w, self.img_h)
            if frameCount % 5 == 0:
                self.slice = (self.slice + 1) % self.num_slices[5]

        elif self.attack_check == True:
            if self.dir == RIGHT:
                image(self.img_attack, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
            elif self.dir == LEFT:
                image(self.img_attack, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, (self.slice + 1) * self.img_w, 0, self.slice * self.img_w, self.img_h)
            if frameCount % 5 == 0:
                self.slice += 1
                if self.slice >= self.num_slices[4]:
                    self.slice = 0
                    self.attack_check = False
                
        elif self.jump == True:
             if self.dir == RIGHT:
                image(self.img_jump, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
             elif self.dir == LEFT:
                image(self.img_jump, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, (self.slice + 1) * self.img_w, 0, self.slice * self.img_w, self.img_h)
             if frameCount % 5 == 0:
                self.slice = (self.slice + 1) % self.num_slices[2]
                
        elif self.fall == True:
             if self.dir == RIGHT:
                image(self.img_fall, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
             elif self.dir == LEFT:
                image(self.img_fall, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, (self.slice + 1) * self.img_w, 0, self.slice * self.img_w, self.img_h)
             if frameCount % 5 == 0:
                self.slice = (self.slice + 1) % self.num_slices[3]
             
        elif self.moving == True:
            if self.dir == RIGHT:
                image(self.img_run, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
            elif self.dir == LEFT:
                image(self.img_run, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, (self.slice + 1) * self.img_w, 0, self.slice * self.img_w, self.img_h)
            if frameCount % 5 == 0:
                self.slice = (self.slice + 1) % self.num_slices[1]
            
        
        else:
            if self.dir == RIGHT:
                image(self.img_idle, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
            elif self.dir == LEFT:
                image(self.img_idle, self.x - (self.img_w - self.w) / 2, self.y - (self.img_h - self.h) / 2, self.img_w, self.img_h, (self.slice + 1) * self.img_w, 0, self.slice * self.img_w, self.img_h)
            if frameCount % 5 == 0:
                self.slice = (self.slice + 1) % self.num_slices[0]
                
class Scientist(Player): # classes of characters
    def __init__(self, x, y, control, score):
        Player.__init__(self, x, y, control, 406, 350, SCIENTIST_NUMBER_SLICES, 
                                                      "/scientist/scientist_idle.png", 
                                                      "/scientist/scientist_run.png",
                                                      "/scientist/scientist_jump.png",
                                                      "/scientist/scientist_fall.png",
                                                      "/scientist/scientist_attack.png",
                                                      "/scientist/scientist_block.png",
                                                      "/scientist/scientist_hit.png",
                                                      "/scientist/scientist_death.png", score)
        
class Philosopher(Player):
    def __init__(self, x, y, control, score):
        Player.__init__(self, x, y, control, 550, 525, PHILOSOPHER_NUMBER_SLICES, 
                                                      "/philosopher/philosopher_idle.png", 
                                                      "/philosopher/philosopher_run.png",
                                                      "/philosopher/philosopher_jump.png",
                                                      "/philosopher/philosopher_fall.png",
                                                      "/philosopher/philosopher_attack.png",
                                                      "/philosopher/philosopher_block.png",
                                                      "/philosopher/philosopher_hit.png",
                                                      "/philosopher/philosopher_death.png", score)
                                         
class Artist(Player):
    def __init__(self, x, y, control, score):
        Player.__init__(self, x, y, control, 550, 580, ARTIST_NUMBER_SLICES, 
                                                      "/artist/artist_idle.png", 
                                                      "/artist/artist_run.png",
                                                      "/artist/artist_jump.png",
                                                      "/artist/artist_fall.png",
                                                      "/artist/artist_attack.png",
                                                      "/artist/artist_block.png",
                                                      "/artist/artist_hit.png",
                                                      "/artist/artist_death.png", score)

class Business(Player):
    def __init__(self, x, y, control, score):
        Player.__init__(self, x, y, control, 350, 310, BUSINESS_NUMBER_SLICES, 
                                                      "/business/business_idle.png", 
                                                      "/business/business_run.png",
                                                      "/business/business_jump.png",
                                                      "/business/business_fall.png",
                                                      "/business/business_attack.png",
                                                      "/business/business_block.png",
                                                      "/business/business_hit.png",
                                                      "/business/business_death.png", score)

class ElectricalEngineer(Player):
    def __init__(self, x, y, control, score):
        Player.__init__(self, x, y, control, 500, 477, ELECTRICAL_ENGINEER_NUMBER_SLICES, 
                                                      "/electrical_engineer/electrical_engineer_idle.png", 
                                                      "/electrical_engineer/electrical_engineer_run.png",
                                                      "/electrical_engineer/electrical_engineer_jump.png",
                                                      "/electrical_engineer/electrical_engineer_fall.png",
                                                      "/electrical_engineer/electrical_engineer_attack.png",
                                                      "/electrical_engineer/electrical_engineer_block.png",
                                                      "/electrical_engineer/electrical_engineer_hit.png",
                                                      "/electrical_engineer/electrical_engineer_death.png", score)
        
class ThomasPotsch(Player):
    def __init__(self, x, y, control, score):
        Player.__init__(self, x, y, control, 490, 435, THOMAS_POTSCH_NUMBER_SLICES, 
                                                      "/thomas_potsch/thomas_potsch_idle.png", 
                                                      "/thomas_potsch/thomas_potsch_run.png",
                                                      "/thomas_potsch/thomas_potsch_jump.png",
                                                      "/thomas_potsch/thomas_potsch_fall.png",
                                                      "/thomas_potsch/thomas_potsch_attack.png",
                                                      "/thomas_potsch/thomas_potsch_block.png",
                                                      "/thomas_potsch/thomas_potsch_hit.png",
                                                      "/thomas_potsch/thomas_potsch_death.png", score)

class FaisalZeeshan(Player):
    def __init__(self, x, y, control, score):
        Player.__init__(self, x, y, control, 290, 290, FAISAL_ZEESHAN_NUMBER_SLICES, 
                                                      "/faisal_zeeshan/faisal_zeeshan_idle.png", 
                                                      "/faisal_zeeshan/faisal_zeeshan_run.png",
                                                      "/faisal_zeeshan/faisal_zeeshan_jump.png",
                                                      "/faisal_zeeshan/faisal_zeeshan_fall.png",
                                                      "/faisal_zeeshan/faisal_zeeshan_attack.png",
                                                      "/faisal_zeeshan/faisal_zeeshan_block.png",
                                                      "/faisal_zeeshan/faisal_zeeshan_hit.png",
                                                      "/faisal_zeeshan/faisal_zeeshan_death.png", score)

class Game(): # game init
    def __init__(self):
        
        
        self.characters = [ElectricalEngineer, Scientist, FaisalZeeshan, ThomasPotsch, ElectricalEngineer, Business, Artist, Philosopher]
        self.temp1 = random.choice(self.characters)
        self.temp2 = random.choice(self.characters)
        self.player1 = self.temp1(900, 415, 1, 0)
        self.player2 = self.temp2(250, 415, 2, 0)
        self.back_image_number = random.choice(back_image_numbers)
        back_image_numbers.remove(self.back_image_number)
        
        self.bg_sound = player.loadFile(PATH + "/sounds/background.mp3")
        self.bg_sound.loop()
        
        self.bimage = loadImage(PATH + "/backimages/option_" + self.back_image_number + ".png")
        self.ground = loadImage(PATH + "/backimages/ground.png")

        self.victory = loadImage(PATH + "/backimages/victory.png")
        
        self.count = []
        self.count.append(loadImage(PATH + "/backimages/count1.png"))
        self.count.append(loadImage(PATH + "/backimages/count2.png"))
        self.count.append(loadImage(PATH + "/backimages/count3.png"))
        
        self.player1_wins = []
        self.player1_wins.append(loadImage(PATH + "/backimages/p1 0.png"))
        self.player1_wins.append(loadImage(PATH + "/backimages/p1 1.png"))
        self.player1_wins.append(loadImage(PATH + "/backimages/p1 2.png"))
        self.player1_wins.append(loadImage(PATH + "/backimages/p1 3.png"))
                                 
        self.player2_wins = []
        self.player2_wins.append(loadImage(PATH + "/backimages/p2 0.png"))
        self.player2_wins.append(loadImage(PATH + "/backimages/p2 1.png"))
        self.player2_wins.append(loadImage(PATH + "/backimages/p2 2.png"))
        self.player2_wins.append(loadImage(PATH + "/backimages/p2 3.png"))
        
        self.player1_win = loadImage(PATH + "/backimages/win1.png")
        self.player2_win = loadImage(PATH + "/backimages/win2.png")
                                 
        self.round_over = False
        self.round_over_time = 0
        self.round_over_cooldown = 2
        self.start_count = 3
        self.last_count = time.time()
        self.round_num = 3
        self.game_over = False
        
    def health_bar(self, health, x, y): # tracks health
        noStroke()
        fill(255,255,255)
        rect(x-5, y-5, 410, 40)
        fill(255,0,0)
        rect(x, y, 400, 30)
        fill(255,255,0)
        rect(x, y, (400 * health)/100, 30)
        fill(255,0,0)
        
    def display(self): # displays game
        if self.player1.score >= 3 or self.player2.score >= 3:
            self.game_over = True
            background(0, 0, 0)
            if self.player1.score >= 3:
                image(self.player1_win, 120, 240)
            elif self.player2.score >= 3:
                image(self.player2_win, 120, 240)
            return
        
        self.health_bar(self.player1.health, 76, 40)
        self.health_bar(self.player2.health, 720, 40)
        fill(255,255,255)
        rect(72, 90, 172, 30)
        rect(954, 90, 172, 30)
        fill(255,0,0)
        image(self.player1_wins[self.player1.score], 60, 90)
        image(self.player2_wins[self.player2.score], 943, 90)
        
        self.draw_count()
            
        if self.round_over == False:
            if self.player1.alive == False:
                self.player2.score += 1
                self.round_over_time = time.time()
                self.round_over = True
            elif self.player2.alive == False:
                self.player1.score += 1
                self.round_over_time = time.time()
                self.round_over = True
        else:
            image(self.victory, 390, 160)
            if time.time() - self.round_over_time >= self.round_over_cooldown:
                self.start_count = 3
                self.last_count = time.time()
                self.round_over = False
                self.player1 = self.temp1(900, 415, 1, self.player1.score)
                self.player2 = self.temp2(250, 415, 2, self.player2.score)
    
                self.back_image_number = random.choice(back_image_numbers)
                back_image_numbers.remove(self.back_image_number)
                self.bimage = loadImage(PATH + "/backimages/option_" + self.back_image_number + ".png")
        
        self.player1.display(self.player2)
        self.player2.display(self.player1)
    
    def draw_count(self): # draws counts of wins
        if self.start_count <= 0:
            self.player1.update(self.player2)
            self.player2.update(self.player1)
        else:
            image(self.count[self.start_count - 1], 500, 160)
            if time.time() - self.last_count >= 1:
                self.start_count -= 1
                self.last_count = time.time()

def setup():
    size(RES_WIDTH, RES_HEIGHT)
    background(255,255,255)
    frameRate(50)
    
def draw():
    if game.game_over == False: # if noone won 3 rounds allows playing
        image(game.bimage, 0, 0)
        for i in range(10):
            image(game.ground, 120 * i, GROUND, RES_WIDTH // 10, RES_HEIGHT - GROUND)
        fill(0, 0, 0)
        fill(230, 0, 0)
    game.display()

def keyReleased(): # keystrokes
    if keyCode in [UP, DOWN, RIGHT, LEFT]:
        game.player1.key_handler[keyCode] = False
    if key in [',', '.']:
        game.player1.key_handler[key] = False
        if key == '.':
            game.player1.block_check = False
    if key in ['w', 'a', 's', 'd']:
        game.player2.key_handler[key] = False
    if key in ['1', '2']:
        game.player2.key_handler[key] = False
        if key == '2':
            game.player2.block_check = False
    
def keyPressed(): # cancels keystrokes
    if keyCode in [UP, DOWN, RIGHT, LEFT]:
        game.player1.key_handler[keyCode] = True
    if key in [',', '.']:
        game.player1.key_handler[key] = True
    if key in ['w', 'a', 's', 'd']:
        game.player2.key_handler[key] = True
    if key in ['1', '2']:
        game.player2.key_handler[key] = True

game = Game()
