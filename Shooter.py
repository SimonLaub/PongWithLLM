"""
Shoote game project. October 2024.
- Programming a Shooter game using an LLM
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:41:14 2024

@author: sila
"""


import pygame
import math
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple FPS Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player setup
player_pos = [400, 300]
player_angle = 0  # Angle in degrees
player_speed = 5
turn_speed = 5

# Bullet setup
bullets = []
bullet_speed = 10

# Enemy setup
enemies = [[random.randint(100, 700), random.randint(100, 500)] for _ in range(5)]
enemy_size = 30

# Font
font = pygame.font.Font(None, 36)

# Main game loop
def main():
    running = True
    score = 0
    clock = pygame.time.Clock()
    global player_angle

    while running:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Key Presses for Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_angle -= turn_speed
        if keys[pygame.K_RIGHT]:
            player_angle += turn_speed
        if keys[pygame.K_UP]:  # Move forward
            player_pos[0] += player_speed * math.cos(math.radians(player_angle))
            player_pos[1] += player_speed * math.sin(math.radians(player_angle))
        if keys[pygame.K_DOWN]:  # Move backward
            player_pos[0] -= player_speed * math.cos(math.radians(player_angle))
            player_pos[1] -= player_speed * math.sin(math.radians(player_angle))

        # Shooting bullets
        if keys[pygame.K_SPACE]:
            # Create a new bullet in the direction of player angle
            bullet_dx = bullet_speed * math.cos(math.radians(player_angle))
            bullet_dy = bullet_speed * math.sin(math.radians(player_angle))
            bullets.append([player_pos[0], player_pos[1], bullet_dx, bullet_dy])

        # Update bullets
        for bullet in bullets[:]:
            bullet[0] += bullet[2]  # Update bullet x position
            bullet[1] += bullet[3]  # Update bullet y position
            # Remove bullet if it goes off-screen
            if bullet[0] < 0 or bullet[0] > SCREEN_WIDTH or bullet[1] < 0 or bullet[1] > SCREEN_HEIGHT:
                bullets.remove(bullet)

        # Check bullet collision with enemies
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if math.hypot(bullet[0] - enemy[0], bullet[1] - enemy[1]) < enemy_size:
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                    break

        # Draw Player (represented as a line showing direction)
        player_end_x = player_pos[0] + 30 * math.cos(math.radians(player_angle))
        player_end_y = player_pos[1] + 30 * math.sin(math.radians(player_angle))
        pygame.draw.line(screen, WHITE, player_pos, (player_end_x, player_end_y), 5)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet[1])), 5)

        # Draw enemies
        for enemy in enemies:
            enemy_distance = math.hypot(enemy[0] - player_pos[0], enemy[1] - player_pos[1])
            scale = max(1, min(1 / (enemy_distance / 200), 5))  # Scaling effect based on distance
            enemy_display_size = int(enemy_size * scale)
            pygame.draw.circle(screen, RED, (int(enemy[0]), int(enemy[1])), enemy_display_size)

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update display
        pygame.display.flip()
        clock.tick(30)  # FPS

# Start game
if __name__ == "__main__":
    main()
