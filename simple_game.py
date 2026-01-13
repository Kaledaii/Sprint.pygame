import pygame
from random import randint
pygame.init()
HEIGHT = 400
WIDTH = 800
game_active=False
start_time=0



def obstacle_movement(obstacle_list):
       if obstacle_list:
              for obstacle in obstacle_list:
                     obstacle.x-=5
                     if obstacle.bottom==300:
                            screen.blit(snail_surf,obstacle)
                     else:
                            screen.blit(fly_surf,obstacle)
              obstacle_list=[obstacle for obstacle in obstacle_list if obstacle.x>-100]
              return obstacle_list
       else: return []

def player_animation():
       global player_surf,index

       if player_rect.bottom<300:
              player_surf=player_jump
       else:
              if index>=len(player_walk):index=0
              player_surf=player_walk[int(index)]
              index+=0.1


def collison(player,obstacles):
       if obstacles:
              for obstacle in obstacles:
                     if player.colliderect(obstacle):return False
       return True

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


snail1=pygame.image.load("graphics/snail1.png").convert_alpha()
snail2=pygame.image.load("graphics/snail2.png").convert_alpha()
snail=[snail1,snail2]
snail_index=0
snail_surf=snail[int(snail_index)]
snail_rect=snail_surf.get_rect(midbottom=(720,300))

fly1=pygame.image.load("graphics/fly1.png").convert_alpha()
fly2=pygame.image.load("graphics/fly2.png").convert_alpha()
fly=[fly1,fly2]
fly_index=0
fly_surf=fly[int(fly_index)]
fly_rect=fly_surf.get_rect(midbottom=(900,200))


obstacle_rect_list=[]

player=pygame.image.load("graphics/player_stand.png").convert_alpha()
player_walk_2=pygame.image.load("graphics/player_walk_2.png").convert_alpha()
player_walk=[player,player_walk_2]
index=0
player_jump=pygame.image.load("graphics/jump.png").convert_alpha()

player_surf=player_walk[index]
player_rect=player_surf.get_rect(midbottom=(50,300))
player_grav=0

#outro shii
player_stand=pygame.image.load("graphics/player_stand.png").convert_alpha()
print("Before:", player_stand.get_size())
player_stand = pygame.transform.scale2x(player_stand)
print("After:", player_stand.get_size())
player_stand_rect=player_stand.get_rect(center=(400,200))
font.set_italic(True)
title=font.render("Pixel Runner",False,(111,196,169))
title_rect=title.get_rect(center=(400,80))
font.set_italic(False)
text_surface=font.render("Press space to run",False,(111,196,169))
text_rect=text_surface.get_rect(center=(400,350))
running=True
score=0

#obstacle timer
obstacle_timer=pygame.USEREVENT+1
pygame.time.set_timer(obstacle_timer,1500)

snail_timer=pygame.USEREVENT+2
pygame.time.set_timer(snail_timer,500)

fly_timer=pygame.USEREVENT+3
pygame.time.set_timer(fly_timer,200)

while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

            if game_active:
                if event.type==obstacle_timer:
                        if randint(0,1):
                                obstacle_rect_list.append(snail_surf.get_rect(midbottom=(randint(900,1100),300)))
                        else:
                                obstacle_rect_list.append(fly_surf.get_rect(midbottom=(randint(900,1100),200)))

                if event.type==snail_timer:
                       if snail_index==0:snail_index=1
                       else:snail_index=0
                       snail_surf=snail[int(snail_index)]

                if event.type==fly_timer:
                       if fly_index==0:fly_index=1
                       else:fly_index=0
                       fly_surf=fly[int(fly_index)]

                if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_SPACE and player_rect.bottom==300:
                                player_grav=-20
                                print("Jump")
                
                if event.type==pygame.MOUSEBUTTONDOWN:
                        if player_rect.collidepoint(event.pos) and player_rect.bottom==300:
                                player_grav=-20
                                print("Jump")
            else:
                if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                       game_active=True
                       snail_rect.left=800
                       start_time=int(pygame.time.get_ticks()/1000)
                       player_grav = 0
                       player_rect.midbottom = (50, 100)

        if game_active:  
                score = display_score()    
                screen.blit(sky_surface, (0,0))
                screen.blit(ground_surface,(0,300))



                display_score()
                player_animation()
                player_grav+=1
                player_rect.y+=player_grav
                if player_rect.bottom>=300:player_rect.bottom=300
                screen.blit(player_surf,player_rect)
                # player_rect.x+=3

                #obstacle movement function
                obstacle_rect_list=obstacle_movement(obstacle_rect_list)
                game_active=collison(player_rect,obstacle_rect_list)

        else:
                obstacle_rect_list.clear()
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