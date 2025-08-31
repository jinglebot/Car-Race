import pygame
import time
import math
from utils import scale_img, blit_rotate_center

GRASS = scale_img(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_img(pygame.image.load("imgs/track.png"), 0.9)

TRACK_BORDER = scale_img(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POS = (130, 250)

RED_CAR = scale_img(pygame.image.load("imgs/red-car.png"), 0.55)
GREEN_CAR = scale_img(pygame.image.load("imgs/green-car.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WACKY RACERS")

clock = pygame.time.Clock()

FPS = 60
PATH = []

class AbstractCar:
    def _init_(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.rotation_vel = rotation_vel
        self.vel = 0
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        if right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180,200)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration/2,0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)

    def _init_(self, max_vel, rotation_vel, path[]):
        super()._init_(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255,0,0), point, 5)

    def draw(self, win):
        super().draw(win)
        self.draw_points(win)

def draw(win,imgs, player_car, computer_car):
    for img,pos in imgs:
        win.blit(img, pos)
    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()

run = True
while run:
    clock.tick(FPS)
    images = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH, FINISH_POS), (TRACK_BORDER, (0,0))]
    player_car = PlayerCar(4,4)
    computer_car = ComputerCar(4,4, PATH)

    draw(WIN, images, player_car, computer_car)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

#        if event.type == pygame.MOUSEBUTTONDOWN:
#            pos = pygame.mouse.get_pos()
#            computer_car.path.append(pos)

    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left= True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POS)
    if finish_poi_collide != None:
        if finish_poi_collide == 0:
            player_car.bounce()
        else:
            player_car.reset()
            print("finish")
    

print(computer_car.path)
pygame.quit()