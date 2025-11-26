import pyxel
import time
import math
import random as rd
import music
import json
import os

x_ship = 80
y_ship = 60
vx_ship = 2     #vitesse horizontale
vy_ship = 2     #vitesse vertical
t_0 = time.time()
mode = "menu"
score = 0
highscore = 0
slow_active = False
slow_start_time = 0
last_slow_spawn = 0
slow_item = None 

def load_highscore():
    global highscore
    if os.path.exists("score.json"):
        with open("score.json", "r") as f:
            data = json.load(f)
            highscore = data.get("highscore", 0)
    else:
        highscore = 0
        
def spawn_slow_item():
    global slow_item, last_slow_spawn

    if time.time() - last_slow_spawn > 20:
        slow_item = [rd.randint(10, 150), rd.randint(10, 110)]
        last_slow_spawn = time.time()

def save_highscore():
    global highscore
    with open("score.json", "w") as f:
        json.dump({"highscore": highscore}, f, indent=4)

shoot = []
enemies = []

pyxel.init(160,120, title="Galaga")
pyxel.load("star_ship.pyxres")

def ship_move(x_ship, y_ship):
    speed_factor = 0.5 if slow_active else 1

    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
        x_ship += vx_ship * speed_factor
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
        x_ship -= vx_ship * speed_factor
    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
        y_ship -= vy_ship * speed_factor
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
        y_ship += vy_ship * speed_factor

    return x_ship, y_ship

def shoot_create(x,y, shoot):
    if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_A):
        shoot.append([x-1,y-1])
    return shoot

def shoot_move(shoot):
    speed_factor = 0.5 if slow_active else 1

    for tir in shoot[:]:
        tir[1] -= 3 * speed_factor
        if tir[1] < -8:
            shoot.remove(tir)
    return shoot

def enemies_create(enemies):
    if pyxel.frame_count%15 == 0:
        enemies.append([rd.randint(0,160), 0])
    return enemies

def enemies_move(enemies):
    speed_factor = 0.5 if slow_active else 1

    for ene in enemies[:]:
        ene[1] += 3 * speed_factor
        if ene[1] > 120:
            enemies.remove(ene)
    return enemies


def slow_motion_start():
    global slow_active, slow_start_time
    slow_active = True
    slow_start_time = time.time()


def check_collisions(shoot, enemies, x_ship, y_ship):
    """fct pour gerer les colision avec les enemeies"""
    global mode, score, highscore
    # sa c la collison tir avec enemie
    for tir in shoot:
        for ene in enemies:
            if abs(tir[0] - ene[0]) < 5 and abs(tir[1] - ene[1]) < 5:
                    shoot.remove(tir)
                    enemies.remove(ene)
                    score += 100

                    if score > highscore:
                        highscore = score
                        save_highscore()
    # se c la colision vaisseau avec enemie
    for ene in enemies:
        if abs(x_ship - ene[0]) < 5 and abs(y_ship - ene[1]) < 4 :
            mode = "gameover"
            
    return shoot, enemies

def restart_game():
    global x_ship, y_ship, shoot, enemies, t_0, mode, score
    x_ship = 80
    y_ship = 60
    shoot = []
    enemies = []
    t_0 = time.time()
    mode = "game"
    score = 0

def update():
    global x_ship, y_ship, shoot, tim, enemies
    global slow_item, slow_active, slow_start_time, last_slow_spawn, mode, score
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    if mode == "menu":
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            restart_game()
        return

    if mode == "gameover":
        if pyxel.btnp(pyxel.KEY_R) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            restart_game()
        return

    x_ship, y_ship = ship_move(x_ship, y_ship)
    shoot = shoot_create(x_ship, y_ship, shoot)
    shoot = shoot_move(shoot)
    enemies = enemies_create(enemies)
    enemies = enemies_move(enemies)
    shoot, enemies = check_collisions(shoot, enemies, x_ship, y_ship)
    spawn_slow_item()

    if slow_item is not None:
        if abs(x_ship - slow_item[0]) < 8 and abs(y_ship - slow_item[1]) < 8:
            slow_motion_start()
            slow_item = None
    if slow_active and time.time() - slow_start_time > 10:
        slow_active = False
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
        pyxel.text(62, 40, "GAME OVER", 8)
        pyxel.text(25, 70, "Appuie sur R pour recommencer", 7)
        pyxel.text(20, 90, f"Highscore : {highscore}", 10)
        return
    if slow_item is not None:
        pyxel.circ(slow_item[0], slow_item[1], 4, 8)
    if slow_active:
        pyxel.text(60, 5, "SLOW-MO !", 7)

    pyxel.blt(x_ship, y_ship, 0, 0, 0, 8, 8)
    for tir in shoot:
        pyxel.blt(tir[0], tir[1],0,10, 0, 3, 7)
        pyxel.blt(tir[0]+6, tir[1]-1,0,10, 0, 3, 7)
    pyxel.text(10, 10, str(round(time.time()-t_0, 1)), 11)
    pyxel.text(30, 10, f"Score: {score}", 11)
    pyxel.text(10, 20, f"Highscore: {highscore}", 10)
    for ene in enemies:
        pyxel.rect(ene[0], ene[1], 5, 5, 9)
    frame = print(pyxel.frame_count%30)

load_highscore()
pyxel.run(update, draw)