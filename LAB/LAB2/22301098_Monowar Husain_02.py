from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time
import sys


WIDTH, HEIGHT = 500, 600
DIAMOND_SIZE = 20
CATCHER_WIDTH, CATCHER_HEIGHT = 100, 30
BUTTON_WIDTH, BUTTON_HEIGHT = 80, 40
DIAMOND_DROP_RANGE = (5, 495)
INITIAL_FALL_SPEED = 2.0
MAX_FALL_SPEED = 15.0
ACCELERATION = 0.01
LINE_WIDTH = 3  #visibility r jonno line width increase


game_state = 'run'  # 'run', 'thambo', 'game_over'
score = 0
catcher_x = WIDTH // 2
catcher_color = (1.0, 1.0, 1.0)  # White
diamond_y = 500
diamond_x = random.randint(*DIAMOND_DROP_RANGE)

diamond_color = (
    random.uniform(0.5, 1.0),
    random.uniform(0.5, 1.0),
    random.uniform(0.5, 1.0)
)
fall_speed = INITIAL_FALL_SPEED
last_frame_time = time.time()

#click button
click_RESTART = (20, HEIGHT - BUTTON_HEIGHT - 20)
click_PLAYPAUSE = (WIDTH//2 - BUTTON_WIDTH//2, HEIGHT - BUTTON_HEIGHT - 20)
click_QUIT = (WIDTH - BUTTON_WIDTH - 20, HEIGHT - BUTTON_HEIGHT - 20)

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    glLineWidth(LINE_WIDTH)  #line width
 
#mpl 8 way
def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0: return 0
        elif dx <= 0 and dy >= 0: return 3
        elif dx <= 0 and dy <= 0: return 4
        elif dx >= 0 and dy <= 0: return 7
    else:
        if dx >= 0 and dy >= 0: return 1
        elif dx <= 0 and dy >= 0: return 2
        elif dx <= 0 and dy <= 0: return 5
        elif dx >= 0 and dy <= 0: return 6

def convert_to_zone0(x, y, zone):
    if zone == 0: return (x, y)
    elif zone == 1: return (y, x)
    elif zone == 2: return (y, -x)
    elif zone == 3: return (-x, y)
    elif zone == 4: return (-x, -y)
    elif zone == 5: return (-y, -x)
    elif zone == 6: return (-y, x)
    elif zone == 7: return (x, -y)

def convert_from_zone0(x, y, zone):
    if zone == 0: return (x, y)
    elif zone == 1: return (y, x)
    elif zone == 2: return (-y, x)
    elif zone == 3: return (-x, y)
    elif zone == 4: return (-x, -y)
    elif zone == 5: return (-y, -x)
    elif zone == 6: return (y, -x)
    elif zone == 7: return (x, -y)

def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()

def draw_line_midpoint(x1, y1, x2, y2):

    zone = find_zone(x1, y1, x2, y2)  #zone find
    x1_conv, y1_conv = convert_to_zone0(x1, y1, zone)
    x2_conv, y2_conv = convert_to_zone0(x2, y2, zone)
    
   
    if x1_conv > x2_conv:
        x1_conv, x2_conv = x2_conv, x1_conv
        y1_conv, y2_conv = y2_conv, y1_conv
    
    #MPL zone 0
    dx = x2_conv - x1_conv
    dy = y2_conv - y1_conv
    d = 2 * dy - dx
    delE = 2 * dy
    delNE = 2 * (dy - dx)
    x, y = x1_conv, y1_conv
    
    while x <= x2_conv:
    
        orig_x, orig_y = convert_from_zone0(x, y, zone)
        draw_pixel(orig_x, orig_y)
        
        if d > 0:
            d += delNE
            y += 1
        else:
            d += delE
        x += 1

def draw_thick_line(x1, y1, x2, y2):  #multiple paralel line for visibility

    for i in range(LINE_WIDTH):
        offset = i - LINE_WIDTH//2
        draw_line_midpoint(x1, y1 + offset, x2, y2 + offset)
        draw_line_midpoint(x1 + offset, y1, x2 + offset, y2)

def draw_diamond(x, y, size, color):  #diamond
    
    glColor3f(*color)
    half_size = size // 2
    
    #convert int
    x, y = int(x), int(y)
    half_size = int(half_size)
    
    #top to right
    draw_thick_line(x, y + half_size, x + half_size, y)
    #right to bottom
    draw_thick_line(x + half_size, y, x, y - half_size)
    #bottom to left
    draw_thick_line(x, y - half_size, x - half_size, y)
    #left to top
    draw_thick_line(x - half_size, y, x, y + half_size)



def draw_catcher(x, width, height, color):

    glColor3f(*color)
    half_width = width // 2
    half_height = height // 2
    top_width = int(width * 0.8)  #bowl shape

    
    x = int(x)
    half_width = int(half_width)
    half_height = int(half_height)
    top_width = int(top_width)

    #swap the trapezoid's orientation:

    #wider top line
    draw_thick_line(x - half_width, half_height, x + half_width, half_height)
    #right 
    draw_thick_line(x + half_width, half_height, x + top_width // 2, -half_height)
    #bottom 
    draw_thick_line(x + top_width // 2, -half_height, x - top_width // 2, -half_height)
    #left side 
    draw_thick_line(x - top_width // 2, -half_height, x - half_width, half_height)


def draw_restart_button(x, y, width, height):

    #left arrow
    glColor3f(0.0, 1.0, 1.0)
    center_x, center_y = x + width//2, y + height//2
    arrow_size = min(width, height) // 2
    
    #line
    draw_thick_line(center_x - arrow_size//2, center_y, 
                   center_x + arrow_size//2, center_y)
    #head
    draw_thick_line(center_x - arrow_size//2, center_y,
                   center_x - arrow_size//2 + arrow_size//3, center_y - arrow_size//3)
    draw_thick_line(center_x - arrow_size//2, center_y,
                   center_x - arrow_size//2 + arrow_size//3, center_y + arrow_size//3)

def draw_playpause_button(x, y, width, height):  #run/thambo

    
    glColor3f(1.0, 0.75, 0.0)
    center_x, center_y = x + width//2, y + height//2
    symbol_size = min(width, height) // 2
    
    if game_state == 'run':
        #double bar
        draw_thick_line(center_x - symbol_size, center_y - symbol_size,
                       center_x - symbol_size, center_y + symbol_size)
        draw_thick_line(center_x + symbol_size, center_y - symbol_size,
                       center_x + symbol_size, center_y + symbol_size)
    else:
        #triangle
        draw_thick_line(center_x - symbol_size, center_y - symbol_size,
                       center_x + symbol_size, center_y)
        draw_thick_line(center_x + symbol_size, center_y,
                       center_x - symbol_size, center_y + symbol_size)
        draw_thick_line(center_x - symbol_size, center_y - symbol_size,
                       center_x - symbol_size, center_y + symbol_size)

def draw_quit_button(x, y, width, height):   #gameover
    #X (red)
    glColor3f(1.0, 0.0, 0.0)
    center_x, center_y = x + width//2, y + height//2
    x_size = min(width, height) // 2
    
    #X
    draw_thick_line(center_x - x_size, center_y - x_size,
                   center_x + x_size, center_y + x_size)
    draw_thick_line(center_x - x_size, center_y + x_size,
                   center_x + x_size, center_y - x_size)

def draw_ui():
    
    draw_restart_button(*click_RESTART, BUTTON_WIDTH, BUTTON_HEIGHT)
    draw_playpause_button(*click_PLAYPAUSE, BUTTON_WIDTH, BUTTON_HEIGHT)
    draw_quit_button(*click_QUIT, BUTTON_WIDTH, BUTTON_HEIGHT)

def check_collision():
    
    diamond_left = diamond_x - DIAMOND_SIZE//2
    diamond_right = diamond_x + DIAMOND_SIZE//2
    diamond_bottom = diamond_y - DIAMOND_SIZE//2
    
    catcher_left = catcher_x - CATCHER_WIDTH//2
    catcher_right = catcher_x + CATCHER_WIDTH//2
    catcher_top = CATCHER_HEIGHT//2  #catcher is at y=0
    
    return (diamond_bottom <= catcher_top and
            diamond_right >= catcher_left and
            diamond_left <= catcher_right)

def update_game():
    global diamond_y, diamond_x, diamond_color, score, game_state, catcher_color, fall_speed, last_frame_time
    
    current_time = time.time()
    delta_time = current_time - last_frame_time
    last_frame_time = current_time
    
    if game_state == 'run':
        #nicher dike move
        diamond_y -= fall_speed * delta_time * 60  #to maintain consistent speed
        
        #increase speed
        fall_speed = min(fall_speed + ACCELERATION * delta_time * 60, MAX_FALL_SPEED)
        
        #gain/lost
        if diamond_y - DIAMOND_SIZE//2 <= 0:
            if check_collision():
                score += 1
                print(f"Score: {score}")
                # New diamond
                diamond_x = random.randint(*DIAMOND_DROP_RANGE)
                diamond_y = 500
                diamond_color = (
                    random.uniform(0.5, 1.0),
                    random.uniform(0.5, 1.0),
                    random.uniform(0.5, 1.0))
            else:
                game_state = 'game_over'
                catcher_color = (1.0, 0.0, 0.0)  # Red
                print(f"Game Over! Score: {score}")

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # draw diamond
    draw_diamond(diamond_x, int(diamond_y), DIAMOND_SIZE, diamond_color)
    
    
    glPushMatrix()
    glTranslatef(0, CATCHER_HEIGHT//2, 0)
    draw_catcher(catcher_x, CATCHER_WIDTH, CATCHER_HEIGHT, catcher_color) #basket
    glPopMatrix()
    
    
    draw_ui()
    
    glutSwapBuffers()



def special_keys(key, x, y):  #controller
    global catcher_x, game_state

    if game_state != 'run':
        return

    if key == GLUT_KEY_LEFT:
        catcher_x = max(CATCHER_WIDTH // 2, catcher_x - 20)
    elif key == GLUT_KEY_RIGHT:
        catcher_x = min(WIDTH - CATCHER_WIDTH // 2, catcher_x + 20)

    glutPostRedisplay()


def mouse(button, state, x, y):
    global game_state, score, diamond_x, diamond_y, diamond_color, catcher_color, fall_speed, last_frame_time
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        #opengl coordinate
        gl_y = HEIGHT - y
        
        # new game
        if (click_RESTART[0] <= x <= click_RESTART[0] + BUTTON_WIDTH and
            click_RESTART[1] <= gl_y <= click_RESTART[1] + BUTTON_HEIGHT):
            # Reset game
            game_state = 'run'
            score = 0
            catcher_color = (1.0, 1.0, 1.0)
            diamond_x = random.randint(*DIAMOND_DROP_RANGE)
            diamond_y = 500
            diamond_color = (
                random.uniform(0.5, 1.0),
                random.uniform(0.5, 1.0),
                random.uniform(0.5, 1.0))
            fall_speed = INITIAL_FALL_SPEED
            last_frame_time = time.time()
            print("Starting Over!")
        
        # run/thambo
        elif (click_PLAYPAUSE[0] <= x <= click_PLAYPAUSE[0] + BUTTON_WIDTH and
              click_PLAYPAUSE[1] <= gl_y <= click_PLAYPAUSE[1] + BUTTON_HEIGHT):
            if game_state == 'run':
                game_state = 'thambo'
            elif game_state == 'thambo':
                game_state = 'run'
                last_frame_time = time.time()
        
        #quit
        elif (click_QUIT[0] <= x <= click_QUIT[0] + BUTTON_WIDTH and
              click_QUIT[1] <= gl_y <= click_QUIT[1] + BUTTON_HEIGHT):
            print(f"Goodbye! Final score: {score}")
            glutLeaveMainLoop()
    
    glutPostRedisplay()

def game_loop(value):
    update_game()
    glutPostRedisplay()
    glutTimerFunc(16, game_loop, 0)  # ~60 FPS

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamond!")
    
    init()
    glutDisplayFunc(display)

    glutSpecialFunc(special_keys) #keyboard func
    glutMouseFunc(mouse)
    glutTimerFunc(0, game_loop, 0)
    
    glutMainLoop()

if __name__ == "__main__":
    main()