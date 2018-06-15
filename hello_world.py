# KidsCanCode - Game Development with Pygame video series
# Shmup game - part 1
# Video link: https://www.youtube.com/watch?v=nGufy7weyGY
# Player sprite and movement
import pygame

WIDTH, HEIGHT = 800, 480
HW, HH = WIDTH / 2, HEIGHT / 2
x = 0
FPS = 60

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DeathGame")
pygame.display.toggle_fullscreen()

ground = pygame.image.load("JungleAssetPack/jungletileset/Jungle_Ground.png").convert_alpha()
ground_size = pygame.transform.scale(ground, (800, 60))


# bg 1
bg1 = pygame.image.load("JungleAssetPack/parallaxBackground/plx-1.png").convert_alpha()
bg1_size = pygame.transform.scale(bg1, (800, 480))
bgScaleWidth1 = bg1_size.get_rect().width

# bg 2
bg2 = pygame.image.load("JungleAssetPack/parallaxBackground/plx-2.png").convert_alpha()
bg2_size = pygame.transform.scale(bg2, (800, 480))
bgScaleWidth2 = bg2_size.get_rect().width

# bg 3
bg3 = pygame.image.load("JungleAssetPack/parallaxBackground/plx-3.png").convert_alpha()
bg3_size = pygame.transform.scale(bg3, (800, 480))
bgScaleWidth3 = bg3_size.get_rect().width

# bg 4
bg4 = pygame.image.load("JungleAssetPack/parallaxBackground/plx-4.png").convert_alpha()
bg4_size = pygame.transform.scale(bg4, (800, 480))
bgScaleWidth4 = bg4_size.get_rect().width

# bg 5
bg5 = pygame.image.load("JungleAssetPack/parallaxBackground/plx-5.png").convert_alpha()
bg5_size = pygame.transform.scale(bg5, (800, 480))
bgScaleWidth5 = bg5_size.get_rect().width


# initialize for background scrolling
stageWidth = bgScaleWidth5 * 2
startScrollingPosX = HW
stagePosX = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("JungleAssetPack/Character/sprites/idle.gif").convert_alpha()
        self.imageRun = pygame.image.load("JungleAssetPack/Character/sprites/run.gif").convert_alpha()
        self.imageflip = pygame.transform.flip(self.imageRun, True, False)
        self.playerwidth = self.image.get_width()
        self.playerheight = self.image.get_height()
        self.playerposx = self.playerwidth
        self.newHeight = pygame.transform.scale(self.image, (19, 17))
        # rect
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 50
        self.speedx = 0
        self.speedy = 0
        self.stageposx = 0
        self.x = 0

    def update(self):

        self.speedx = 0
        self.speedy = 0

        # Key pressed: constant movement
        keystate = pygame.key.get_pressed()
        mousepos = pygame.mouse.get_pos()
        mousepress = pygame.mouse.get_pressed()
        pygame.mouse.set_visible(True)
        if keystate[pygame.K_LEFT] or mousepos < (HW, HEIGHT) and mousepress == (1, 0, 0):
            self.speedx = -8
            self.image = self.imageflip
        elif keystate[pygame.K_RIGHT] or mousepos > (HW, HEIGHT) and mousepress == (1, 0, 0):
            self.speedx = 8
            self.image = pygame.image.load("JungleAssetPack/Character/sprites/run.gif").convert_alpha()
        elif keystate[pygame.K_DOWN]:
            # self.image = pygame.image.load("JungleAssetPack/Character/sprites/landing.png").convert_alpha()
            self.image = self.newHeight
            self.rect.bottom = HEIGHT - 50 + 19
        else:
            self.image = pygame.image.load("JungleAssetPack/Character/sprites/idle.gif").convert_alpha()
            self.rect.bottom = HEIGHT - 50

        # Key pressed: only one move
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.rect.bottom = HEIGHT - 100
                self.image = pygame.image.load("JungleAssetPack/Character/sprites/jump.png").convert_alpha()

        # Key release: only one move
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.rect.bottom = HEIGHT - 50

        self.rect.x += self.speedx
        if self.rect.right > WIDTH - 100:
            self.rect.right = WIDTH - 100
        if self.rect.left < 100:
            self.rect.left = 100

        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Game loop
running = True
while running:

    if player.playerposx < startScrollingPosX:
        newPlayerPosX = player.playerposx
    elif player.playerposx > stageWidth - startScrollingPosX:
        newPlayerPosX = player.playerposx - stageWidth + WIDTH
    else:
        newPlayerPosX = startScrollingPosX

    stagePosX += -player.speedx

    rel_x = stagePosX % bgScaleWidth5
    screen.blit(bg1_size, (rel_x - bgScaleWidth1, 0))
    screen.blit(bg2_size, (rel_x - bgScaleWidth2, 0))
    screen.blit(bg3_size, (rel_x - bgScaleWidth3, 0))
    screen.blit(bg4_size, (rel_x - bgScaleWidth4, 0))
    screen.blit(bg5_size, (rel_x - bgScaleWidth5, 0))

    if rel_x < WIDTH:
        screen.blit(bg1_size, (rel_x, 0))
        screen.blit(bg2_size, (rel_x, 0))
        screen.blit(bg3_size, (rel_x, 0))
        screen.blit(bg4_size, (rel_x, 0))
        screen.blit(bg5_size, (rel_x, 0))

    rel_ground = stagePosX % ground_size.get_rect().width
    screen.blit(ground_size, (rel_ground - ground_size.get_rect().width, 420))
    if rel_ground < WIDTH:
            screen.blit(ground_size, (rel_ground, 420))

    Player()

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False


    # Update
    all_sprites.update()

    # Draw / render

    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
