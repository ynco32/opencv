import pygame
import time
import random
 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
dis_width = 1000
dis_height = 1000
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15
red_speed = 40
 

sound_image = pygame.image.load('pygame/sound_on.png')
sound_image = pygame.transform.scale(sound_image, [100, 100])
sound_rect = pygame.Rect(sound_image.get_rect())
sound_rect.left = (dis_width - 60)/2 
sound_rect.top = 10


sound = pygame.mixer.Sound( "pygame/gameover.wav" )


time_delay = 1000
timer_event = pygame.USEREVENT+1
pygame.time.set_timer(timer_event, time_delay)

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("garamond", 35)




def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, blue)
    dis.blit(value, [dis_width/3, 10])
 
def Your_time(cnt):
    text = score_font.render(str(cnt), True, (0, 128, 0))
    dis.blit(text, [dis_width-100, 10])
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
 
 
def gameLoop():
    counter = 0
    counter_sys = 0
    game_over = False
    game_close = False
    
 
    # clock.tick(60)
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
    is_play = 0
    snake_List = []
    Length_of_snake = 1
    red_block1 = round(random.randrange(0, dis_width - snake_block*3) / 10.0) * 10.0
    red_block2 = 0
    red_block1_2 = 0
    red_block2_2 = round(random.randrange(0, dis_width - snake_block*3) / 10.0) * 10.0
 
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
 
    while not game_over:
        while game_close == True:

            # clock.tick(60)
            
            dis.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_PAUSE:
                    is_play = 1
            if event.type == timer_event:
                counter += 1
                counter_sys += 1
                red_block2 += red_speed
                if red_block2 >= dis_width:
                    red_block2 = 0

                red_block1_2 += red_speed
                if red_block1_2 >= dis_height:
                    red_block2 = 0

                text = score_font.render(str(counter), True, (0, 128, 0))
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos[0], event.pos[1])
                # red_block1 = event.pos[0]
                # red_block2 = event.pos[1]
                
 
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        dis.fill(black)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        
        pygame.draw.rect(dis, red, [red_block1, red_block2, snake_block*3, snake_block*3])
        pygame.draw.rect(dis, red, [red_block1_2, red_block2_2, snake_block*3, snake_block*3])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
        Your_time(counter)
        

        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
        
        if x1 >= red_block1 and x1 <= red_block1 + snake_block*3:
            if y1 >= red_block2 and y1 <= red_block2 + snake_block*3:
                game_close = True

        if x1 >= red_block1_2 and x1 <= red_block1_2 + snake_block*3:
            if y1 >= red_block2_2 and y1 <= red_block2_2 + snake_block*3:
                game_close = True

        if counter_sys == 5:
            foodx = round(random.randrange(0, dis_width - snake_block*3) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block*3) / 10.0) * 10.0
            counter_sys = 0
            
        dis.blit(sound_image, sound_rect)

        if is_play == 1:
            print("play....")
            is_play = 0
            sound.play()
 
        clock.tick(snake_speed)
        

        # update the display
    # pygame.display.flip()   
 
    pygame.quit()
    quit()
 
 
gameLoop()
