import pygame
import math

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("정사영 원근투영 비교")
clock = pygame.time.Clock()

# 큐브 꼭짓점
vertices = [
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
]

# 큐브 모서리
edges = [
    [0,1], [1,2], [2,3], [3,0],  # 앞면
    [4,5], [5,6], [6,7], [7,4],  # 뒷면
    [0,4], [1,5], [2,6], [3,7]   # 연결하는 선
]

rotation_x = 0.5
rotation_y = 0.5
distance = 5  # 카메라 거리

def rotate_point(point, rx, ry):
    x, y, z = point
    
    # Y축 회전
    cos_y = math.cos(ry)
    sin_y = math.sin(ry)
    temp_x = x * cos_y - z * sin_y
    temp_z = x * sin_y + z * cos_y
    x, z = temp_x, temp_z
    
    # X축 회전
    cos_x = math.cos(rx)
    sin_x = math.sin(rx)
    temp_y = y * cos_x - z * sin_x
    temp_z = y * sin_x + z * cos_x
    y, z = temp_y, temp_z
    
    return [x, y, z]

def orthographic_projection(point): # 정사영, z좌표를 그냥 무시하는 형태로
    x, y, z = point
    return [x, y]

def perspective_projection(point, d): # 원근 투영
    x, y, z = point
    scale = d / (d + z)
    return [x * scale, y * scale]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                distance += 0.5
            elif event.key == pygame.K_DOWN:
                distance = max(2, distance - 0.5)
    
    # 자동 회전
    rotation_x += 0.01
    rotation_y += 0.02
    
    screen.fill((240, 240, 240))
    
    # 회전된 꼭짓점 계산
    rotated = [rotate_point(v, rotation_x, rotation_y) for v in vertices]
    
    # 정사영
    ortho_projected = [orthographic_projection(v) for v in rotated]
    for edge in edges:
        p1 = ortho_projected[edge[0]]
        p2 = ortho_projected[edge[1]]
        x1 = int(WIDTH//4 + p1[0] * 80)
        y1 = int(HEIGHT//2 - p1[1] * 80)
        x2 = int(WIDTH//4 + p2[0] * 80)
        y2 = int(HEIGHT//2 - p2[1] * 80)
        pygame.draw.line(screen, (100, 100, 255), (x1, y1), (x2, y2), 2)
    
    # 원근투영
    persp_projected = [perspective_projection(v, distance) for v in rotated]
    for edge in edges:
        p1 = persp_projected[edge[0]]
        p2 = persp_projected[edge[1]]
        x1 = int(3*WIDTH//4 + p1[0] * 80)
        y1 = int(HEIGHT//2 - p1[1] * 80)
        x2 = int(3*WIDTH//4 + p2[0] * 80)
        y2 = int(HEIGHT//2 - p2[1] * 80)
        pygame.draw.line(screen, (255, 100, 100), (x1, y1), (x2, y2), 2)
    
    font = pygame.font.Font(None, 36)
    text1 = font.render("정사영", True, (100, 100, 255))
    text2 = font.render("원근투영", True, (255, 100, 100))
    text3 = font.render(f"거리: {distance:.1f}", True, (0, 0, 0))
    screen.blit(text1, (WIDTH//4 - 80, 30))
    screen.blit(text2, (3*WIDTH//4 - 70, 30))
    screen.blit(text3, (WIDTH//2 - 150, HEIGHT - 40))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()