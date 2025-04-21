from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import random

# Global Game State
player_pos = [0.0, 1.0, 0.0]
gun_angle = 0.0
bullets = []
enemies = []
score = 0
lives = 5
missed_bullets = 0
cheat_mode = False
first_person = False
camera_height = 5.0
camera_angle = 45.0
game_over = False

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    reset_game()

def draw_grid():
    glColor3f(0.4, 0.4, 0.4)
    glBegin(GL_LINES)
    for i in range(-10, 11):
        glVertex3f(i, 0, -10)
        glVertex3f(i, 0, 10)
        glVertex3f(-10, 0, i)
        glVertex3f(10, 0, i)
    glEnd()

    # Walls
    glColor3f(0.2, 0.2, 0.2)
    for x in [-10, 10]:
        glPushMatrix()
        glTranslatef(x, 1.5, 0)
        glScalef(0.1, 3, 20)
        glutSolidCube(1)
        glPopMatrix()
    for z in [-10, 10]:
        glPushMatrix()
        glTranslatef(0, 1.5, z)
        glScalef(20, 3, 0.1)
        glutSolidCube(1)
        glPopMatrix()

def draw_player():
    glPushMatrix()
    glTranslatef(*player_pos)
    glRotatef(gun_angle, 0, 1, 0)
    if game_over:
        glRotatef(90, 0, 0, 1)

    # Torso
    glColor3f(0.0, 0.0, 1.0)
    glPushMatrix()
    glScalef(0.8, 1.2, 0.4)
    glutSolidSphere(0.5, 20, 20)
    glPopMatrix()

    # Head
    glColor3f(1.0, 0.8, 0.6)
    glPushMatrix()
    glTranslatef(0, 0.9, 0)
    glutSolidSphere(0.25, 20, 20)
    glPopMatrix()

    # Left Arm
    glColor3f(1.0, 0.8, 0.6)
    glPushMatrix()
    glTranslatef(-0.6, 0.4, 0)
    glRotatef(90, 0, 0, 1)
    glutSolidCylinder(0.1, 0.5, 20, 20)
    glPopMatrix()

    # Right Arm
    glPushMatrix()
    glTranslatef(0.6, 0.4, 0)
    glRotatef(-90, 0, 0, 1)
    glutSolidCylinder(0.1, 0.5, 20, 20)
    glPopMatrix()

    # Gun
    glColor3f(0.4, 0.4, 0.4)
    glPushMatrix()
    glTranslatef(0.9, 0.4, 0)
    glScalef(1.0, 0.2, 0.2)
    glutSolidCube(0.5)
    glPopMatrix()

    glPopMatrix()

def draw_enemy(pos, scale):
    glPushMatrix()
    glTranslatef(*pos)
    glScalef(scale, scale, scale)

    glColor3f(1, 0, 0)
    glutSolidSphere(0.5, 20, 20)

    glPushMatrix()
    glTranslatef(0, 0.7, 0)
    glutSolidSphere(0.3, 20, 20)
    glPopMatrix()

    glPopMatrix()

def draw_bullet(pos):
    glPushMatrix()
    glTranslatef(*pos)
    glColor3f(1, 1, 0)
    glutSolidCube(0.2)
    glPopMatrix()

def update_camera():
    glLoadIdentity()
    if first_person:
        dx = math.sin(math.radians(gun_angle))
        dz = math.cos(math.radians(gun_angle))
        eye = [player_pos[0] - dx, player_pos[1] + 1.5, player_pos[2] - dz]
        center = [player_pos[0] + dx, player_pos[1] + 1.0, player_pos[2] + dz]
        gluLookAt(*eye, *center, 0, 1, 0)
    else:
        x = 10 * math.sin(math.radians(camera_angle))
        z = 10 * math.cos(math.radians(camera_angle))
        gluLookAt(x, camera_height, z, 0, 0, 0, 0, 1, 0)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    update_camera()
    draw_grid()
    draw_player()

    for enemy in enemies:
        draw_enemy(enemy['pos'], enemy['scale'])

    for bullet in bullets:
        draw_bullet(bullet['pos'])

    glColor3f(1, 1, 1)
    glWindowPos2i(10, 580)
    status = f"Lives: {lives} Score: {score}  Missed: {missed_bullets}"
    if game_over:
        status += "   [GAME OVER]"
    for ch in status:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    glutSwapBuffers()

def update_game(value):
    global lives, missed_bullets, score, gun_angle, game_over

    if game_over:
        glutPostRedisplay()
        glutTimerFunc(16, update_game, 0)
        return

    for enemy in enemies:
        dx = player_pos[0] - enemy['pos'][0]
        dz = player_pos[2] - enemy['pos'][2]
        dist = math.hypot(dx, dz)
        if dist > 0.01:
            enemy['pos'][0] += dx / dist * 0.01
            enemy['pos'][2] += dz / dist * 0.01


        enemy['scale'] += enemy['scale_dir'] * 0.02
        if enemy['scale'] > 1.2 or enemy['scale'] < 0.8:
            enemy['scale_dir'] *= -1

        if dist < 1.0:
            lives -= 1
            if lives <= 0:
                game_over = True
                print("Game Over: Player ran out of lives.")
            enemy['pos'] = [random.uniform(-9, 9), 1.0, random.uniform(-9, 9)]

    for bullet in bullets[:]:
        bullet['pos'][0] += bullet['vel'][0]
        bullet['pos'][2] += bullet['vel'][2]
        if abs(bullet['pos'][0]) > 10 or abs(bullet['pos'][2]) > 10:
            bullets.remove(bullet)
            missed_bullets += 1
            if missed_bullets >= 10:
                game_over = True
                print("Game Over: 10 bullets were missed.")
            continue

        for enemy in enemies[:]:
            dx = bullet['pos'][0] - enemy['pos'][0]
            dz = bullet['pos'][2] - enemy['pos'][2]
            if math.hypot(dx, dz) < 0.8:
                enemies.remove(enemy)
                enemies.append({
                    'pos': [random.uniform(-9, 9), 1.0, random.uniform(-9, 9)],
                    'scale': 1.0,
                    'scale_dir': 0.1
                })
                bullets.remove(bullet)
                score += 10
                break

    if cheat_mode:
        gun_angle += 2.0
        if gun_angle >= 360:
            gun_angle -= 360

        for enemy in enemies:
            dx = enemy['pos'][0] - player_pos[0]
            dz = enemy['pos'][2] - player_pos[2]
            angle_to_enemy = math.degrees(math.atan2(dx, dz))
            if abs(angle_to_enemy - gun_angle) < 5:
                fire_bullet()

    glutPostRedisplay()
    glutTimerFunc(16, update_game, 0)

def fire_bullet():
    if game_over:
        return
    speed = 0.3
    rad = math.radians(gun_angle)
    bullets.append({
        'pos': [player_pos[0], player_pos[1] + 0.5, player_pos[2]],
        'vel': [math.sin(rad) * speed, 0.0, math.cos(rad) * speed]
    })

def keyboard(key, x, y):
    global gun_angle, player_pos, cheat_mode, first_person, game_over

    key = key.decode('utf-8').lower()
    rad = math.radians(gun_angle)
    speed = 0.2

    if key == 'w':
        player_pos[0] += math.sin(rad) * speed
        player_pos[2] += math.cos(rad) * speed
    elif key == 's':
        player_pos[0] -= math.sin(rad) * speed
        player_pos[2] -= math.cos(rad) * speed
    elif key == 'a':
        gun_angle -= 3.0
    elif key == 'd':
        gun_angle += 3.0
    elif key == 'c':
        cheat_mode = not cheat_mode
    elif key == 'v' and cheat_mode:
        first_person = not first_person
    elif key == 'r':
        reset_game()

    glutPostRedisplay()

def special_keys(key, x, y):
    global camera_height, camera_angle

    if key == GLUT_KEY_UP:
        camera_height += 0.5
    elif key == GLUT_KEY_DOWN:
        camera_height = max(1.0, camera_height - 0.5)
    elif key == GLUT_KEY_LEFT:
        camera_angle -= 3.0
    elif key == GLUT_KEY_RIGHT:
        camera_angle += 3.0

    glutPostRedisplay()

def mouse(button, state, x, y):
    global first_person
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person
        glutPostRedisplay()

def reset_game():
    global player_pos, gun_angle, bullets, enemies, score, lives, missed_bullets, game_over
    player_pos = [0.0, 1.0, 0.0]
    gun_angle = 0.0
    bullets = []
    enemies = []
    score = 0
    lives = 5
    missed_bullets = 0
    game_over = False
    for _ in range(5):
        enemies.append({
            'pos': [random.uniform(-9, 9), 1.0, random.uniform(-9, 9)],
            'scale': 1.0,
            'scale_dir': 0.1
        })

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Bullet Frenzy")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutMouseFunc(mouse)
    glutTimerFunc(0, update_game, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
