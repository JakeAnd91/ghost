import pygame

pygame.init()

# Screen setup
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Drawing Shapes")
clock = pygame.time.Clock()

scene = pygame.Surface((600,600), pygame.SRCALPHA)

dark_blue = (10, 25, 74)
light_blue = (30, 150, 255)

def draw_glow_circle(surface, color, pos, radius, layers=6):
    r, g, b = color
    for i in range(layers, 0, -1):
        alpha = int(40 / i)  # lower = brighter center
        glow_surf = pygame.Surface((radius*4, radius*4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (r, g, b, alpha), (radius*2, radius*2), radius + i*8)
        surface.blit(glow_surf, (pos[0] - radius*2, pos[1] - radius*2), special_flags=pygame.BLEND_RGB_ADD)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    scene.fill((0,0,0,0))  # transparent clear

    # Glow behind center circle
    draw_glow_circle(scene, light_blue, (300, 250), 40)

    # Shapes
    pygame.draw.circle(scene, dark_blue, (300, 250), 150)
    pygame.draw.polygon(scene, light_blue, ([300,170], [380,250], [300, 330], [220,250]), 60)
    pygame.draw.line(scene, dark_blue, (450, 250), (150, 250), 5)
    pygame.draw.circle(scene, light_blue, (300, 250), 30)

    # Rotate
    rotated = pygame.transform.rotate(scene, -90)

    screen.fill((30,30,30))
    screen.blit(rotated, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
