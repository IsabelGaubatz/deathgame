# KidsCanCode - Game Development with Pygame video series
# Shmup game - part 1
# Video link: https://www.youtube.com/watch?v=nGufy7weyGY
# Player sprite and movement
import pygame



WIDTH, HEIGHT = 800, 480
HW, HH = WIDTH/2, HEIGHT/2
x = 0
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HelloWorld")
bg = pygame.image.load("JungleAssetPack/parallaxBackground/plx-5.png").convert()
bgWidth, bgHeight = bg.get_rect().size
bg_size = pygame.transform.scale(bg, (800, 480))
bgScaleWidth = bg_size.get_rect().width


stageWidth = bgScaleWidth*2


startScrollingPosX = HW



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("JungleAssetPack/Character/sprites/idle.gif").convert()#pygame.Surface((50, 40))
        self.playerwidth = self.image.get_width()
        self.playerheight = self.image.get_height()
        self.playerposx = self.playerwidth
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.stageposx = 0
        self.x = 0




    def update(self):

            self.speedx = 0
            self.speedy = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -8
                self.image = pygame.image.load("JungleAssetPack/Character/sprites/run.gif").convert()
            elif keystate[pygame.K_RIGHT]:
                self.speedx = 8
                self.image = pygame.image.load("JungleAssetPack/Character/sprites/run.gif").convert()
            elif keystate[pygame.K_DOWN]:
                self.speedy = 8
                self.image = pygame.image.load("JungleAssetPack/Character/sprites/jump.png").convert()
            elif keystate[pygame.K_UP]:
                self.speedy = -8
                self.image = pygame.image.load("JungleAssetPack/Character/sprites/landing.png").convert()
            else:
                self.image = pygame.image.load("JungleAssetPack/Character/sprites/idle.gif").convert()


            self.rect.x += self.speedx
            if self.rect.right > WIDTH: #kann man verwenden um zu schauen, wann das Hintergrundbild weiter läuft
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

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

    rel_x = x % bgScaleWidth
    screen.blit(bg_size, (rel_x - bgScaleWidth, 0))
    if rel_x < WIDTH:
        screen.blit(bg_size, (rel_x, 0))
    x -= 1


    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    #screen.blit(bg_size, [0, 0])

    # Update
    all_sprites.update()

    # Draw / render

    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()

