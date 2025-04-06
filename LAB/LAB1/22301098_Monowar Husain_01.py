#task01
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

windowWidth = 500
windowHeight = 500




 
day_step = 0  

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    drawBackground()
    house()
    rain()
    
    glutSwapBuffers()

def drawBackground():
    global day_step

    colors = [
        (0, 0, 0),  
        (0.3, 0.3, 0.3),  
        (0.6, 0.6, 0.6),  
        (1.0, 1.0, 1.0)  
    ] #for day/n8

    glBegin(GL_QUADS)
    
    #black n8
    glColor3f(0, 0, 0)  
    glVertex2f(0, windowHeight)
    glVertex2f(windowWidth, windowHeight)


    glColor3f(*colors[day_step])  
    glVertex2f(windowWidth, windowHeight // 2) #day w, mid upp
    glVertex2f(0, windowHeight // 2)


    glColor3f(0, 0, 0)
    glVertex2f(windowWidth, 0)
    glVertex2f(0, 0)

    glEnd()

def house():
    glColor3f(1.0, 1.0, 0.0)  #yellow


    #house
    glBegin(GL_LINES)
    x1, y1 = 150, 150  #down-left
    x2, y2 = 350, 150  #down-right
    x3, y3 = 150, 300  #top-left
    x4, y4 = 350, 300  #top-right

    glVertex2f(x1, y1)
    glVertex2f(x2, y2)  #bottom

    glVertex2f(x3, y3)
    glVertex2f(x4, y4)  #top

    glVertex2f(x1, y1)
    glVertex2f(x3, y3)  #left

    glVertex2f(x2, y2)
    glVertex2f(x4, y4)  #right
    glEnd()

    #rooftop
    glBegin(GL_TRIANGLES)
    glVertex2f(x3, y3)
    glVertex2f(x4, y4)
    glVertex2f(250, 380)  #point
    glEnd()

    drawWindows() 

def drawWindows():
    glColor3f(0.8, 0.8, 1.0)

    window_size = 40

    #L win
    x1, y1 = 170, 200
    x2, y2 = x1 + window_size, y1
    x3, y3 = x1, y1 + window_size
    x4, y4 = x2, y3

    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)

    glVertex2f(x2, y2)
    glVertex2f(x4, y4)

    glVertex2f(x4, y4)
    glVertex2f(x3, y3)

    glVertex2f(x3, y3)
    glVertex2f(x1, y1)

    #R Win (120pixel righ shifted)
    x1 += 120 
    x2 += 120
    x3 += 120
    x4 += 120

    glVertex2f(x1, y1)
    glVertex2f(x2, y2)

    glVertex2f(x2, y2)
    glVertex2f(x4, y4)

    glVertex2f(x4, y4)
    glVertex2f(x3, y3)

    glVertex2f(x3, y3)
    glVertex2f(x1, y1)
    glEnd()

raindrops = [(random.randint(0, windowWidth), random.randint(0, windowHeight)) for _ in range(50)]
rainOrientation = 0 
def rain():
    global raindrops

    glColor3f(0.6, 0.6, 1.0)

    glBegin(GL_LINES)
    for i in range(len(raindrops)):
        x, y = raindrops[i]

        
        glVertex2f(x, y)
        glVertex2f(x + rainOrientation, y - 20) #drop

       
        raindrops[i] = (x, y - 0.2)  #speed


        
        if y - 5 < 0:
            raindrops[i] = (random.randint(0, windowWidth), windowHeight)
    glEnd()

def animateRain():
    glutPostRedisplay()

def bristi(key, x1, y1):
    global rainOrientation
    if key == GLUT_KEY_LEFT:
        rainOrientation -= 2  #left for - value
    elif key == GLUT_KEY_RIGHT:
        rainOrientation += 2  #rt for + value

def raatdin(key, x, y):
    global day_step

    if key == b'd' and day_step < 3:  ##left for - value
        day_step += 1

    elif key == b'n' and day_step > 0:  #rt for + value
        day_step -= 1

    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(windowWidth, windowHeight)

screen_width = glutGet(GLUT_SCREEN_WIDTH)
screen_height = glutGet(GLUT_SCREEN_HEIGHT)
glutInitWindowPosition((screen_width - 500) // 2, (screen_height - 500) // 2)

glutCreateWindow(b"lab1task1")


glutDisplayFunc(showScreen)
glutIdleFunc(animateRain)
glutKeyboardFunc(raatdin)
glutSpecialFunc(bristi)

glClearColor(0, 0, 0, 1.0) 

glutMainLoop()



#task02

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

window_width = 500
window_height = 500

balls = []
speed = random.randint(1, 5)
ball_size = random.randint(4, 8)
fun_flag = True  #chk animation func run or not
blinking = False

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        direction = random.choice([(-1, 1), (-1, -1), (1, 1), (1, -1)])
        self.dx = direction[0] * speed
        self.dy = direction[1] * speed
        
        self.color = (random.random(), random.random(), random.random()) #random color
        self.size = random.randint(4, 8)
        self.previous_color = None

def coordinates_convert(x, y):
    global window_width, window_height
    a = x - (window_width / 2)
    b = (window_height / 2) - y
    return a, b

def draw_ball(ball):
    glPointSize(ball.size)
    glBegin(GL_POINTS)
    glColor3f(ball.color[0], ball.color[1], ball.color[2])
    glVertex2f(ball.x, ball.y)
    glEnd()

def keyboardListener(key, x, y):
    global ball_size
    if key == b" ":
        #space die pause/play animation
        global fun_flag
        if fun_flag:
            fun_flag = False
            print("paused")
        else:
            fun_flag = True
            print("resumed")
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global fun_flag
    if not fun_flag:
        print("Animation paused, no action")
        return
    global speed
    if key == GLUT_KEY_UP:
        speed += 0.5
        for ball in balls:
            ball.dx = (ball.dx / abs(ball.dx)) * speed
            ball.dy = (ball.dy / abs(ball.dy)) * speed
        print(f"Speed increased, current speed: {speed}")
    
    if key == GLUT_KEY_DOWN:
        speed -= 0.5
        if speed > 0:
            for ball in balls:
                ball.dx = (ball.dx / abs(ball.dx)) * speed
                ball.dy = (ball.dy / abs(ball.dy)) * speed
            print(f"Speed decreased, current speed: {speed}")
        else:
            speed = 5
            print(f"Speed too low, reset to: {speed}")

def toggle_blinking(value):
    global blinking
    if not blinking:
        for ball in balls:
            if ball.previous_color:
                ball.color = ball.previous_color
        return
    
    if value == 0:
        for ball in balls:
            ball.previous_color = ball.color
            ball.color = (0, 0, 0)
        #delay 1s
        glutTimerFunc(1000, toggle_blinking, 1) 
    
    if value == 1:
        for ball in balls:
            ball.color = ball.previous_color
        
        if blinking:
            glutTimerFunc(1000, toggle_blinking, 0)
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global fun_flag
    global speed
    global blinking

    if not fun_flag:
        print("paused, no action")
        return
    
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        print(x, y)
        converted_x, converted_y = coordinates_convert(x, y)
        new_ball = Ball(converted_x, converted_y)
        direction = random.choice([(-1, 1), (-1, -1), (1, 1), (1, -1)])
        new_ball.dx = direction[0] * speed
        new_ball.dy = direction[1] * speed
        balls.append(new_ball)
    glutPostRedisplay()

    #Mouse left
    if button == GLUT_LEFT_BUTTON: 
        if state == GLUT_DOWN:
            blinking = True
            glutTimerFunc(0, toggle_blinking, 0)
        elif state == GLUT_UP:
            blinking = False
            for ball in balls:
                if ball.previous_color:
                    ball.color = ball.previous_color
        
        print(f"Blinking state: {blinking}")
    glutPostRedisplay()

def render_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    for ball in balls:
        draw_ball(ball)
    glutSwapBuffers()

def animate_balls():
    glutPostRedisplay()
    global fun_flag
    if not fun_flag:
        return
    for ball in balls:
        ball.x += ball.dx
        ball.y += ball.dy
        if ball.x <= -window_width / 2 or ball.x >= window_width / 2: 
            ball.dx = -ball.dx
        if ball.y <= -window_height / 2 or ball.y >= window_height / 2: 
            ball.dy = -ball.dy

def initialize():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

glutInit()
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(100, 150)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

window = glutCreateWindow(b"lab1task2")
initialize()

glutDisplayFunc(render_scene)
glutIdleFunc(animate_balls)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()
