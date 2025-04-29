import pygame
import random

pygame.init()

# 화면 크기 설정
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Circle, Square and Luck")

#점수
score = 0
font = pygame.font.SysFont(None, 36)

# 색깔
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# 동그라미 시작 위치
x = 500
y = 300
radius = 20  # 반지름

# 네모
red_rect = [pygame.Rect(400, 300, 50, 50)]
green_rect = pygame.Rect(700, 200, 50, 50)
green_alive = True
red_spawned = 1  # 초기에 1개 생성되어 있음


def is_collision(circle_x, circle_y, radius, rect):
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))
    distance_x = circle_x - closest_x
    distance_y = circle_y - closest_y
    return distance_x ** 2 + distance_y ** 2 < radius ** 2

def draw_score(score):
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

def respawn_green():
    return pygame.Rect(random.randint(0, 950), random.randint(0, 550), 50, 50)

def spawn_red():
    return pygame.Rect(random.randint(0, 950), random.randint(0, 550), 50, 50)

# 속도
speed = 1

def play_game():
    global score
    global x, y, radius, speed
    global red_rect, green_rect, green_alive, red_spawned

    # 초기화
    score = 0
    x = 500
    y = 300
    radius = 20
    speed = 1
    red_rect = [pygame.Rect(400, 100, 50, 50)]
    green_rect = pygame.Rect(700, 200, 50, 50)
    green_alive = True
    red_spawned = 1

    # 게임 루프 (반복해서 화면을 유지)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 키 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x - radius > 0:
            x -= speed
        if keys[pygame.K_RIGHT] and x + radius < 1000:
            x += speed
        if keys[pygame.K_UP] and y - radius > 0:
            y -= speed
        if keys[pygame.K_DOWN] and y + radius < 600:
            y += speed

        if score // 5 + 1 > red_spawned:
            red_rect.append(spawn_red())
            red_spawned += 1


        # 충돌 체크
        for red in red_rect:
            if is_collision(x, y, radius, red):
                running = False


        if green_alive and is_collision(x, y, radius, green_rect):
            green_alive = False
            score += 1
            green_rect = respawn_green()
            green_alive = True

        # 화면 다시 그리기
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, BLUE, (x, y), radius)  # 동그라미 그리기
        for red in red_rect:
            pygame.draw.rect(screen, RED, red)
        if green_alive:
            pygame.draw.rect(screen, GREEN, green_rect)
        draw_score(score)
        pygame.display.update()

while True:
    play_game()
    # 게임 끝나고
    screen.fill((0, 0, 0))
    game_over_text = font.render(f"Your Score is {score}", True, (255, 255, 255))
    retry_text = font.render("Retry: Press any key (ESC to quit)", True, (255, 255, 255))
    screen.blit(game_over_text, (400, 250))
    screen.blit(retry_text, (300, 320))
    pygame.display.update()

    # 아무 키나 입력 기다리기
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                else:
                    waiting = False
