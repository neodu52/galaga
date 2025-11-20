import pyxel
import time
import math
import random as rd

x_ship = 80
y_ship = 60
vx_ship = 2     #vitesse horizontale
vy_ship = 2     #vitesse vertical
t_0 = time.time()

shoot = []
enemies = []

pyxel.init(160,120, title="Galaga")
pyxel.load("star_ship.pyxres")

def ship_move(x_ship, y_ship):

    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
        x_ship += vx_ship
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
        x_ship -= vx_ship
    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
        y_ship -= vy_ship
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
        y_ship += vy_ship
    if pyxel.btnr(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnr(pyxel.KEY_KP_ENTER):
        pause()
    return x_ship, y_ship

def shoot_create(x,y, shoot):
    if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_A):
        shoot.append([x-1,y-1])
    return shoot

def shoot_move(shoot):
    global tir
    for tir in shoot:
        tir[1] -= 3
        if tir[1] < -8:
            shoot.remove(tir)
    return shoot

def enemies_create(enemies):
    if pyxel.frame_count%10 == 0:
        enemies.append([rd.randint(0,160), 0])
    return enemies

def enemies_move(enemies):
    for ene in enemies:
        ene[1] += 3
        if ene[1] > 120:
            enemies.remove(ene)
    return enemies

def update():
    global x_ship, y_ship, shoot, tim, enemies
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    x_ship, y_ship = ship_move(x_ship, y_ship)
    shoot = shoot_create(x_ship, y_ship, shoot)
    shoot = shoot_move(shoot)
    enemies = enemies_create(enemies)
    enemies = enemies_move(enemies)
    tim = round(time.time()-t_0, 1)

def pause():
    while pyxel.btnr(pyxel.GAMEPAD1_BUTTON_B) == 1:
        time.sleep()

def draw():
    pyxel.cls(0)
    pyxel.blt(x_ship, y_ship, 0, 0, 0, 8, 8)
    for tir in shoot:
        pyxel.blt(tir[0], tir[1],0,10, 0, 3, 7)
        pyxel.blt(tir[0]+6, tir[1]-1,0,10, 0, 3, 7)
    pyxel.text(10, 10, str(tim), 11)
    for ene in enemies:
        pyxel.rect(ene[0], ene[1], 5, 5, 9)
    frame = print(pyxel.frame_count%30)

pyxel.run(update, draw)
