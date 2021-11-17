import numpy as np
import pygame as pg

width = 400
grid = np.zeros((width, width), 'bool')
accreted = np.zeros((width, width), 'bool')
# 1 dans grid = draw square
def spawn(qty, weirdmode):
    # for now particles can spawn in regions within the 'crystal'
    a, b, c, d = np.min(accreted.nonzero()[0]), np.max(accreted.nonzero()[0]), np.min(accreted.nonzero()[1]), np.max(accreted.nonzero()[1])
    if qty>0:
        qt1 = int(qty*(width*a)/(width**2))
        grid[(np.random.randint(0, a, qt1), np.random.randint(0, width, qt1))] = 1
        qt2 = int(qty*(width-b)*width/(width**2))
        grid[(np.random.randint(b, width, qt2), np.random.randint(0, width, qt2))] = 1
        if a!=b:
            qt3 = int(qty*(b-a)*c/(width**2))
            grid[(np.random.randint(a, b, qt3), np.random.randint(0, c, qt3))] = 1
            qt4 = int(qty*((b-a)*(width-d))/(width**2))
            grid[(np.random.randint(a, b, qt4), np.random.randint(d, width, qt4))] = 1
            if not weirdmode:
                density = 1/800
                qt5 = round(((b-a)*(d-c))*density)
                grid[(np.random.randint(a , b, qt5), np.random.randint(c, d, qt5))] = 1
    return

def check_neighbour(array_a, array_b, diagonal=True):
    #creating accretion sites array
    array_b_indexes = array_b.nonzero()
    if diagonal == True:
        displacements = np.array([(1,1), (1,-1), (-1,-1), (-1, 1), (1, 0), (-1, 0), (0, 1), (0, -1)])
    else:
        displacements = np.array([(1, 0), (-1, 0), (0, 1), (0, -1)])
    acc_sites = np.copy(array_b)
    for i in displacements:
        try:
            acc_sites[(array_b_indexes[0]+i[0], array_b_indexes[1]+i[1])] = 1
        except IndexError:
            pass
    #comparing the 2 arrays
    index1, index2 = (array_a & acc_sites).nonzero()
    return index1, index2

def move():
    x, y = grid.nonzero()
    grid[(x, y)] = 0 #remove the particles
    #move the particles
    x += np.random.randint(-1, 2, x.size) 
    y += np.random.randint(-1, 2, y.size)
    #just so the particles don't escape the screen
    x[x<0]+=1
    x[x>width-1]-=1
    y[y<0]+=1
    y[y>width-1]-=1
    grid[(x, y)] = 1 #place them in their new position
    return 

def accrete(diagonal):

    #updating positions
    index = check_neighbour(grid, accreted, diagonal=diagonal)
    grid[index] = 0
    accreted[index] = 1
    return

def redrawWindow(win, n):
    win.fill((0, 0, 0))
    for i,j in zip(grid.nonzero()[0], grid.nonzero()[1]):
        pg.draw.rect(win, 'seagreen', [n*i, n*j, n, n])
    for i,j in zip(accreted.nonzero()[0], accreted.nonzero()[1]):
        pg.draw.rect(win, 'white', [n*i, n*j, n, n])
    pg.display.update()
    return


def main(qty,scale=1, diagonal = True, weirdmode = False, roundfactor = 15):
    global win
    win = pg.display.set_mode((scale*width, scale*width))
    clock = pg.time.Clock()
    spawn(qty, weirdmode)

    while True:
        # pygame.time.delay(5)
        move()
        spawn(qty - (grid.nonzero()[0].size + accreted.nonzero()[0].size), weirdmode)
        accrete(diagonal)
        redrawWindow(win, scale)
        pg.display.set_caption(f'{clock.get_fps():.2f} {grid.nonzero()[0].size} {accreted.nonzero()[0].size}')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        clock.tick()

#Stem to start accretion, change it if you want
# accreted[np.arange(1, width-1),width-1] = 1
accreted[round(width/2), round(width/2)] = 1
# accreted[100, 100] = 1
# accreted[150,150] = 1

#first argument is the quantity of particles, it remains contant throughout the simulation
main(20000, scale=2)