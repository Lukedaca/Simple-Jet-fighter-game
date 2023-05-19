import pygame
import sys
import random

# Konstanty pro okno
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# Barvy
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
# Inicializace Pygame
pygame.init()

# Nastavení okna
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Hráč
player = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, 50, 50)

# Střely hráče
bullets = []

# Střely nepřítele
enemy_bullets = []

# Nepřítel
enemy = pygame.Rect(SCREEN_WIDTH // 2, 0, 50, 50)

# Nastavení hodin (pro FPS)
clock = pygame.time.Clock()

# Stav hry
running, playing, paused = True, False, False
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if playing:
                    paused = not paused
                else:
                    running = False
            elif event.key == pygame.K_RETURN and not paused:
                playing = True
                enemy.x = SCREEN_WIDTH // 2  # reset pozice nepřítele
                enemy.y = 0
            elif event.key == pygame.K_SPACE and playing and not paused:  # střelba
                bullet = pygame.Rect(player.x + 20, player.y, 10, 20)
                bullets.append(bullet)
    keys = pygame.key.get_pressed()
    if not paused and playing:
        if keys[pygame.K_LEFT] and player.x - 5 > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.x + 5 < SCREEN_WIDTH - 50:
            player.x += 5
    screen.fill(BLACK)
    if playing and not paused:
        pygame.draw.rect(screen, GREEN, player)
        pygame.draw.rect(screen, RED, enemy)
        enemy.y += 1  # snížení rychlosti nepřítele
        if random.randint(0, 100) < 2:  # 2% šance na střelbu v každém framu
            enemy_bullet = pygame.Rect(enemy.x + 20, enemy.y + 50, 10, 20)
            enemy_bullets.append(enemy_bullet)
        for bullet in bullets[:]:
            bullet.y -= 5
            pygame.draw.rect(screen, WHITE, bullet)
            if bullet.colliderect(enemy):  # detekce kolize mezi střelou a nepřítelem
                bullets.remove(bullet)  # odebrání střely
                enemy.y = 0  # reset nepřítele

        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet.y += 5
            pygame.draw.rect(screen, RED, enemy_bullet)
            if enemy_bullet.colliderect(player):  # detekce kolize mezi střelou nepřítele a hráčem
                enemy_bullets.remove(enemy_bullet)  # odebrání střely
                playing = False  # konec hry, pokud hráč je zasažen

        bullets = [bullet for bullet in bullets if bullet.y > 0]
        enemy_bullets = [enemy_bullet for enemy_bullet in enemy_bullets if enemy_bullet.y < SCREEN_HEIGHT]

        if enemy.y > SCREEN_HEIGHT:
            playing = False  # konec hry, pokud nepřítel dosáhne spodní části obrazovky
    elif paused:
        font = pygame.font.Font(None, 36)
        text = font.render("Game is paused, press ESC to resume", 1, (255, 255, 255))
        screen.blit(text, (100, 200))
    else:
        font = pygame.font.Font(None, 36)
        text = font.render("Press Enter to start game, or close window to quit", 1, (255, 255, 255))
        screen.blit(text, (100, 100))
    
    pygame.display.flip()

pygame.quit()
sys.exit()

