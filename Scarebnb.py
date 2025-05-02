from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18

import math
import random

# Camera and scene settings
camera_pos = (0, 500, 500)
fovY = 60
GRID_LENGTH = 2000  # Increased floor area
BORDER_X_MIN = -GRID_LENGTH + 20
BORDER_X_MAX = GRID_LENGTH - 20
BORDER_Y_MIN = -GRID_LENGTH + 20
BORDER_Y_MAX = GRID_LENGTH - 20
rand_var = 423

first_person_mode = False

# Character state
man_pos = [0, 0, 0]  # [x, y, z]
man_angle = 0  # Facing angle (degrees)
man_speed = 5
jumping = False
jump_velocity = 0
keys_pressed = set()
# List to store active lasers
lasers = []  # List to store active lasers
# List to store active ghosts
ghosts = []
# spawn zones for your 7 rooms:
spawn_zones = [
    (-300, 300, -300, 300),  # Room 1
    (-300, 300, -1200, -600),  # Room 2 #1
    (300, 900, -300, 300),  # Room 2 #2
    (200, 800, -1200, -600),  # Room 3 #1
    (900, 1900, -300, 300),  # Room 3 #2
    (800, 1800, -1200, -600),  # Room 3 #3
    (1800, 2200, -1200, -600),  # Room 3 #4
]
spawn_zones += [(-300, 1700, -600, -300), (1400, 1700, -600, -200), ]  # hallway

# Player life system
player_life = 5  # Initial player life

# Treasure and score system
treasures = []
score = 0

# walls collision
collision_walls = []  # list of (xmin, xmax, ymin, ymax) for every wall segment
# boss
boss_fight_active = False
victory = False
enemy_projectiles = []  # boss’s shots
# Track if the game is over
game_over = False

cheat_mode = False  # Track cheat mode state


def add_wall(x_center, y_center, width, height):
    """Register one axis-aligned wall rectangle for collision."""
    xmin = x_center - width / 2
    xmax = x_center + width / 2
    ymin = y_center - height / 2
    ymax = y_center + height / 2
    collision_walls.append((xmin, xmax, ymin, ymax))


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def room1():
    # PARAMETERS
    ROOM_SIZE = 300
    GRID_STEP = 40
    WALL_HEIGHT = 200
    WALL_THICK = 5

    # FLOOR
    DARK_BROWN = (0.15, 0.07, 0.02)
    LIGHT_BROWN = (0.4, 0.2, 0.1)
    glBegin(GL_QUADS)
    for x in range(-ROOM_SIZE, ROOM_SIZE, GRID_STEP):
        for y in range(-ROOM_SIZE, ROOM_SIZE, GRID_STEP):
            noise = (abs(x) % 100) * 0.02 + math.sin(x * 0.05) + math.sin((x + y) * 0.1)
            intensity = (math.sin(noise) + 1) * 0.5
            r = DARK_BROWN[0] + (LIGHT_BROWN[0] - DARK_BROWN[0]) * intensity
            g = DARK_BROWN[1] + (LIGHT_BROWN[1] - DARK_BROWN[1]) * intensity
            b = DARK_BROWN[2] + (LIGHT_BROWN[2] - DARK_BROWN[2]) * intensity
            glColor3f(r, g, b)
            glVertex3f(x, y, 0)
            glVertex3f(x + GRID_STEP, y, 0)
            glVertex3f(x + GRID_STEP, y + GRID_STEP, 0)
            glVertex3f(x, y + GRID_STEP, 0)
    glEnd()

    # WALLS (+ door gap on south)
    wall_color = (0.30, 0.10, 0.10)
    door_w = 110
    half_w = (2 * ROOM_SIZE - door_w) / 2
    glColor3f(*wall_color)

    # North wall
    glPushMatrix()
    glTranslatef(0, ROOM_SIZE, WALL_HEIGHT / 2)
    glScalef(2 * ROOM_SIZE, WALL_THICK, WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    add_wall(x_center=0,
             y_center=ROOM_SIZE,
             width=2 * ROOM_SIZE,
             height=WALL_THICK)

    # South wall segments (door gap in middle)
    # Left segment
    glPushMatrix()
    glTranslatef(-ROOM_SIZE + half_w / 2, -ROOM_SIZE, WALL_HEIGHT / 2)
    glScalef(half_w, WALL_THICK, WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    add_wall(x_center=-ROOM_SIZE + half_w / 2,
             y_center=-ROOM_SIZE,
             width=half_w,
             height=WALL_THICK)

    # Right segment
    glPushMatrix()
    glTranslatef(ROOM_SIZE - half_w / 2, -ROOM_SIZE, WALL_HEIGHT / 2)
    glScalef(half_w, WALL_THICK, WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    add_wall(x_center=ROOM_SIZE - half_w / 2,
             y_center=-ROOM_SIZE,
             width=half_w,
             height=WALL_THICK)

    # East wall
    glPushMatrix()
    glTranslatef(ROOM_SIZE, 0, WALL_HEIGHT / 2)
    glScalef(WALL_THICK, 2 * ROOM_SIZE, WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    add_wall(x_center=ROOM_SIZE,
             y_center=0,
             width=WALL_THICK,
             height=2 * ROOM_SIZE)

    # West wall
    glPushMatrix()
    glTranslatef(-ROOM_SIZE, 0, WALL_HEIGHT / 2)
    glScalef(WALL_THICK, 2 * ROOM_SIZE, WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    add_wall(x_center=-ROOM_SIZE,
             y_center=0,
             width=WALL_THICK,
             height=2 * ROOM_SIZE)

    # SIDE LAMPS
    glColor3f(1.0, 0.8, 0.2)
    for sx in (-1, 1):
        glPushMatrix()
        glTranslatef(sx * (ROOM_SIZE - WALL_THICK - 5), -10, WALL_HEIGHT - 10)
        glutSolidSphere(5, 16, 16)
        glPopMatrix()

    # PAINTING with FRAME
    psize = 60;
    z1, z2 = 50, 130
    frame_w = psize + 5;
    frame_h1, frame_h2 = z1 - 5, z2 + 5
    glColor3f(0.05, 0.02, 0.02)
    glBegin(GL_LINE_LOOP)
    glVertex3f(-frame_w, ROOM_SIZE - WALL_THICK / 2 - 2, frame_h1)
    glVertex3f(frame_w, ROOM_SIZE - WALL_THICK / 2 - 2, frame_h1)
    glVertex3f(frame_w, ROOM_SIZE - WALL_THICK / 2 - 2, frame_h2)
    glVertex3f(-frame_w, ROOM_SIZE - WALL_THICK / 2 - 2, frame_h2)
    glEnd()
    glColor3f(0.4, 0, 0)
    glBegin(GL_QUADS)
    glVertex3f(-psize, ROOM_SIZE - WALL_THICK / 2 - 2, z1)
    glVertex3f(psize, ROOM_SIZE - WALL_THICK / 2 - 2, z1)
    glVertex3f(psize, ROOM_SIZE - WALL_THICK / 2 - 2, z2)
    glVertex3f(-psize, ROOM_SIZE - WALL_THICK / 2 - 2, z2)
    glEnd()

    # PROP: Table + Candle (NW) - larger & brighter
    glColor3f(0.55, 0.35, 0.20);
    glPushMatrix()
    glTranslatef(-ROOM_SIZE / 2, ROOM_SIZE / 2 - 70, 20);
    glScalef(120, 40, 10);
    glutSolidCube(1);
    glPopMatrix()
    for dx in (-55, 55):
        for dy in (-15, 15):
            glColor3f(0.55, 0.35, 0.20)
            glPushMatrix();
            glTranslatef(-ROOM_SIZE / 2 + dx, ROOM_SIZE / 2 - 70 + dy, 5);
            glScalef(10, 10, 45);
            glutSolidCube(1);
            glPopMatrix()
    glColor3f(0.95, 0.95, 0.75)
    glPushMatrix();
    glTranslatef(-ROOM_SIZE / 2, ROOM_SIZE / 2 - 70, 60);
    gluCylinder(gluNewQuadric(), 3, 3, 15, 8, 1);
    glTranslatef(0, 0, 17);
    glColor3f(1, 0.85, 0.1);
    glutSolidSphere(6, 8, 8);
    glPopMatrix()

    # PROP: Crate (SE) - distinct orange
    glColor3f(0.9, 0.6, 0.3);
    glPushMatrix()
    glTranslatef(ROOM_SIZE / 2 - 60, -ROOM_SIZE / 2 + 60, 30);
    glScalef(60, 60, 60);
    glutSolidCube(1);
    glPopMatrix()

    # PROP: Barrel (SW) - lighter gray
    glColor3f(0.5, 0.5, 0.5)
    glPushMatrix()
    glTranslatef(-ROOM_SIZE / 2 + 80, -ROOM_SIZE / 2 + 50, 30)
    glRotatef(-20, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 22, 22, 45, 12, 4)
    glPopMatrix()

    # BIG COBWEBS — large webs confined inside walls
    glColor3f(0.8, 0.8, 0.8)
    web_radius = ROOM_SIZE - WALL_THICK - 20  # just inside wall, inset 20 units
    arc_steps = 240
    num_arcs = 5
    corners = [
        (-ROOM_SIZE + WALL_THICK + 10, ROOM_SIZE - WALL_THICK - 10),
        (ROOM_SIZE - WALL_THICK - 10, ROOM_SIZE - WALL_THICK - 10),
        (ROOM_SIZE - WALL_THICK - 10, -ROOM_SIZE + WALL_THICK + 10),
        (-ROOM_SIZE + WALL_THICK + 10, -ROOM_SIZE + WALL_THICK + 10)
    ]
    for cx, cy in corners:
        # concentric quarter arcs
        for j in range(1, num_arcs + 1):
            r = web_radius * j / num_arcs
            glBegin(GL_LINE_STRIP)
            for i in range(arc_steps // 4 + 1):
                angle = math.radians(90 * i / (arc_steps // 4))
                if cx > 0 and cy > 0:
                    a = math.radians(180) + angle
                elif cx < 0 and cy > 0:
                    a = math.radians(180) - angle
                elif cx < 0 and cy < 0:
                    a = math.radians(270) - angle
                else:
                    a = math.radians(360) - angle
                glVertex3f(cx + r * math.cos(a), cy + r * math.sin(a), WALL_HEIGHT - 2)
            glEnd()
        # radial spokes
        glBegin(GL_LINES)
        for k in range(0, 91, 15):
            if cx > 0 and cy > 0:
                base = math.radians(180 + k)
            elif cx < 0 and cy > 0:
                base = math.radians(180 - k)
            elif cx < 0 and cy < 0:
                base = math.radians(270 - k)
            else:
                base = math.radians(360 - k)
            glVertex3f(cx, cy, WALL_HEIGHT - 2)
            glVertex3f(cx + web_radius * math.cos(base), cy + web_radius * math.sin(base), WALL_HEIGHT - 2)
        glEnd()


# Draws an L-shaped corridor (white-dotted on your map).
def draw_hallway():
    # PARAMETERS
    STEP = 40.0
    DARK_BROWN = (0.15, 0.07, 0.02)
    LIGHT_BROWN = (0.40, 0.20, 0.10)
    WALL_HEIGHT = 200.0
    WALL_THICK = 5.0
    wall_color = (0.30, 0.10, 0.10)

    # EAST–WEST LEG
    x0, y0 = -300.0, -600.0
    HALL_LEN, HALL_WID = 2500.0, 300.0
    x = x0
    while x < x0 + HALL_LEN:
        y = y0
        while y < y0 + HALL_WID:
            noise = (abs(x) % 100) * 0.02 + math.sin(x * 0.05) + math.sin((x + y) * 0.1)
            t = (math.sin(noise) + 1) * 0.5
            r = DARK_BROWN[0] + (LIGHT_BROWN[0] - DARK_BROWN[0]) * t
            g = DARK_BROWN[1] + (LIGHT_BROWN[1] - DARK_BROWN[1]) * t
            b = DARK_BROWN[2] + (LIGHT_BROWN[2] - DARK_BROWN[2]) * t
            glColor3f(r, g, b)
            glBegin(GL_QUADS)
            glVertex3f(x, y, 0)
            glVertex3f(x + STEP, y, 0)
            glVertex3f(x + STEP, y + STEP, 0)
            glVertex3f(x, y + STEP, 0)
            glEnd()
            y += STEP
        x += STEP

    # NORTH–SOUTH LEG
    x1, y1 = x0 + HALL_LEN - HALL_WID, y0 + HALL_WID
    NS_LEN, NS_WID = HALL_WID, 600.0
    x = x1
    while x < x1 + NS_LEN:
        y = y1
        while y < y1 + NS_WID:
            noise = (abs(x) % 100) * 0.02 + math.sin(x * 0.05) + math.sin((x + y) * 0.1)
            t = (math.sin(noise) + 1) * 0.5
            r = DARK_BROWN[0] + (LIGHT_BROWN[0] - DARK_BROWN[0]) * t
            g = DARK_BROWN[1] + (LIGHT_BROWN[1] - DARK_BROWN[1]) * t
            b = DARK_BROWN[2] + (LIGHT_BROWN[2] - DARK_BROWN[2]) * t
            glColor3f(r, g, b)
            glBegin(GL_QUADS)
            glVertex3f(x, y, 0)
            glVertex3f(x + STEP, y, 0)
            glVertex3f(x + STEP, y + STEP, 0)
            glVertex3f(x, y + STEP, 0)
            glEnd()
            y += STEP
        x += STEP

    # WALL AT HALLWAY START (near Room1)
    glColor3f(*wall_color)
    glPushMatrix()
    glTranslatef(x0, y0 + HALL_WID / 2, WALL_HEIGHT / 2)
    glScalef(WALL_THICK, HALL_WID, WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    add_wall(x_center=x0,
             y_center=y0 + HALL_WID / 2,
             width=WALL_THICK,
             height=HALL_WID)
    # WALL AT NS-LEG END (far north end of the L)
    glColor3f(*wall_color)
    # center it in X over the width of that leg, and at the top Y
    wall_x = x1 + NS_LEN / 2.0
    wall_y = y1 + NS_WID
    glPushMatrix()
    glTranslatef(wall_x, wall_y, WALL_HEIGHT / 2.0)
    # span it east–west across the corridor width, thickness north–south
    glScalef(NS_LEN, WALL_THICK, WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()

    add_wall(
        x_center=wall_x,
        y_center=wall_y,
        width=NS_LEN,
        height=WALL_THICK
    )


def room2(offset_x=0, offset_y=0,
          door_side='north',  # 'north','south','east' or 'west'
          door_center=0,  # center-of-gap along that wall
          door_width=110.0):
    """
    Room 2: wooden floor + walls with a door on any side,
    plus horror décor: spider-webs, blood pool, coffin, candles & skulls.
    """
    ROOM = 300
    H = 200
    T = 5
    STEP = 40
    hw = 300 / 2
    hh = 300 / 2

    glPushMatrix()
    glTranslatef(offset_x, offset_y, 0)

    # 1) wooden-plank floor
    DARK = (0.15, 0.07, 0.02)
    LIGHT = (0.4, 0.2, 0.1)
    glBegin(GL_QUADS)
    for x in range(-ROOM, ROOM, STEP):
        for y in range(-ROOM, ROOM, STEP):
            n = (abs(x) % 100) * 0.02 + math.sin(x * 0.05) + math.sin((x + y) * 0.1)
            i = (math.sin(n) + 1) * 0.5
            r = DARK[0] + (LIGHT[0] - DARK[0]) * i
            g = DARK[1] + (LIGHT[1] - DARK[1]) * i
            b = DARK[2] + (LIGHT[2] - DARK[2]) * i
            glColor3f(r, g, b)
            glVertex3f(x, y, 0)
            glVertex3f(x + STEP, y, 0)
            glVertex3f(x + STEP, y + STEP, 0)
            glVertex3f(x, y + STEP, 0)
    glEnd()

    # 2) walls with a parametric door
    glColor3f(0.30, 0.10, 0.10)
    half = (2 * ROOM - door_width) / 2

    def W(tx, ty, sx, sy):
        # draw the actual GL cube exactly where you expect:
        glPushMatrix()
        glTranslatef(tx, ty, H / 2)
        glScalef(sx, sy, H)
        glutSolidCube(1)
        glPopMatrix()
        add_wall(
            x_center=offset_x + tx,
            y_center=offset_y + ty,
            width=sx,
            height=sy
        )

    # north
    if door_side == 'north':
        W(door_center - door_width / 2 - half / 2, ROOM, half, T)
        W(door_center + door_width / 2 + half / 2, ROOM, half, T)

    else:
        W(0, ROOM, 2 * ROOM, T)

    # south
    if door_side == 'south':
        W(door_center - door_width / 2 - half / 2, -ROOM, half, T)
        W(door_center + door_width / 2 + half / 2, -ROOM, half, T)

    else:
        W(0, -ROOM, 2 * ROOM, T)

    # east
    if door_side == 'east':
        W(ROOM, door_center - door_width / 2 - half / 2, T, half)
        W(ROOM, door_center + door_width / 2 + half / 2, T, half)

    else:
        W(ROOM, 0, T, 2 * ROOM)

    # west
    if door_side == 'west':
        W(-ROOM, door_center - door_width / 2 - half / 2, T, half)
        W(-ROOM, door_center + door_width / 2 + half / 2, T, half)

    else:
        W(-ROOM, 0, T, 2 * ROOM)

    # 3) horror décor

    # a) giant spider‐webs in all 4 corners
    glColor3f(1, 1, 1)
    web_rad = ROOM * 0.5
    for cx, cy in [(ROOM - T, ROOM - T), (-ROOM + T, ROOM - T),
                   (ROOM - T, -ROOM + T), (-ROOM + T, -ROOM + T)]:
        glBegin(GL_LINE_STRIP)
        for ring in range(3):
            for seg in range(0, 91, 15):
                a = math.radians(seg)
                r = web_rad - ring * web_rad * 0.3
                glVertex3f(cx, cy,
                           H - 10 - ring * 5)
                glVertex3f(
                    cx + math.cos(a) * r,
                    cy + math.sin(a) * r,
                    H - 10 - ring * 5
                )
        glEnd()

    # b) blood pool on floor center
    glColor4f(0.6, 0, 0, 0.7)
    glBegin(GL_TRIANGLE_FAN)
    bx, by, bz = 0, -ROOM * 0.3, 1
    glVertex3f(bx, by, bz)
    for ang in range(0, 361, 30):
        a = math.radians(ang)
        glVertex3f(
            bx + math.cos(a) * 40 + random.uniform(-5, 5),
            by + math.sin(a) * 20 + random.uniform(-5, 5),
            bz
        )
    glEnd()

    # c) broken coffin (rotated box) in NE
    glColor3f(0.25, 0.1, 0.05)
    glPushMatrix()
    glTranslatef(ROOM * 0.5, ROOM * 0.2, 20)
    glRotatef(15, 0, 0, 1)
    glScalef(80, 30, 8)
    glutSolidCube(1)
    glPopMatrix()

    # d) flickering candles along west wall
    for y in (-ROOM * 0.6, 0, ROOM * 0.6):
        glPushMatrix()
        glTranslatef(-ROOM + 15, y, 10)
        glColor3f(0.9, 0.9, 0.7)
        gluCylinder(gluNewQuadric(), 2, 2, 12, 6, 1)
        glTranslatef(0, 0, 14)
        glColor3f(1, 0.8, 0.1)
        glutSolidSphere(4, 8, 8)
        glPopMatrix()
    # ——— Corner Props ———

    # top-right: rusty barrel
    glColor3f(0.4, 0.2, 0.05)
    glPushMatrix()
    glTranslatef(hw - 50, hh - 50, 25)
    glScalef(50, 50, 50)
    glutSolidCube(1)
    glPopMatrix()

    # top-left: overturned chair
    glColor3f(0.2, 0.1, 0.05)
    glPushMatrix()
    glTranslatef(-hw + 60, hh - 40, 10)
    glRotatef(90, 1, 0, 0)  # lay on its back
    glRotatef(20, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 5, 30, 8, 4)  # seat
    glTranslatef(0, 0, 30)  # move up for backrest
    gluCylinder(gluNewQuadric(), 5, 5, 30, 8, 4)  # back-rest
    glPopMatrix()

    # bottom-left: spider-egg sac
    glColor3f(0.9, 0.9, 0.8)
    glPushMatrix()
    glTranslatef(-hw + 30, -hh + 30, 5)
    glutSolidSphere(10, 12, 12)
    glPopMatrix()

    # bottom-right: shadowed floor patch
    glColor4f(0, 0, 0, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(hw - 80, -hh + 10, 0.1)
    glVertex3f(hw - 10, -hh + 10, 0.1)
    glVertex3f(hw - 10, -hh + 70, 0.1)
    glVertex3f(hw - 80, -hh + 70, 0.1)
    glEnd()

    # ——— Scary Paintings on All Four Walls ———
    # painting dimensions
    p_w, p_h = 80.0, 100.0
    z1, z2 = 60.0, 60.0 + p_h

    # dark red canvas
    glColor3f(0.4, 0.0, 0.0)
    # Black “cracks”
    glColor3f(1, 1, 1);
    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex3f(-p_w, ROOM + T / 2 + 0.2, z2 - 20);
    glVertex3f(p_w, ROOM + T / 2 + 0.2, z1 + 10)
    glVertex3f(-20, ROOM + T / 2 + 0.2, z2);
    glVertex3f(20, ROOM + T / 2 + 0.2, z1)
    glEnd()

    # West wall (rotated quad)
    glPushMatrix()
    glTranslatef(-ROOM - T / 2 - 0.1 - 60, 0, 0)
    glRotatef(-90, 0, 0, 1)
    glColor3f(0.4, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(-p_w, hh - 60, z1)
    glVertex3f(p_w, hh - 60, z1)
    glVertex3f(p_w, hh - 60, z2)
    glVertex3f(-p_w, hh - 60, z2)
    glEnd()
    glColor3f(0, 0, 0);
    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex3f(-p_w, hh + 0.1 - 100, z2 - 20);
    glVertex3f(p_w, hh + 0.1 - 100, z1 + 20)
    glVertex3f(-20, hh + 0.1 - 100, z2 - 35);
    glVertex3f(20, hh + 0.1 - 100, z1 + 10)
    glEnd()
    glPopMatrix()

    # e) skulls scattered on floor
    glColor3f(0.9, 0.9, 0.9)
    for sx, sy in [(-50, 50), (30, -70), (80, 80)]:
        glPushMatrix()
        glTranslatef(sx, sy, 5)
        gluSphere(gluNewQuadric(), 5, 8, 8)
        glPopMatrix()

    glPopMatrix()


def room3(offset_x=0, offset_y=0,
          room_w=350, room_h=250,  # full extents in X/Y
          door_side='west',  # 'north','south','east' or 'west'
          door_center=0,  # center‐of‐gap along that wall (in world coords)
          door_width=100.0):
    """
    Room 3: parametric width/height bedroom
    plus: big bed, oversized bookshelf, cracked mirror, rocking chair, blood splatter.
    """
    H = 200  # wall height
    T = 5  # wall thickness
    STEP = 40  # floor plank size

    glPushMatrix()
    glTranslatef(offset_x, offset_y, 0)

    # 1) wooden‐plank floor (same shader as room2)
    DARK = (0.15, 0.07, 0.02)
    LIGHT = (0.40, 0.20, 0.10)
    glBegin(GL_QUADS)
    for x in range(-room_w, room_w, STEP):
        for y in range(-room_h, room_h, STEP):
            n = (abs(x) % 100) * 0.02 + math.sin(x * 0.05) + math.sin((x + y) * 0.1)
            i = (math.sin(n) + 1) * 0.5
            r = DARK[0] + (LIGHT[0] - DARK[0]) * i
            g = DARK[1] + (LIGHT[1] - DARK[1]) * i
            b = DARK[2] + (LIGHT[2] - DARK[2]) * i
            glColor3f(r, g, b)
            glVertex3f(x, y, 0)
            glVertex3f(x + STEP, y, 0)
            glVertex3f(x + STEP, y + STEP, 0)
            glVertex3f(x, y + STEP, 0)
    glEnd()

    # 2) walls + parametric door
    glColor3f(0.30, 0.10, 0.10)
    half_x = (2 * room_w - door_width) / 2
    half_y = (2 * room_h - door_width) / 2

    def W(tx, ty, sx, sy):
        # draw
        glPushMatrix()
        glTranslatef(tx, ty, H / 2)
        glScalef(sx, sy, H)
        glutSolidCube(1)
        glPopMatrix()
        # collision
        add_wall(
            x_center=offset_x + tx,
            y_center=offset_y + ty,
            width=sx,
            height=sy
        )

    # north
    if door_side == 'north':
        W(door_center - door_width / 2 - half_x / 2, room_h, half_x, T)
        W(door_center + door_width / 2 + half_x / 2, room_h, half_x, T)
    else:
        W(0, room_h, 2 * room_w, T)
    # south
    if door_side == 'south':
        W(door_center - door_width / 2 - half_x / 2, -room_h, half_x, T)
        W(door_center + door_width / 2 + half_x / 2, -room_h, half_x, T)
    else:
        W(0, -room_h, 2 * room_w, T)
    # east
    if door_side == 'east':
        W(room_w, door_center - door_width / 2 - half_y / 2, T, half_y)
        W(room_w, door_center + door_width / 2 + half_y / 2, T, half_y)
    else:
        W(room_w, 0, T, 2 * room_h)
    # west
    if door_side == 'west':
        W(-room_w, door_center - door_width / 2 - half_y / 2, T, half_y)
        W(-room_w, door_center + door_width / 2 + half_y / 2, T, half_y)
    else:
        W(-room_w, 0, T, 2 * room_h)

    # 3) bedroom décor

    # a) BIG BED (south-west corner)
    glColor3f(0.2, 0.1, 0.05)
    glPushMatrix()
    glTranslatef(-room_w + 100, -room_h + 80, 20)
    glScalef(200, 120, 40)
    glutSolidCube(1)
    glPopMatrix()
    # pillow
    glColor3f(0.9, 0.9, 0.9)
    glPushMatrix()
    glTranslatef(-room_w + 100, -room_h + 20, 50)
    glScalef(80, 60, 20)
    glutSolidCube(1)
    glPopMatrix()

    # b) OVERSIZED BOOKSHELF (north-east corner)
    glColor3f(0.3, 0.15, 0.05)
    glPushMatrix()
    glTranslatef(room_w - 60, room_h - 100, 100)
    glScalef(120, 40, 200)
    glutSolidCube(1)
    glPopMatrix()
    # a few “books” as thin quads
    glColor3f(0.8, 0.1, 0.1)
    for i in range(-2, 3):
        glBegin(GL_QUADS)
        x0 = room_w - 120 + i * 20
        glVertex3f(x0, room_h - 120, 140)
        glVertex3f(x0 + 5, room_h - 120, 140)
        glVertex3f(x0 + 5, room_h - 120, 180)
        glVertex3f(x0, room_h - 120, 180)
        glEnd()

    # c) cracked mirror (east wall middle)
    glColor3f(0.7, 0.7, 0.9)
    glBegin(GL_QUADS)
    mx1, mx2 = room_w, 0
    my = 0
    mw, mh = 80, 120
    glVertex3f(mx1 + T / 2 + 0.1 - 10, my - mw, 80)
    glVertex3f(mx1 + T / 2 + 0.1 - 10, my + mw, 80)
    glVertex3f(mx1 + T / 2 + 0.1 - 10, my + mw, mh + 80)
    glVertex3f(mx1 + T / 2 + 0.1 - 10, my - mw, mh + 80)
    glEnd()
    # crack lines
    glColor3f(0, 0, 0);
    glLineWidth(2)
    glBegin(GL_LINES)
    for yz in [100, 140, 180]:
        glVertex3f(mx1 + T / 2 + 0.2, my - mw, yz)
        glVertex3f(mx1 + T / 2 + 0.2, my + mw, yz - 20)
    glEnd()

    # d) Rocking chair (west wall middle)
    glColor3f(0.2, 0.1, 0.05)
    glPushMatrix()
    glTranslatef(-room_w + 60, 0, 20)
    glRotatef(90, 0, 1, 0)  # face east
    gluCylinder(gluNewQuadric(), 5, 5, 60, 8, 4)  # seat
    glPopMatrix()

    # e) blood splatter on north wall
    glColor4f(0.6, 0, 0, 0.8)
    glBegin(GL_TRIANGLE_FAN)
    bx, by, bz = 0, room_h - T / 2 - 0.1, 120
    glVertex3f(bx, by, bz)
    for ang in range(0, 361, 30):
        a = math.radians(ang)
        glVertex3f(
            bx + math.cos(a) * 50 + random.uniform(-10, 10),
            by,
            bz + math.sin(a) * 20 + random.uniform(-5, 5)
        )
    glEnd()

    glPopMatrix()


def draw_man():
    glPushMatrix()
    glTranslatef(man_pos[0], man_pos[1], man_pos[2] + 40)
    glRotatef(-man_angle, 0, 0, 1)  # Face direction

    # Enable blending for opacity if cheat mode is active
    if cheat_mode:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        body_alpha = 0.3
    else:
        body_alpha = 1.0

    # Body
    glColor4f(0.8, 0.2, 0.2, body_alpha)
    glPushMatrix()
    gluCylinder(gluNewQuadric(), 20, 20, 40, 10, 10)
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(0, 0, 52)
    glColor4f(0.9, 0.7, 0.5, body_alpha)
    gluSphere(gluNewQuadric(), 12, 10, 10)
    glPopMatrix()

    # Arms
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glColor4f(0.2, 0.2, 0.8, body_alpha)

    # Left arm
    glPushMatrix()
    glTranslatef(-23, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 5, 40, 10, 10)
    glPopMatrix()

    # Right arm with weapon
    glPushMatrix()
    glTranslatef(23, 0, 0)
    glRotatef(0, 0, 0, 1)  # No rotation for simplicity
    gluCylinder(gluNewQuadric(), 5, 5, 40, 10, 10)

    # Weapon (cuboid)
    glPushMatrix()
    glTranslatef(20, 0, 0)  # position weapon at hand tip
    glScalef(30, 2, 2)  # length, height, width
    glColor4f(0.3, 0.3, 0.3, body_alpha)  # dark gray weapon
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()  # End right arm
    glPopMatrix()  # End arm block

    # Legs
    glPushMatrix()
    glColor4f(0.1, 0.1, 0.1, body_alpha)
    glTranslatef(-7, 0, -41)
    gluCylinder(gluNewQuadric(), 7, 7, 40, 10, 10)
    glTranslatef(15, 0, 0)
    gluCylinder(gluNewQuadric(), 7, 7, 40, 10, 10)
    glPopMatrix()

    if cheat_mode:
        glDisable(GL_BLEND)

    glPopMatrix()


# Define the ghost class
class Ghost:
    def __init__(self, x, y, z, angle):
        self.pos = [x, y, z]  # Position (x, y, z)
        self.angle = angle  # Direction the ghost is facing
        self.size = 50  # Size of the ghost
        self.body_height = 60  # Height of the body
        self.body_radius_top = 20  # Slimmer top radius
        self.body_radius_bottom = 25  # Slimmer bottom radius
        self.head_radius = 20  # Radius of the head
        # Animation parameters for scaling effect
        self.scale = 1.0  # Current scale factor
        self.scale_dir = 1  # Direction of scaling (1 = expanding, -1 = shrinking)
        self.scale_speed = 0.005  # Speed of scaling animation
        self.scale_min = 0.8  # Minimum scale factor
        self.scale_max = 1.2  # Maximum scale factor
        # Movement parameters
        self.speed = 0.7  # Speed of ghost movement

    def update_scale(self):
        # Update the scale factor for animation
        self.scale += self.scale_dir * self.scale_speed
        if self.scale > self.scale_max:
            self.scale = self.scale_max
            self.scale_dir = -1  # Start shrinking
        elif self.scale < self.scale_min:
            self.scale = self.scale_min
            self.scale_dir = 1  # Start expanding

    def move_towards_player(self, player_pos):
        # Calculate direction vector from ghost to player
        move_dir = [player_pos[0] - self.pos[0], player_pos[1] - self.pos[1]]

        # Normalize the direction vector
        mag = math.sqrt(move_dir[0] ** 2 + move_dir[1] ** 2)
        if mag > 0:  # Avoid division by zero
            move_dir[0] /= mag
            move_dir[1] /= mag

            # Move ghost towards player
            self.pos[0] += move_dir[0] * self.speed
            self.pos[1] += move_dir[1] * self.speed

            # Update ghost's angle to face the player
            self.angle = (math.degrees(math.atan2(move_dir[1], move_dir[0])) + 90) % 360

    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        # Apply the scaling effect to make the ghost pulsate
        glScalef(self.scale, self.scale, self.scale)

        # Body (Cylinder) - Slimmer ghost body (Black)
        glColor3f(0, 0, 0)  # Black color for the body
        glPushMatrix()
        glRotatef(-self.angle, 0, 0, 1)
        gluCylinder(gluNewQuadric(), self.body_radius_top, self.body_radius_bottom, self.body_height, 10,
                    10)  # Slimmer body
        glPopMatrix()

        # Head (Sphere) - Larger head
        glPushMatrix()
        glTranslatef(0, 0, self.body_height)  # Position head on top of the body
        glColor3f(1.0, 1.0, 1.0)  # White color for the head
        gluSphere(gluNewQuadric(), self.head_radius, 10, 10)  # Head
        glPopMatrix()

        # Arms (using small cylinders) - Outstretched arms to scare the player
        arm_length = 30
        arm_thickness = 5
        glPushMatrix()

        # Left arm - Outstretched to scare
        glTranslatef(-self.body_radius_bottom, 0, self.body_height - 10)
        glColor3f(1.0, 1.0, 1.0)  # White arms
        gluCylinder(gluNewQuadric(), arm_thickness, arm_thickness, arm_length, 10, 10)

        # Right arm - Outstretched to scare
        glTranslatef(2 * self.body_radius_bottom, 0, 0)  # Move right arm to the other side
        gluCylinder(gluNewQuadric(), arm_thickness, arm_thickness, arm_length, 10, 10)

        glPopMatrix()

        # Draw facial features (eyes and mouth)
        # Eyes (two spheres)
        glPushMatrix()
        glTranslatef(-7, 10, self.body_height + 10)  # Left eye position
        glColor3f(0, 0, 0)  # Black for eyes
        gluSphere(gluNewQuadric(), 5, 10, 10)  # Left eye
        glPopMatrix()

        glPushMatrix()
        glTranslatef(7, 10, self.body_height + 10)  # Right eye position
        glColor3f(0, 0, 0)  # Black for eyes
        gluSphere(gluNewQuadric(), 5, 10, 10)  # Right eye
        glPopMatrix()

        # Mouth (small oval shape)
        glPushMatrix()
        glTranslatef(0, -5, self.body_height)  # Position of mouth
        glColor3f(0, 0, 0)  # Black for the mouth
        glScalef(1, 0.3, 1)
        gluSphere(gluNewQuadric(), 8, 10, 10)
        glPopMatrix()

        glPopMatrix()

    def is_hit_by_laser(self, laser):
        # Calculate the position of the ghost's head
        ghost_head_z = self.pos[2] + self.body_height

        # Calculate distance between laser and ghost's head
        distance = math.sqrt(
            (self.pos[0] - laser['x']) ** 2 +
            (self.pos[1] - laser['y']) ** 2 +
            (ghost_head_z - laser['z']) ** 2
        )

        # Check if distance is within hit radius (head radius + some tolerance)
        return distance < (self.head_radius + 15)


# Define the treasure class
class Treasure:
    def __init__(self, x, y, z):
        self.pos = [x, y, z]
        self.size = 35  # Size of the treasure (increased from 20)
        self.rotation = 0  # For animation
        # Animation parameters
        self.float_offset = 0
        self.float_speed = 0.05

    def update(self):
        # Rotate the treasure
        self.rotation = (self.rotation + 1) % 360
        # Make the treasure float up and down
        self.float_offset = 5 * math.sin(glutGet(GLUT_ELAPSED_TIME) * 0.001 + self.pos[0] * 0.1)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2] + self.float_offset)
        glRotatef(self.rotation, 0, 0, 1)

        # Draw a treasure chest
        glColor3f(0.6, 0.4, 0.1)  # Brown for chest base

        # Base of the chest
        glPushMatrix()
        glScalef(self.size, self.size * 0.7, self.size * 0.5)
        glutSolidCube(1)
        glPopMatrix()

        # Lid of the chest
        glPushMatrix()
        glTranslatef(0, 0, self.size * 0.25)
        glColor3f(0.8, 0.6, 0.2)  # Lighter brown for lid
        glScalef(self.size, self.size * 0.7, self.size * 0.25)
        glutSolidCube(1)
        glPopMatrix()

        # Gold details (some gold coins/jewelry visible)
        glPushMatrix()
        glTranslatef(0, 0, self.size * 0.5)
        glColor3f(1.0, 0.84, 0.0)  # Gold color
        gluSphere(gluNewQuadric(), self.size * 0.2, 10, 10)
        glPopMatrix()

        glPopMatrix()


def initialize_ghosts(num_ghosts):
    global ghosts
    ghosts = []
    for _ in range(num_ghosts):
        # pick one of your spawn zones at random
        xmin, xmax, ymin, ymax = random.choice(spawn_zones)
        x = random.uniform(xmin, xmax)
        y = random.uniform(ymin, ymax)
        z = 0
        angle = random.uniform(0, 360)
        ghosts.append(Ghost(x, y, z, angle))


def initialize_treasures(num_treasures):
    global treasures
    treasures = []

    # only keep the “room” zones: chop off the first 3 and the last 2
    room_zones = spawn_zones[3: -2]

    MARGIN = 50  # so treasures don’t hug a wall exactly

    for _ in range(num_treasures):
        xmin, xmax, ymin, ymax = random.choice(room_zones)
        x = random.uniform(xmin + MARGIN, xmax - MARGIN)
        y = random.uniform(ymin + MARGIN, ymax - MARGIN)
        z = 50

        # keep it at least 200 units from the player
        dx, dy = x - man_pos[0], y - man_pos[1]
        if math.hypot(dx, dy) < 200:
            sign_x = 1 if dx >= 0 else -1
            sign_y = 1 if dy >= 0 else -1
            x = max(min(x + sign_x * 200, xmax - MARGIN), xmin + MARGIN)
            y = max(min(y + sign_y * 200, ymax - MARGIN), ymin + MARGIN)

        treasures.append(Treasure(x, y, z))


def respawn_ghost(ghost_index):
    """Respawns a ghost at a random location far from the player."""
    global ghosts, man_pos

    # Get the current player position
    px, py = man_pos[0], man_pos[1]

    # Choose a random position that's far from the player (at least half the grid size away)
    min_distance = GRID_LENGTH * 0.7

    while True:
        # Generate a completely random position
        x = random.uniform(-GRID_LENGTH * 0.9, GRID_LENGTH * 0.9)
        y = random.uniform(-GRID_LENGTH * 0.9, GRID_LENGTH * 0.9)

        # Calculate distance from player
        distance = math.sqrt((x - px) ** 2 + (y - py) ** 2)

        # If it's far enough away, use this position
        if distance > min_distance:
            break

    z = 0  # All ghosts start at ground level
    angle = random.randint(0, 360)  # Random angle for direction

    # Update ghost position
    ghosts[ghost_index].pos = [x, y, z]
    ghosts[ghost_index].angle = angle
    ghosts[ghost_index].scale = 1.0  # Reset scale
    ghosts[ghost_index].scale_dir = 1  # Start expanding


# Move lasers and check for collision with ghosts
def move_lasers():
    global ghosts, man_pos, boss
    for laser in lasers[:]:  # Use a copy to avoid modification during iteration
        laser_speed = 10
        angle_rad = math.radians(laser['angle'])
        laser['x'] += math.sin(angle_rad) * laser_speed
        laser['y'] += math.cos(angle_rad) * laser_speed

        # Check if any laser hits a ghost
        for i, ghost in enumerate(ghosts):
            if ghost.is_hit_by_laser(laser):
                print("Ghost hit! Respawning...")
                respawn_ghost(i)  # Respawn ghost at a new random location
                lasers.remove(laser)  # Remove the laser after hit
                break  # One laser can only hit one ghost

        if boss.alive:
            dx = laser['x'] - boss.pos[0]
            dy = laser['y'] - boss.pos[1]
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 100:
                print("Laser hit the boss!")
                boss.take_damage(10)
                lasers.remove(laser)
                break


def check_treasure_collision():
    global treasures, score, man_pos

    # Player collision radius (approximating the character's body)
    player_radius = 25

    # Check each treasure
    for treasure in treasures[:]:  # Use a copy to safely modify during iteration
        # Calculate distance between player and treasure
        distance = math.sqrt((man_pos[0] - treasure.pos[0]) ** 2 +
                             (man_pos[1] - treasure.pos[1]) ** 2)

        # If collision detected
        if distance < (player_radius + treasure.size):
            treasures.remove(treasure)  # Remove the collected treasure
            score += 1  # Increase score
            print(f"Treasure collected! Score: {score}")
            print(f"Remaining treasures: {len(treasures)}")


def draw_lasers():
    glColor3f(1, 0, 0)  # Red lasers
    glLineWidth(4)
    glBegin(GL_LINES)
    for laser in lasers:
        x, y, z = laser['x'], laser['y'], laser['z']
        angle_rad = math.radians(laser['angle'])
        glVertex3f(x, y, z)
        glVertex3f(x + math.sin(angle_rad) * 20, y + math.cos(angle_rad) * 20, z)
    glEnd()


def boss_room(offset_x=0, offset_y=0,
              room_w=400, room_h=700,
              door_side='north',  # 'north','south','east' or 'west'
              door_center=0,  # center-of-gap along that wall
              door_width=120.0):
    """
    Boss Room: stone floor (no wood), walls with a single door on any side,
    plus a big boss arena.  You can reposition and resize via the parameters.
    """
    H = 250  # wall height
    T = 5  # wall thickness

    glPushMatrix()
    glTranslatef(offset_x, offset_y, 0)

    # 1) stone floor (instead of wood)
    STEP = 40
    LIGHT = (0.6, 0.6, 0.6)
    DARK = (0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    for x in range(-room_w, room_w, STEP):
        for y in range(-room_h, room_h, STEP):
            shade = ((x // STEP + y // STEP) & 1)
            glColor3f(*(LIGHT if shade else DARK))
            glVertex3f(x, y, 0)
            glVertex3f(x + STEP, y, 0)
            glVertex3f(x + STEP, y + STEP, 0)
            glVertex3f(x, y + STEP, 0)
    glEnd()

    # 2) walls w/ parametric door
    glColor3f(0.2, 0.1, 0.1)
    half_x = (2 * room_w - door_width) / 2  # span for north/south segments
    half_y = (2 * room_h - door_width) / 2  # span for east/west  segments

    def W(tx, ty, sx, sy):
        glPushMatrix()
        glTranslatef(tx, ty, H / 2)
        glScalef(sx, sy, H)
        glutSolidCube(1)
        glPopMatrix()
        add_wall(offset_x + tx, offset_y + ty, sx, sy)

    # north
    if door_side == 'north':
        W(door_center - door_width / 2 - half_x / 2, room_h, half_x, T)
        W(door_center + door_width / 2 + half_x / 2, room_h, half_x, T)
    else:
        W(0, room_h, 2 * room_w, T)
    # south
    if door_side == 'south':
        W(door_center - door_width / 2 - half_x / 2, -room_h, half_x, T)
        W(door_center + door_width / 2 + half_x / 2, -room_h, half_x, T)
    else:
        W(0, -room_h, 2 * room_w, T)
    # east
    if door_side == 'east':
        W(room_w, door_center - door_width / 2 - half_y / 2, T, half_y)
        W(room_w, door_center + door_width / 2 + half_y / 2, T, half_y)
    else:
        W(room_w, 0, T, 2 * room_h)
    # west
    if door_side == 'west':
        W(-room_w, door_center - door_width / 2 - half_y / 2, T, half_y)
        W(-room_w, door_center + door_width / 2 + half_y / 2, T, half_y)
    else:
        W(-room_w, 0, T, 2 * room_h)
    # 3) you can add boss props here (arena pillars, lava pits, etc.)
    glPopMatrix()


# helper to spawn boss shots
def spawn_boss_projectile(pos, angle):
    enemy_projectiles.append({
        'x': pos[0],
        'y': pos[1],
        'z': pos[2] + 50,
        'angle': math.degrees(angle)
    })


# advance boss projectiles & hit player
def move_enemy_projectiles():
    global player_life, game_over
    speed = 8
    for p in enemy_projectiles[:]:
        a = math.radians(p['angle'])
        p['x'] += math.sin(a) * speed
        p['y'] += math.cos(a) * speed
        # out of bounds?
        if abs(p['x']) > GRID_LENGTH or abs(p['y']) > GRID_LENGTH:
            enemy_projectiles.remove(p)
            continue
        # hit player?
        if math.hypot(p['x'] - man_pos[0], p['y'] - man_pos[1]) < 25:
            enemy_projectiles.remove(p)
            player_life -= 1
            if player_life <= 0:
                game_over = True


def draw_enemy_projectiles():
    glColor3f(1, 1, 0)  # yellow boss shots
    glLineWidth(4)
    glBegin(GL_LINES)
    for p in enemy_projectiles:
        a = math.radians(p['angle'])
        glVertex3f(p['x'], p['y'], p['z'])
        glVertex3f(p['x'] + math.sin(a) * 20, p['y'] + math.cos(a) * 20, p['z'])
    glEnd()


# --- BOSS CLASS ---
class Boss:
    def __init__(self, x, y, z=0):
        self.pos = [x, y, z]
        self.health = 200
        self.alive = True
        self.hit_cooldown = 0.0
        self.attack_timer = 0.0
        self.attack_interval = 120
        # scale for pulsation
        self.scale = 1.0
        self.scale_dir = 1
        self.scale_speed = 0.002
        self.scale_min = 0.9
        self.scale_max = 1.1

        self.speed = 1

    def update(self, player_pos):
        if not (self.alive and boss_fight_active): return

        # chase
        dx, dy = player_pos[0] - self.pos[0], player_pos[1] - self.pos[1]
        d = math.hypot(dx, dy)
        if d > 1:
            self.pos[0] += dx / d * self.speed
            self.pos[1] += dy / d * self.speed

        # cooldowns...
        if self.hit_cooldown > 0: self.hit_cooldown -= 1
        self.attack_timer += 1
        if self.attack_timer >= self.attack_interval:
            angle = math.atan2(player_pos[1] - self.pos[1],
                               player_pos[0] - self.pos[0])
            spawn_boss_projectile(self.pos, angle)
            self.attack_timer = 0

    def attack(self, player_pos):
        # implement later…
        pass

    def take_damage(self, amount):
        if self.hit_cooldown > 0 or not self.alive:
            return
        self.health -= amount
        self.hit_cooldown = 0.5
        if self.health <= 0:
            self.die()

    def die(self):
        self.alive = False
        global victory
        victory = True

    def draw(self):
        if not self.alive:
            return
        glPushMatrix()
        # move to boss center
        glTranslatef(self.pos[0], self.pos[1], self.pos[2] + 90)
        # make the head huge and scary
        head_radius = 100.0
        glColor3f(0.5, 0.0, 0.0)  # dark red head
        gluSphere(gluNewQuadric(), head_radius, 32, 32)

        # —— HORNS —— two white cones on top
        glColor3f(1.0, 1.0, 1.0)
        for x_off in (-40, +40):
            glPushMatrix()
            glTranslatef(x_off, 0, head_radius + 50)  # sit on top
            glRotatef(180, 1, 0, 0)  # point upward
            gluCylinder(gluNewQuadric(), 0.0, 20, 60, 16, 4)
            glPopMatrix()

        # —— FANGS —— two white cones at front
        glColor3f(1.0, 1.0, 1.0)
        for x_off in (-80, +80):
            glPushMatrix()
            glTranslatef(x_off, head_radius * 0.8, head_radius * 0.2)
            glRotatef(75, 1, 0, 0)  # tilt downward
            gluCylinder(gluNewQuadric(), 0.0, 10, 30, 12, 4)
            glPopMatrix()

        # —— Eyes —— glowing black orbs
        glColor3f(0.0, 0.0, 0.0)
        for x_off in (-60, +60):
            glPushMatrix()
            glTranslatef(x_off, head_radius * 0.6, head_radius * 0.4)
            gluSphere(gluNewQuadric(), 15, 12, 12)
            glPopMatrix()

        glPopMatrix()


boss = Boss(2650, -400, 0)


def reset_game():
    global man_pos, man_angle, player_life, score, treasures, lasers, ghosts, game_over

    # Reset character position and angle
    man_pos = [0, 0, 0]  # Reset player position
    man_angle = 0  # Reset player angle

    # Reset player life and score
    player_life = 5
    score = 0

    # Clear lasers and ghosts
    lasers = []
    ghosts = []

    # Initialize the ghosts and treasures again
    initialize_ghosts(10)  # Reset 10 ghosts
    initialize_treasures(5)  # Reset 5 treasures

    # Reset the game over state
    game_over = False

    print("Game restarted!")


def keyboardListener(key, x, y):
    global keys_pressed, jumping, jump_velocity, cheat_mode
    keys_pressed.add(key)

    # Jump functionality (spacebar)
    if key == b' ' and not jumping:
        jumping = True
        jump_velocity = 10

    # Toggle cheat mode (C/c)
    if key == b'c' or key == b'C':
        cheat_mode = not cheat_mode

    # Restart game (R)
    if key == b'r' or key == b'R':
        reset_game()  # Call the reset function when R is pressed


def keyboardUpListener(key, x, y):
    if key in keys_pressed:
        keys_pressed.remove(key)


def specialKeyListener(key, x, y):
    global camera_pos
    x, y, z = camera_pos
    if key == GLUT_KEY_LEFT:
        x -= 1
    elif key == GLUT_KEY_RIGHT:
        x += 1
    camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    global first_person_mode, lasers

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Angle based on character's current orientation
        angle_rad = math.radians(man_angle)
        laser_x = man_pos[0] + math.sin(angle_rad) * 23  # Position laser at character's front
        laser_y = man_pos[1] + math.cos(angle_rad) * 23
        laser_z = man_pos[2] + 50  # Slightly above the player for better visibility
        lasers.append({'x': laser_x, 'y': laser_y, 'z': laser_z, 'angle': man_angle})
        print("Laser Fired!")  # Add a print statement to confirm laser creation

    # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person_mode = not first_person_mode


def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    global first_person_mode

    if first_person_mode:
        eye_x = man_pos[0]
        eye_y = man_pos[1]
        eye_z = man_pos[2] + 95

        angle_rad = math.radians(man_angle)
        forward_offset = 15  # Move camera a bit forward

        eye_x += math.sin(angle_rad) * forward_offset
        eye_y += math.cos(angle_rad) * forward_offset

        center_x = eye_x + math.sin(angle_rad)
        center_y = eye_y + math.cos(angle_rad)
        center_z = eye_z

        gluLookAt(eye_x, eye_y, eye_z, center_x, center_y, center_z, 0, 0, 1)
    else:
        # Third-person chase-cam: always follow the player from behind & above
        angle_rad = math.radians(man_angle)
        back_dist = 260.0  # how far behind the player
        height = 260.0  # how high above the player

        # camera position = player pos minus a vector behind them
        eye_x = man_pos[0] - math.sin(angle_rad) * back_dist
        eye_y = man_pos[1] - math.cos(angle_rad) * back_dist
        eye_z = man_pos[2] + height

        # look at the player's head
        center_x = man_pos[0]
        center_y = man_pos[1]
        center_z = man_pos[2] + 80.0

        gluLookAt(
            eye_x, eye_y, eye_z,
            center_x, center_y, center_z,
            0, 0, 1
        )


def idle():
    global man_pos, jumping, jump_velocity, man_angle, lasers, game_over
    global boss_fight_active

    if game_over or victory:
        return

    step = man_speed
    angle_rad = math.radians(man_angle)
    move_lasers()
    # Calculate next position (for collision check)
    dx = dy = 0
    if b'w' in keys_pressed:
        dx += math.sin(angle_rad) * step
        dy += math.cos(angle_rad) * step
    if b's' in keys_pressed:
        dx -= math.sin(angle_rad) * step
        dy -= math.cos(angle_rad) * step
    if b'a' in keys_pressed:
        man_angle -= 2
    if b'd' in keys_pressed:
        man_angle += 2

    # Check boundaries before applying position
    if not cheat_mode:
        new_x = man_pos[0] + dx
        new_y = man_pos[1] + dy
        blocked = False
        for xmin, xmax, ymin, ymax in collision_walls:
            if xmin <= new_x <= xmax and ymin <= new_y <= ymax:
                blocked = True
                break
        if not blocked:
            man_pos[0] = new_x
            man_pos[1] = new_y
        # else: do nothing (player stays in place)
    else:
        # In cheat mode, ignore wall collision
        man_pos[0] += dx
        man_pos[1] += dy

    # Optional: Q/E for up/down (no collision needed for Z)
    if b'q' in keys_pressed:
        man_pos[2] += step
    if b'e' in keys_pressed:
        man_pos[2] -= step

    # Jumping
    if jumping:
        man_pos[2] += jump_velocity
        jump_velocity -= 1
        if man_pos[2] <= 0:
            man_pos[2] = 0
            jumping = False
            jump_velocity = 0

    # Move lasers and check for collision
    move_lasers()

    # Update ghost scaling animation and movement
    if not game_over:
        for i, ghost in enumerate(ghosts):
            ghost.update_scale()
            ghost.move_towards_player(man_pos)
            if not cheat_mode:
                # Check collision with player
                player_radius = 25
                ghost_radius = ghost.body_radius_bottom
                dx = man_pos[0] - ghost.pos[0]
                dy = man_pos[1] - ghost.pos[1]
                distance = math.sqrt(dx * dx + dy * dy)
                if distance < (player_radius + ghost_radius):
                    global player_life
                    player_life -= 1
                    print(f"Player hit by ghost! Remaining life: {player_life}")
                    respawn_ghost(i)
                    if player_life <= 0:
                        game_over = True
                        print("Game Over!")

    # Update treasures and check for collisions
    for treasure in treasures:
        treasure.update()
    check_treasure_collision()

    # boss
    move_lasers()
    move_enemy_projectiles()

    # open the door AND start boss fight if ready
    if score >= 5 and not boss_fight_active:
        # if player is at the door opening to boss
        bx, by = 2200, -400
        if abs(man_pos[0] - bx) < 50 and abs(man_pos[1] - by) < 50:
            boss_fight_active = True

    boss.update(man_pos)
    # boss–player collision
    if boss_fight_active and boss.alive and not cheat_mode:
        dx = man_pos[0] - boss.pos[0]
        dy = man_pos[1] - boss.pos[1]
        # approximate boss radius = head_radius (100)
        if math.hypot(dx, dy) < 100 + 25:  # 25 = player radius
            player_life -= 1
            print("Hit by boss! Life=", player_life)
            # optional: knock player back or add cooldown here
            if player_life <= 0:
                game_over = True

    glutPostRedisplay()


def showScreen():
    collision_walls.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    room1()
    draw_hallway()
    room2(offset_x=0, offset_y=-900,
          door_side='north',  # 'north','south','east' or 'west'
          door_center=0,  # offset along the wall axis, in world units
          door_width=120.0)

    room2(offset_x=600, offset_y=0,
          door_side='south',  # 'north','south','east' or 'west'
          door_center=0,  # offset along the wall axis, in world units
          door_width=120.0)

    room3(offset_x=500, offset_y=-900, room_w=300, room_h=300,
          door_side='north', door_center=50, door_width=120.0)

    room3(offset_x=1400, offset_y=0, room_w=500, room_h=300,
          door_side='south', door_center=50, door_width=120.0)

    room3(offset_x=1300, offset_y=-900, room_w=500, room_h=300,
          door_side='north', door_center=50, door_width=120.0)

    room3(offset_x=2000, offset_y=-900, room_w=200, room_h=300,
          door_side='north', door_center=50, door_width=120.0)

    boss_room(offset_x=2500, offset_y=-400, room_w=300, room_h=700,
              door_side='west', door_center=0, door_width=120)

    # invisible blockade until you’ve got all 5
    if score < 5:
        add_wall(2200, -400, 100, 100)

    draw_man()
    # Draw the ghosts
    for ghost in ghosts:
        ghost.draw()

    # Draw treasures
    for treasure in treasures:
        treasure.draw()

    # Draw lasers (if any)
    draw_lasers()

    # draw boss
    boss.draw()
    # Display some text
    draw_text(10, 770, "Haunted Mansion - Left-Click to shoot lasers!")
    draw_text(10, 740, f"Score: {score}/5 treasures collected")
    draw_text(10, 710, f"Player Life: {player_life}")
    if boss_fight_active:
        draw_text(10, 680, f"Boss Health: {boss.health}")
    if victory:
        draw_text(400, 400, "YOU WIN!")
    if game_over:
        draw_text(400, 400, "GAME OVER", font=GLUT_BITMAP_HELVETICA_18)

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"3D OpenGL Haunted Mansion")

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutKeyboardUpFunc(keyboardUpListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glEnable(GL_DEPTH_TEST)
    initialize_ghosts(10)  # Always 10 ghosts
    initialize_treasures(5)  # 5 treasures to collect
    glutMainLoop()


if __name__ == "__main__":
    main()
