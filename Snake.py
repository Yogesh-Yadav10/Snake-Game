#library
import pygame #for writing games
import random #random values generate krna

pygame.init() #modules import

# SOUND k lie code
pygame.mixer.init() #use for mulimedia
food_sound = pygame.mixer.Sound("D:/Journey/Snake-Game/eating.wav")
gameover_sound = pygame.mixer.Sound("D:/Journey/Snake-Game/gameover.wav")
click_sound = pygame.mixer.Sound("D:/Journey/Snake-Game/click.wav")

# Game screen settings
WIDTH=1550 
HEIGHT = 805

#Background image
bg_image = pygame.image.load("D:/Journey/Snake-Game/background.jpg")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
clock = pygame.time.Clock()

screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors and fonts
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,200,0)
RED = (200,0,0)

title_font = pygame.font.SysFont("Impact", 60)
button_font = pygame.font.SysFont("Georgia", 40)
score_font = pygame.font.SysFont("Georgia", 35)

#Buttons
start_button=pygame.Rect(700,250,200,60)
exit_button = pygame.Rect(700, 350, 200, 60)
restart_button = pygame.Rect(675, 400, 250, 60)
exit_button2 = pygame.Rect(675, 480, 250, 60)
game_state="home"

#Snake Variables
snake_x = 200
snake_y = 200
GRID_SIZE=20
snake_speed = GRID_SIZE
direction = "RIGHT"
score = 0
snake_body=[]
snake_length=1

# High Score
highscore_file = open("highscore.txt", "r")
high_score = int(highscore_file.read())
highscore_file.close()

# Food code
food_x = random.randrange(0, WIDTH, GRID_SIZE)
food_y = random.randrange(0, HEIGHT, GRID_SIZE)

running=True

# Main game loop 
while running:
    for event in pygame.event.get():

#Window events
        if event.type== pygame.QUIT:
         running=False
         
#Mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
         print("Mouse Click Hua")

#Game Home Screen
         if game_state=="home":
          if start_button.collidepoint(event.pos):
            click_sound.play()
            print("Start Button Clicked")

          if exit_button.collidepoint(event.pos):
            click_sound.play()
            print("Home Exit Clicked")
            running = False
          game_state="game"

#Game Over screen
         if game_state=="game_over":

          if restart_button.collidepoint(event.pos):
            click_sound.play()
            print("Restart Clicked")
            game_state = "game"

#Snake Variables
            snake_x = 200
            snake_y = 200
            direction = "RIGHT"
            score = 0
            snake_body = []
            snake_length = 1
            
#Food code
            food_x = random.randrange(0, WIDTH, GRID_SIZE)
            food_y = random.randrange(0, HEIGHT, GRID_SIZE)

          if exit_button2.collidepoint(event.pos):
           click_sound.play()
           print("exit Clicked")
           running= False

# Keyboard Events ka code
        if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_RIGHT:
          if direction != "LEFT":
            direction="RIGHT"
            print("RIGHT KEY PRESSED")
         if event.key == pygame.K_LEFT:
           if direction != "RIGHT":
            direction="LEFT"
            print("LEFT KEY PRESSED")
         if event.key == pygame.K_UP:
           if direction != "DOWN":
            direction="UP"
            print("UP KEY PRESSED")
         if event.key == pygame.K_DOWN:
          if direction != "UP":
           direction="DOWN"
           print("DOWN KEY PRESSED")

         if event.key == pygame.K_SPACE:
           click_sound.play()
           if game_state == "game":
               game_state = "pause"

           elif game_state == "pause":
              game_state = "game"

#background image code
    screen.blit(bg_image, (0, 0))

#Home Screen code
    if game_state=="home":

        pygame.draw.rect(screen, GREEN, start_button)
        start_text = button_font.render("Start", True, WHITE)
        text_rect=start_text.get_rect(center=start_button.center)
        screen.blit(start_text, text_rect)

        pygame.draw.rect(screen, RED,exit_button)
        exit_text = button_font.render("Exit", True, WHITE)
        text_rect_exit=exit_text.get_rect(center=exit_button.center)
        screen.blit(exit_text, text_rect_exit)

        title_text=title_font.render("Welcome To Snake Game", True, WHITE)
        title_rect=title_text.get_rect(center=(775,80))
        screen.blit(title_text, title_rect)

#Game Screen
    if game_state=="game":
      
       score_text = score_font.render(f"Score: {score}", True, WHITE)
       screen.blit(score_text, (20, 20))

       high_score_text = score_font.render(f"High Score: {high_score}", True, WHITE)
       screen.blit(high_score_text, (20, 60))
       
       if direction=="RIGHT":
        snake_x += snake_speed
       if direction == "LEFT":
        snake_x -= snake_speed
       if direction == "UP":
        snake_y -= snake_speed
       if direction == "DOWN":
        snake_y += snake_speed

# Snake Wall collision code
       if snake_x < 0 or snake_x >= WIDTH or snake_y < 0 or snake_y >= HEIGHT:
        game_state = "game_over"
        gameover_sound.play()

#Snake body code
       snake_body.append((snake_x, snake_y))
       if len(snake_body) > snake_length:
        snake_body.pop(0)

       food_rect=pygame.Rect(food_x, food_y, GRID_SIZE, GRID_SIZE)
       pygame.draw.circle(screen, RED, (food_x+GRID_SIZE //2, food_y+ GRID_SIZE//2),GRID_SIZE//2)
       
       for segment in snake_body:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

#Snake self collision code
       snake_rect = pygame.Rect(snake_x, snake_y, GRID_SIZE, GRID_SIZE)
       for segment in snake_body[:-1]:
        body_rect = pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE)

        if snake_rect.colliderect(body_rect):
          game_state = "game_over"
          gameover_sound.play()

#Food collision code
       if snake_rect.colliderect(food_rect):
        food_sound.play()
        print("Food Eaten")
        score+=1
        snake_length+=1
        if score > high_score:
         high_score = score

#Highscore filehandling code
         highscore_file = open("highscore.txt", "w")
         highscore_file.write(str(high_score))
         highscore_file.close()

#food setup
        food_x = random.randrange(0, WIDTH, GRID_SIZE)
        food_y = random.randrange(0, HEIGHT, GRID_SIZE)

        while (food_x, food_y) in snake_body:

#food setup
         food_x = random.randrange(0, WIDTH, GRID_SIZE)
         food_y = random.randrange(0, HEIGHT, GRID_SIZE)

#Game over screen state code
    if game_state=="game_over":
      screen.fill(BLACK)
      game_over_text = title_font.render("GAME OVER ", True, RED)
      game_over_rect = game_over_text.get_rect(center=(775,250))
      screen.blit(game_over_text, game_over_rect)

      pygame.draw.rect(screen, RED,restart_button)
      restart_text = button_font.render("Restart", True, WHITE)
      text_rect_restart=restart_text.get_rect(center=restart_button.center)
      screen.blit(restart_text, text_rect_restart)
      
      pygame.draw.rect(screen, RED,exit_button2)
      exit_text = button_font.render("Exit", True, WHITE)
      text_rect_exit=exit_text.get_rect(center=exit_button2.center)
      screen.blit(exit_text, text_rect_exit)

#Game pause screen code
    if game_state == "pause":

     screen.fill(BLACK)

     pause_text = title_font.render("PAUSED", True, WHITE)
     pause_rect = pause_text.get_rect(center=(775, 250))
     screen.blit(pause_text, pause_rect)

     resume_text = button_font.render("Press SPACE to Resume", True, WHITE)
     resume_rect = resume_text.get_rect(center=(775, 320))
     screen.blit(resume_text, resume_rect)

#code for screen update
    pygame.display.update()
    clock.tick(10) #fps of game ie 10
pygame.quit() #pygame and other modules closed

