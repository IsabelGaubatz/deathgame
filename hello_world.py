import pygame
# import os  # to use path directory
# import numpy as np  # to use numpy.asarray to convert a list to an array

WIDTH, HEIGHT = 800, 480
HW, HH = WIDTH / 2, HEIGHT / 2
FPS = 60

# path directories
pathBackground = 'JungleAssetPack/parallaxBackground/'
pathTileset = 'JungleAssetPack/jungletileset/'
pathPlayer = 'JungleAssetPack/Character/sprites/'

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
pygame.display.set_caption("DeathGame")

# TODO: default in Fullscreen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
# TODO: default mouse visible False
pygame.mouse.set_visible(True)

# World and Background
ground = pygame.image.load(pathTileset + "Jungle_Ground.png").convert_alpha()
ground_size = pygame.transform.scale(ground, (800, 60))

obstacle = pygame.image.load(pathTileset + "tileset-01.png").convert_alpha()
obstacle_size = pygame.transform.scale(obstacle, (60, 60))

# bg 1
bg1 = pygame.image.load(pathBackground + "plx-1.png").convert_alpha()
bg1_size = pygame.transform.scale(bg1, (800, 480))
bgScaleWidth1 = bg1_size.get_rect().width

# bg 2
bg2 = pygame.image.load(pathBackground + "plx-2.png").convert_alpha()
bg2_size = pygame.transform.scale(bg2, (800, 480))
bgScaleWidth2 = bg2_size.get_rect().width

# bg 3
bg3 = pygame.image.load(pathBackground + "plx-3.png").convert_alpha()
bg3_size = pygame.transform.scale(bg3, (800, 480))
bgScaleWidth3 = bg3_size.get_rect().width

# bg 4
bg4 = pygame.image.load(pathBackground + "plx-4.png").convert_alpha()
bg4_size = pygame.transform.scale(bg4, (800, 480))
bgScaleWidth4 = bg4_size.get_rect().width

# bg 5
bg5 = pygame.image.load(pathBackground + "plx-5.png").convert_alpha()
bg5_size = pygame.transform.scale(bg5, (800, 480))
bgScaleWidth5 = bg5_size.get_rect().width

# initialize for background scrolling
stageWidth = bgScaleWidth5 * 2

ground_height = HEIGHT - 50


class Player(pygame.sprite.Sprite):

    # TODO: alle Bilder aus einem Ordner laden
    """
    def load_images(self, path_to_directory):
        image_dict = {}
        self.myArray = []
        for filename in os.listdir(path_to_directory):
            if filename.endswith('.png'):
                pathdir = os.path.join(path_to_directory, filename)
                key = filename[:-4]
                image_dict[key] = pygame.image.load(pathdir).convert()
                self.myArray = np.asarray(image_dict)
        return self.myArray
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.mobs_index = 0

        # GIF Idle
        self.idle = []
        self.idle.append(pygame.image.load(pathPlayer + 'idle-png/idle-01.png').convert_alpha())
        self.idle.append(pygame.image.load(pathPlayer + 'idle-png/idle-02.png').convert_alpha())
        self.idle.append(pygame.image.load(pathPlayer + 'idle-png/idle-03.png').convert_alpha())
        self.idle.append(pygame.image.load(pathPlayer + 'idle-png/idle-04.png').convert_alpha())
        self.idle.append(pygame.image.load(pathPlayer + 'idle-png/idle-05.png').convert_alpha())
        self.idle.append(pygame.image.load(pathPlayer + 'idle-png/idle-06.png').convert_alpha())
        self.idle.append(pygame.image.load(pathPlayer + 'idle-png/idle-07.png').convert_alpha())
        self.idle.append(pygame.image.load(pathPlayer + 'idle-png/idle-08.png').convert_alpha())
        self.idle.append(pygame.image.load(pathPlayer + 'idle-png/idle-09.png').convert_alpha())
        self.idle.append(pygame.image.load(pathPlayer + 'idle-png/idle-10.png').convert_alpha())
        self.idle.append(pygame.image.load(pathPlayer + 'idle-png/idle-11.png').convert_alpha())
        self.idle.append(pygame.image.load(pathPlayer + 'idle-png/idle-12.png').convert_alpha())

        # GIF run
        self.run = []
        self.run.append(pygame.image.load(pathPlayer + 'run-png/run_00.png').convert_alpha())
        self.run.append(pygame.image.load(pathPlayer + 'run-png/run_01.png').convert_alpha())
        self.run.append(pygame.image.load(pathPlayer + 'run-png/run_02.png').convert_alpha())
        self.run.append(pygame.image.load(pathPlayer + 'run-png/run_03.png').convert_alpha())
        self.run.append(pygame.image.load(pathPlayer + 'run-png/run_04.png').convert_alpha())
        self.run.append(pygame.image.load(pathPlayer + 'run-png/run_05.png').convert_alpha())
        self.run.append(pygame.image.load(pathPlayer + 'run-png/run_06.png').convert_alpha())
        self.run.append(pygame.image.load(pathPlayer + 'run-png/run_07.png').convert_alpha())

        # index values for arrays
        self.arrayIndex = 0
        self.idleIndex = 0
        self.runIndex = 0

        # player  # TODO: get_width() von allen Arrays nehmen
        self.playerwidth = self.idle[self.arrayIndex].get_width()
        self.playerheight = self.idle[self.arrayIndex].get_height()
        self.HPH = int(round(self.playerheight / 2))  # float to int
        self.newHeight = pygame.transform.scale(self.idle[self.arrayIndex], (self.playerwidth, self.HPH))

        # rectangle
        self.rect = self.idle[self.arrayIndex].get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = ground_height
        self.speedy = 0
        self.x = 0
        self.playerposy = ground_height
        self.stagePosX = 0

    def play_gif(self, gif_array, gif_speed, image_flip):
        self.idleIndex += 1
        if self.idleIndex >= gif_speed:  # normale Geschw. = 1, halbe Geschw. = 2, doppelte Geschw. = 0.5
            self.arrayIndex += 1
            self.idleIndex = 0
        if self.arrayIndex >= len(gif_array):
            self.arrayIndex = 0
        self.image = pygame.transform.flip(gif_array[self.arrayIndex], image_flip, False)

    def update(self):
        self.speedy = 0

        key_state = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()

        self.key_left = key_state[pygame.K_LEFT] or mouse_pos < (HW, HEIGHT) and mouse_press == (1, 0, 0)
        self.key_right = key_state[pygame.K_RIGHT] or mouse_pos > (HW, HEIGHT) and mouse_press == (1, 0, 0)
        self.key_up = key_state[pygame.K_UP]

        # Key pressed: constant movement
        if self.key_left:
            self.play_gif(player.run, 3, True)
        elif self.key_right:
            self.play_gif(player.run, 3, False)
        elif key_state[pygame.K_DOWN]:
            # self.image = pygame.image.load(pathPlayer + "landing.png").convert_alpha()
            self.image = self.newHeight
            self.rect.bottom = self.playerposy + self.HPH
        else:
            self.play_gif(self.idle, 2, False)
            self.rect.bottom = self.playerposy

        # Key pressed: only one move
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.rect.bottom = self.playerposy - 50
                self.image = pygame.image.load(pathPlayer + "jump.png").convert_alpha()
            elif event.key == pygame.K_f or event.key == pygame.K_ESCAPE:
                if screen.get_flags() & pygame.FULLSCREEN:
                    pygame.display.set_mode((WIDTH, HEIGHT))
                else:
                    pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

        # Key release: only one move
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.rect.bottom = self.playerposy
        self.rect.y += self.speedy

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if self.rect.top < 0:
            self.rect.top = 0


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = obstacle
        self.obstacle_ypos = HEIGHT - ground_size.get_rect().height - obstacle_size.get_rect().height + 15

        # first obstacle
        self.rect = self.image.get_rect()
        self.rect.x = 600  # TODO: 800 ist momentan die einzig funktionierende Position für die Collision...
        self.rect.y = self.obstacle_ypos

        # second obstacle
        self.rect2 = self.image.get_rect()
        self.rect2.x = 1200

        # third obstacle
        self.rect3 = self.image.get_rect()
        self.rect3.x = 1600

        # add all x positions of the obstacles to the array
        self.all_mobs_x = []
        self.all_mobs_x.append(self.rect.x)
        self.all_mobs_x.append(self.rect2.x)
        self.all_mobs_x.append(self.rect3.x)


def allow_run_right():
    if player.key_right:
        player.stagePosX -= 8


def allow_run_left():
    if player.key_left:
        player.stagePosX += 8


def collision_detection():
    # check to see if mob hit the player
    # hits = pygame.sprite.spritecollide(player, mobs, False)
    # hits = pygame.sprite.collide_rect(player, mob)

    mob_posx = mob.all_mobs_x[player.mobs_index] + player.stagePosX
    # print("Block Position:", mob_posx)
    mob_posy = mob.rect.y
    mob_width = mob.image.get_rect().width

    playerposx = player.stagePosX * -1
    # print("Player Position:", playerposx)

    # player left of obstacle
    if playerposx <= mob_posx - 20:
        # print("if erfüllt:", playerposx, "kleiner als", mob_posx)
        allow_run_right()
        player.playerposy = ground_height
    # player on top of obstacle
    elif mob_posx + mob_width + 50 >= playerposx >= mob_posx - 20 and player.rect.y <= mob_posy:
        # print("elif erfüllt:", mob_posx + mob_width, "größer als", playerposx, "größer als", mob_posx)
        allow_run_right()
        allow_run_left()
        player.playerposy = mob_posy + 4
    # player right of obstacle
    elif playerposx >= mob_posx + mob_width + 50:
        # print("letzte elif:", playerposx, "größer als", mob_posx + mob_width)
        allow_run_left()
        player.playerposy = ground_height
        player.mobs_index += 1

        if player.mobs_index >= len(mob.all_mobs_x):
            player.mobs_index = 0
    # distance between player and obstacle
    if playerposx <= mob_posx:
        allow_run_left()
    elif playerposx >= mob_posx + mob_width + 40:
        allow_run_right()
    # print(playerposx)


def load_bg():
    # background
    rel_x = player.stagePosX % WIDTH
    rel_x_bg2 = player.stagePosX * 0.7 % WIDTH
    rel_x_bg3 = player.stagePosX * 0.8 % WIDTH
    rel_x_bg4 = player.stagePosX * 0.9 % WIDTH

    def bg_speed(bg_size, rel_pos):
        screen.blit(bg_size, (rel_pos - WIDTH, 0))
        if rel_pos < WIDTH:
            screen.blit(bg_size, (rel_pos, 0))

    bg_speed(bg1_size, rel_x)
    bg_speed(bg2_size, rel_x_bg2)
    bg_speed(bg3_size, rel_x_bg3)
    bg_speed(bg4_size, rel_x_bg4)
    bg_speed(bg5_size, rel_x)

    # ground
    rel_ground = player.stagePosX % ground_size.get_rect().width
    screen.blit(ground_size, (rel_ground - ground_size.get_rect().width, 420))
    if rel_ground < WIDTH:
        screen.blit(ground_size, (rel_ground, 420))


# sprite groups
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()

# classes
player = Player()
mob = Mob()

# add the sprites to groups
mobs.add(mob)
all_sprites.add(player)

# Game loop
running = True
while running:

    load_bg()

    def test_mob(mob_rect_x):
        if mob_rect_x <= WIDTH:
            dist_to_w = (WIDTH - mob_rect_x) / 2
        else:
            dist_to_w = (WIDTH - mob_rect_x) / 2
        return mob_rect_x + player.stagePosX + dist_to_w

    # draw all obstacles
    screen.blit(obstacle_size, (test_mob(mob.rect.x), mob.rect.y))
    screen.blit(obstacle_size, (test_mob(mob.rect2.x), mob.rect.y))
    screen.blit(obstacle_size, (test_mob(mob.rect3.x), mob.rect.y))
    # print("Render Block:", mob.rect.x + stagePosX)

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # check to see if mob hit the player
    collision_detection()

    # Draw / render
    all_sprites.draw(screen)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
