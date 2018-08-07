import sys, pygame
import gamestate as gs
import random

pygame.init()

size = width, height = 800, 500
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

wolf = pygame.image.load("wolf.png")
wolfrect = wolf.get_rect()

sheep = pygame.image.load("sheep.png")
sheeprect = sheep.get_rect()

ticks = pygame.time.get_ticks()

clck = pygame.time.Clock()

font = pygame.font.SysFont("Monospaced", 39)
name = 'Dilli'
print('Hallo %s' % name)

state = gs.START

block_size = 50
w, h = 10, 10
field = [[0 for x in range(w)] for y in range(h)]

field[0][0] = 1

sheep_pos = [0, 0]
wolf_pos = [8, 8]
color_grass = (0, 128, 0)
color_soil = (118, 47, 50)


def reset():
    global sheep_pos
    global wolf_pos
    global field
    sheep_pos = [0, 0]
    wolf_pos = [8, 8]
    field = [[0 for x in range(w)] for y in range(h)]


def draw_field():
    for y in range(h):
        for x in range(w):
            rect = pygame.Rect((x*block_size)+3, (y*block_size)+3, 47, 47)
            col = color_grass
            if field[x][y] == 1:
                col = color_soil
            pygame.draw.rect(screen, col,  rect, 0)


def draw_sheep():
    rect = pygame.Rect((sheep_pos[0] * block_size) + 3, (sheep_pos[1] * block_size) + 3, 47, 47)
    pygame.draw.rect(screen, (200, 200, 200), rect, 0)
    screen.blit(sheep, rect)


def move_sheep(direction):
    global sheep_pos
    if direction == 'right':
        if sheep_pos[0] < w - 1:
            sheep_pos = (sheep_pos[0]+1, sheep_pos[1])
    if direction == 'left':
        if sheep_pos[0] > 0:
            sheep_pos = (sheep_pos[0]-1, sheep_pos[1])
    if direction == 'down':
        if sheep_pos[1] < h - 1:
            sheep_pos = (sheep_pos[0], sheep_pos[1]+1)
    if direction == 'up':
        if sheep_pos[1] > 0:
            sheep_pos = (sheep_pos[0], sheep_pos[1]-1)


def draw_wolf():
    rect = pygame.Rect((wolf_pos[0] * block_size) + 3, (wolf_pos[1] * block_size) + 3, 47, 47)
    pygame.draw.rect(screen, (50, 50, 50), rect, 0)
    rect.left += 10
    screen.blit(wolf, rect)


def move_wolf():
    global wolf_pos, w, h
    move_x = random.randint(-1, 1)
    move_y = random.randint(-1, 1)
    wolf_pos = [wolf_pos[0] + move_x, wolf_pos[1] + move_y]
    if wolf_pos[0] < 0:
        wolf_pos[0] = 0
    if wolf_pos[0] >= w:
        wolf_pos[0] = w-1
    if wolf_pos[1] < 0:
        wolf_pos[1] = 0
    if wolf_pos[1] >= h:
        wolf_pos[1] = h-1

def update():
    field[sheep_pos[0]][sheep_pos[1]] = 1


def show_speed():
    global text
    x = abs(speed[0])
    font = pygame.font.SysFont("Monospaced", 39)
    text = font.render(" speed: %i" % x, True, (128, 0, 0))


def draw_grass():
    rect = pygame.Rect(3, 3, 50, 50)
    pygame.draw.rect(screen, (0, 128, 0),  rect, 0)

def get_remaining_grass():
    result = 0
    for y in range(h):
        for x in range(w):
            if field[x][y] == 0:
                result += 1
    return result


def draw_status():
    font = pygame.font.SysFont("Monospaced", 50)
    text = font.render("Sheep!", True, (128, 128, 128))
    screen.blit(text, (580, 40))

    font = pygame.font.SysFont("Monospaced", 39)
    text = font.render("Grass: %i" % get_remaining_grass(), True, (128, 128, 128))
    screen.blit(text, (580, 100))


def beschleunige():
    if speed[0]<0:
        speed[0] = speed[0]-1
    if speed[0]>0:
        speed[0] = speed[0]+1
    if speed[1]<0:
        speed[1] = speed[1]-1
    if speed[1]>0:
        speed[1] = speed[1]+1

    show_speed()


pygame.display.set_caption('Sheep!')
#show_speed()
draw_grass()

reset()

while True:
    clck.tick(40)
    # print("%s ticks: %i" % (state, ticks))
    for event in pygame.event.get():
        # print('event: ', event)
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            print('KEYDOWN event.unicode = %s' % event.unicode)
            # print('KEYDOWN pygame.K_q = %s' % pygame.K_q)
            if event.key == pygame.K_q:
                print('Q')
                sys.exit()
            if event.key == pygame.K_p:
                print('PAUSE')
                if state == gs.RUNNING:
                    state = gs.PAUSE
                else:
                    if state == gs.PAUSE:
                        state = gs.RUNNING
            if event.key == pygame.K_LEFT:
                print('LEFT')
                if state == gs.RUNNING:
                    move_sheep('left')
            if event.key == pygame.K_RIGHT:
                print('RIGHT')
                if state == gs.RUNNING:
                    move_sheep('right')
            if event.key == pygame.K_UP:
                print('UP')
                if state == gs.RUNNING:
                    move_sheep('up')
            if event.key == pygame.K_DOWN:
                print('DOWN')
                if state == gs.RUNNING:
                    move_sheep('down')
            if event.key == pygame.K_RETURN:
                print('RETURN')
                if state == gs.START:
                    reset()
                    state = gs.RUNNING
                if state == gs.LOST or state == gs.WON:
                    state = gs.START
                if state == gs.PAUSE:
                    state = gs.RUNNING

    #if pygame.time.get_ticks() - ticks > 50:
    #ballrect = ballrect.move(speed)
    #    ticks = pygame.time.get_ticks()
    #if ballrect.left <= 0 or ballrect.right >= width:
    #    beschleunige()
    #    speed[0] = -speed[0]
    #if ballrect.top <= 0 or ballrect.bottom >= height:
    #    beschleunige()
    #    speed[1] = -speed[1]

    screen.fill(black)
    #screen.blit(ball, ballrect)
    #screen.blit(text, (320 - text.get_width() // 2, 240 - text.get_height() // 2))
    #screen.blit(text, (0, 0))
    #drawGrass()

    draw_field()
    draw_sheep()
    draw_wolf()
    draw_status()

    if state == gs.RUNNING:
        if pygame.time.get_ticks() - ticks > 240:
            move_wolf()
            ticks = pygame.time.get_ticks()

        update()
        if wolf_pos[0] == sheep_pos[0] and wolf_pos[1] == sheep_pos[1]:
            print('WOLF WINS')
            state = gs.LOST

        gras_found = False
        for y in range(h):
            for x in range(w):
                if field[x][y] == 0:
                    #print('not finished')
                    gras_found = True
                    break
        if not gras_found:
            print('YOU WIN!')
            state = gs.WON
    if state == gs.START:

        rect = pygame.Rect(503, 220, 550, 250)
        pygame.draw.rect(screen, (200, 200, 200), rect, 0)

        font = pygame.font.SysFont("Monospaced", 25)
        text = font.render("Du bist ein Schaf!", True, (128, 0, 0))
        screen.blit(text, (510, 240))
        text = font.render("Also benimm dich auch so!", True, (128, 0, 0))
        screen.blit(text, (510, 270))
        text = font.render("Lauf los und friss Gras, und zwar alles!", True, (128, 0, 0))
        screen.blit(text, (510, 300))
        text = font.render("Aber pass auf den Wolf auf!", True, (128, 0, 0))
        screen.blit(text, (510, 330))

        rect = pygame.Rect(530, 380, 150, 60)
        pygame.draw.rect(screen, color_grass, rect, 0)
        pygame.draw.rect(screen, color_soil, rect, 10)
        text = font.render("Määähh!", True, (0, 0, 0))
        screen.blit(text, (560, 400))

    if state == gs.LOST:

        rect = pygame.Rect(200, 220, 550, 250)
        pygame.draw.rect(screen, (200, 200, 200), rect, 0)

        font = pygame.font.SysFont("Monospaced", 39)
        text = font.render("Der Wolf hat dich erwischt!", True, (128, 0, 0))
        screen.blit(text, (220, 270))

        rect = pygame.Rect(270, 380, 150, 70)
        pygame.draw.rect(screen, (128, 0, 0), rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), rect, 10)
        text = font.render("Mäh :-(", True, (0, 0, 0))
        screen.blit(text, (290, 400))

    if state == gs.WON:

        rect = pygame.Rect(200, 220, 550, 250)
        pygame.draw.rect(screen, (200, 200, 200), rect, 0)

        font = pygame.font.SysFont("Monospaced", 39)
        text = font.render("Du hast den Wolf ausgetrickst!", True, (128, 0, 0))
        screen.blit(text, (220, 270))
        text = font.render("Gutes Schaf!", True, (128, 0, 0))
        screen.blit(text, (220, 300))

        rect = pygame.Rect(270, 380, 150, 70)
        pygame.draw.rect(screen, (128, 0, 0), rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), rect, 10)
        text = font.render("Mäh :-)", True, (0, 0, 0))
        screen.blit(text, (290, 400))

    if state == gs.PAUSE:

        rect = pygame.Rect(200, 220, 550, 250)
        pygame.draw.rect(screen, (200, 200, 200), rect, 0)

        font = pygame.font.SysFont("Monospaced", 39)
        text = font.render("Du kannst dich ausruhen!", True, (128, 0, 0))
        screen.blit(text, (220, 270))
        text = font.render("Aber der Wolf auch!", True, (128, 0, 0))
        screen.blit(text, (220, 300))

        rect = pygame.Rect(270, 380, 150, 70)
        pygame.draw.rect(screen, (128, 0, 0), rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), rect, 10)
        text = font.render("Mäh", True, (0, 0, 0))
        screen.blit(text, (290, 400))

    pygame.display.flip()

