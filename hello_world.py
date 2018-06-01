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
bg = pygame.image.load("JungleAssetPack/parallaxBackground/plx-5.png").convert()
# bgWidth, bgHeight = bg.get_rect().size
bg_size = pygame.transform.scale(bg, (800, 480))
bgScaleWidth = bg_size.get_rect().width

# initialize for background scrolling
stageWidth = bgScaleWidth * 2
startScrollingPosX = HW
stagePosX = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(
            "JungleAssetPack/Character/sprites/idle.gif").convert_alpha()  # pygame.Surface((50, 40))
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
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
            self.image = self.imageflip
        elif keystate[pygame.K_RIGHT]:
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

    rel_x = stagePosX % bgScaleWidth
    screen.blit(bg_size, (rel_x - bgScaleWidth, 0))
    if rel_x < WIDTH:
        screen.blit(bg_size, (rel_x, 0))

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
