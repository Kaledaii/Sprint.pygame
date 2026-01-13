import pygame
from random import choice, randint
pygame.init()
HEIGHT = 400
WIDTH = 800
game_active=False
start_time=0
music=pygame.mixer.Sound('graphics/music.wav')
music.set_volume(0.1)
music.play(loops=-1)
class Player(pygame.sprite.Sprite):
       def __init__(self):
              super().__init__()
              player=pygame.image.load("graphics/player_stand.png").convert_alpha()
              player_walk_2=pygame.image.load("graphics/player_walk_2.png").convert_alpha()
              self.player_walk=[player,player_walk_2]
              self.index=0
              self.player_jump=pygame.image.load("graphics/jump.png").convert_alpha()
              self.image=self.player_walk[self.index]
              self.rect=self.image.get_rect(midbottom=(50,100))
              self.grav = 0   # added init for gravity
              self.speed=3
              self.jump_sound=pygame.mixer.Sound('graphics/jump.mp3')
              self.jump_sound.set_volume(0.3)

       def player_input(self):
              keys=pygame.key.get_pressed()
              if keys[pygame.K_SPACE] and self.rect.bottom==300:
                     self.grav=-20
                     self.jump_sound.play()
       def apply_gravity(self):
              self.grav+=1
              self.rect.y+=self.grav
              if self.rect.bottom>=300:self.rect.bottom=300

       def player_animation(self):
              if self.rect.bottom<300:
                self.image=self.player_jump
              else:
                if self.index>=len(self.player_walk):self.index=0
                self.image=self.player_walk[int(self.index)]
                self.index+=0.1

       def update(self):
              self.player_input()
              self.apply_gravity()
              self.player_animation()
              self.rect.x+=self.speed
              if self.rect.right>=400:
                     self.rect.right=400

class Obstacle(pygame.sprite.Sprite):
       def __init__(self,type):
              super().__init__()

              if type=='fly':
                    fly1=pygame.image.load("graphics/fly1.png").convert_alpha()
                    fly2=pygame.image.load("graphics/fly2.png").convert_alpha()
                    self.frames=[fly1,fly2]
                    y_pos=200
              else:
                    snail1=pygame.image.load("graphics/snail1.png").convert_alpha()
                    snail2=pygame.image.load("graphics/snail2.png").convert_alpha()
                    self.frames=[snail1,snail2]
                    y_pos=300
              self.index=0
              self.image=self.frames[self.index]
              self.rect=self.image.get_rect(midbottom=(randint(900,1100),y_pos))

       def animation(self):
              if self.index>=len(self.frames):self.index=0
              self.image=self.frames[int(self.index)]
              self.index+=0.1

       def update(self):
               self.animation()
               self.rect.x-=5
               if self.rect.x<=-50:
                      self.kill()


# --- COMMENTED OUT: old obstacle/player rect system ---
# def obstacle_movement(obstacle_list): ...
# def player_animation(): ...
# def collison(player,obstacles): ...

def display_score():
       current_time=int(pygame.time.get_ticks()/1000)-start_time
       score_surf=font.render(f"Score: {current_time}",False,(0,0,0))
       score_rect=score_surf.get_rect(center=(400,50))
       screen.blit(score_surf,score_rect)
       return current_time

screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock=pygame.time.Clock()
font=pygame.font.Font('graphics/Pixeltype.ttf',50)

sky_surface=pygame.image.load("graphics/Sky.png").convert_alpha()
ground_surface=pygame.image.load("graphics/ground.png").convert_alpha()

# Groups
play=pygame.sprite.GroupSingle()
play.add(Player())

obstacle_group=pygame.sprite.Group()

# --- COMMENTED OUT: duplicate player rect/surf system ---
# obstacle_rect_list=[]
# player=pygame.image.load("graphics/player_stand.png").convert_alpha()
# player_walk_2=pygame.image.load("graphics/player_walk_2.png").convert_alpha()
# player_walk=[player,player_walk_2]
# index=0
# player_jump=pygame.image.load("graphics/jump.png").convert_alpha()
# player_surf=player_walk[index]
# player_rect=player_surf.get_rect(midbottom=(50,300))
# player_grav=0

# outro shii
player_stand=pygame.image.load("graphics/player_stand.png").convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect=player_stand.get_rect(center=(400,200))
font.set_italic(True)
title=font.render("Pixel Runner",False,(111,196,169))
title_rect=title.get_rect(center=(400,80))
font.set_italic(False)
text_surface=font.render("Press space to run",False,(111,196,169))
text_rect=text_surface.get_rect(center=(400,350))
running=True
score=0

# obstacle timer
obstacle_timer=pygame.USEREVENT+1
pygame.time.set_timer(obstacle_timer,1500)

# snail_timer=pygame.USEREVENT+2
# pygame.time.set_timer(snail_timer,500)

# fly_timer=pygame.USEREVENT+3
# pygame.time.set_timer(fly_timer,200)

while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

            if game_active:
                if event.type==obstacle_timer:
                        obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))

            else:
                if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                       game_active=True
                       start_time=int(pygame.time.get_ticks()/1000)
                       play.sprite.rect.midbottom = (50, 100)   # spawn high
                       play.sprite.grav = 0

        if game_active:      
                screen.blit(sky_surface, (0,0))
                screen.blit(ground_surface,(0,300))
               

                # Player
                play.draw(screen)
                play.update()

                # Obstacles
                obstacle_group.draw(screen)
                obstacle_group.update()
                score = display_score()
                # Collision
                if pygame.sprite.spritecollide(play.sprite, obstacle_group,False):
                       game_active=False

        else:
                obstacle_group.empty()
                screen.fill((94,129,162))
                screen.blit(player_stand,player_stand_rect)
                screen.blit(title,title_rect)
                if score==0:
                       screen.blit(text_surface,text_rect)
                else:
                       score_message=font.render(f"Your score: {score}",False,(111,196,169))
                       score_message_rect=score_message.get_rect(center=(400,350))
                       screen.blit(score_message,score_message_rect)

        pygame.display.update()
        clock.tick(60)
pygame.quit()