import pygame
import random

pygame.init()
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 36)

# Цвета
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
PURPLE = (150, 0, 150)
YELLOW = (255, 255, 0)

# Птичка
bird_x = 100
bird_y = HEIGHT // 2
bird_radius = 20
bird_velocity = 0
gravity = 0.5
jump_strength = -8

# Трубы
pipe_width = 60
pipe_gap = 180
pipe_speed = 3
pipes = []
score = 0

# Босс
boss_active = False
boss_gap = 130
boss_width = 100
boss_timer = 0
boss_projectiles = []
boss_shoot_delay = 60  # кадры между выстрелами

def create_pipe():
    top = random.randint(80, HEIGHT - pipe_gap - 80)
    bottom = top + pipe_gap
    return {'x': WIDTH, 'top': top, 'bottom': bottom, 'boss': False}

def create_boss():
    top = random.randint(50, HEIGHT - boss_gap - 50)
    bottom = top + boss_gap
    return {'x': WIDTH, 'top': top, 'bottom': bottom, 'boss': True, 'shoot_timer': 0}

def shoot_from_boss(boss):
    y = (boss['top'] + boss['bottom']) // 2
    return {'x': boss['x'], 'y': y, 'r': 8, 'vx': -6}

# Игра
running = True
game_over = False
pipes.append(create_pipe())

while running:
    clock.tick(60)
    win.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                bird_y = HEIGHT // 2
                bird_velocity = 0
                pipes = [create_pipe()]
                boss_projectiles = []
                score = 0
                boss_active = False
                game_over = False

    if not game_over:
        bird_velocity += gravity
        bird_y += bird_velocity

        # Движение труб
        for pipe in pipes:
            pipe['x'] -= pipe_speed

        # Удаление старых труб
        if pipes and pipes[0]['x'] < -max(pipe_width, boss_width):
            pipes.pop(0)
            score += 1
            boss_active = False

        # Добавление новых труб
        if pipes and pipes[-1]['x'] < WIDTH - 250:
            if score > 0 and score % 5 == 0 and not boss_active:
                pipes.append(create_boss())
                boss_active = True
            else:
                pipes.append(create_pipe())

        # Обновление снарядов
        for proj in boss_projectiles:
            proj['x'] += proj['vx']
        boss_projectiles = [p for p in boss_projectiles if p['x'] > -20]

        # Стрельба босса
        for pipe in pipes:
            if pipe['boss']:
                pipe['shoot_timer'] += 1
                if pipe['shoot_timer'] >= boss_shoot_delay:
                    boss_projectiles.append(shoot_from_boss(pipe))
                    pipe['shoot_timer'] = 0

        # Столкновения с трубами
        for pipe in pipes:
            w = boss_width if pipe['boss'] else pipe_width
            if pipe['x'] < bird_x + bird_radius < pipe['x'] + w:
                if bird_y - bird_radius < pipe['top'] or bird_y + bird_radius > pipe['bottom']:
                    game_over = True

        # Столкновения с снарядами
        for proj in boss_projectiles:
            dx = bird_x - proj['x']
            dy = bird_y - proj['y']
            dist = (dx**2 + dy**2)**0.5
            if dist < bird_radius + proj['r']:
                game_over = True

        if bird_y > HEIGHT or bird_y < 0:
            game_over = True

    # Отрисовка труб
    for pipe in pipes:
        color = PURPLE if pipe['boss'] else GREEN
        w = boss_width if pipe['boss'] else pipe_width
        pygame.draw.rect(win, color, (pipe['x'], 0, w, pipe['top']))
        pygame.draw.rect(win, color, (pipe['x'], pipe['bottom'], w, HEIGHT - pipe['bottom']))

    # Отрисовка снарядов
    for proj in boss_projectiles:
        pygame.draw.circle(win, YELLOW, (int(proj['x']), int(proj['y'])), proj['r'])

    # Птичка
    pygame.draw.circle(win, RED, (bird_x, int(bird_y)), bird_radius)

    # Счёт
    score_text = font.render(f"Счёт: {score}", True, WHITE)
    win.blit(score_text, (10, 10))

    # Game Over
    if game_over:
        over_text = font.render("Вы проиграли! R — рестарт", True, WHITE)
        win.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2))

    pygame.display.flip()

pygame.quit()
