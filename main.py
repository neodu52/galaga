import pyxel
import time
import math
import random as rd
import music
import json
import os

music
x_ship = 80
y_ship = 60
vx_ship = 2     #vitesse horizontale
vy_ship = 2     #vitesse vertical
t_0 = time.time()
mode = "menu"
score = 0

data ={
  "a": {
    "x": score,
  },
}

with open('data.json', 'a') as f:
    f.write(json.dumps(data, ensure_ascii=False, indent=4))

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
    if pyxel.frame_count%15 == 0:
        enemies.append([rd.randint(0,160), 0])
    return enemies

def enemies_move(enemies):
    for ene in enemies:
        ene[1] += 3
        if ene[1] > 120:
            enemies.remove(ene)
    return enemies

def check_collisions(shoot, enemies, x_ship, y_ship):
    """fct pour gerer les colision avec les enemeies"""
    # sa c la collison tir avec enemie
    for tir in shoot:
        for ene in enemies:
            if abs(tir[0] - ene[0]) < 5 and abs(tir[1] - ene[1]) < 5:
                    shoot.remove(tir)
                    enemies.remove(ene)
    # se c la colision vaisseau avec enemie
    for ene in enemies:
        if abs(x_ship - ene[0]) < 5 and abs(y_ship - ene[1]) < 4 :
            mode = "gameover"
            return
    return shoot, enemies

def restart_game():
    global x_ship, y_ship, shoot, enemies, t_0, mode
    x_ship = 80
    y_ship = 60
    shoot = []
    enemies = []
    t_0 = time.time()
    mode = "game"

def update():
    global x_ship, y_ship, shoot, tim, enemies
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    if mode == "menu":
        if pyxel.btnp(pyxel.KEY_SPACE):
            restart_game()
        return

    if mode == "gameover":
        if pyxel.btnp(pyxel.KEY_R):
            restart_game()
        return

    x_ship, y_ship = ship_move(x_ship, y_ship)
    shoot = shoot_create(x_ship, y_ship, shoot)
    shoot = shoot_move(shoot)
    enemies = enemies_create(enemies)
    enemies = enemies_move(enemies)
    shoot, enemies = check_collisions(shoot, enemies, x_ship, y_ship)
    tim = round(time.time()-t_0, 1)

def pause():
    while pyxel.btnr(pyxel.GAMEPAD1_BUTTON_B) == 1:
        pyxel.quit()

def draw():
    pyxel.cls(0)
    if mode == "menu":
        pyxel.text(70, 40, "GALAGA", pyxel.frame_count % 11)
        pyxel.text(55, 70, "Space to play", 7)
        return

    if mode == "gameover":
        pyxel.text(40, 40, "GAME OVER", 8)
        pyxel.text(20, 70, "Appuie sur R pour recommencer", 7)
        return
    
    pyxel.blt(x_ship, y_ship, 0, 0, 0, 8, 8)
    for tir in shoot:
        pyxel.blt(tir[0], tir[1],0,10, 0, 3, 7)
        pyxel.blt(tir[0]+6, tir[1]-1,0,10, 0, 3, 7)
    pyxel.text(10, 10, str(round(time.time()-t_0, 1)), 11)
    for ene in enemies:
        pyxel.rect(ene[0], ene[1], 5, 5, 9)
    frame = print(pyxel.frame_count%30)

pyxel.run(update, draw)
