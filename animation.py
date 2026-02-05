"""
Rotating Windmill Simulation
A computer graphics project demonstrating 2D/3D transformations and animation
using Python and PyOpenGL
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Global variables
rotation_angle = 0.0
rotation_speed = 2.0
is_paused = False
windmill_scale = 1.0
window_width = 800
window_height = 600

def init():
    """Initialize OpenGL settings"""
    glClearColor(0.53, 0.81, 0.92, 1.0)  # Sky blue background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-400, 400, -300, 300)
    glMatrixMode(GL_MODELVIEW)

def draw_circle(x, y, radius, segments=50):
    """Draw a filled circle using triangle fan"""
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(segments + 1):
        angle = 2.0 * math.pi * i / segments
        dx = radius * math.cos(angle)
        dy = radius * math.sin(angle)
        glVertex2f(x + dx, y + dy)
    glEnd()

def draw_rectangle(x, y, width, height):
    """Draw a filled rectangle"""
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

def draw_blade():
    """Draw a single windmill blade"""
    # Blade body (trapezoid shape)
    glColor3f(0.9, 0.9, 0.9)  # Light gray
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(15, 5)
    glVertex2f(120, 20)
    glVertex2f(120, -20)
    glEnd()
    
    # Blade tip
    glBegin(GL_TRIANGLES)
    glVertex2f(120, 20)
    glVertex2f(120, -20)
    glVertex2f(140, 0)
    glEnd()

def draw_windmill():
    """Draw the complete windmill structure"""
    # Apply scaling transformation
    glPushMatrix()
    glScalef(windmill_scale, windmill_scale, 1.0)
    
    # Draw tower (main structure)
    glColor3f(0.6, 0.4, 0.2)  # Brown color
    draw_rectangle(-30, -250, 60, 200)
    
    # Tower top (wider base)
    glBegin(GL_QUADS)
    glVertex2f(-40, -50)
    glVertex2f(40, -50)
    glVertex2f(30, -30)
    glVertex2f(-30, -30)
    glEnd()
    
    # Draw rotating blades
    glPushMatrix()
    glTranslatef(0, 0, 0)  # Center position for blades
    glRotatef(rotation_angle, 0, 0, 1)  # Rotate around z-axis
    
    # Draw 4 blades at 90-degree intervals
    for i in range(4):
        glPushMatrix()
        glRotatef(i * 90, 0, 0, 1)
        draw_blade()
        glPopMatrix()
    
    glPopMatrix()
    
    # Draw center hub
    glColor3f(0.3, 0.3, 0.3)  # Dark gray
    draw_circle(0, 0, 20)
    
    # Draw center circle (decorative)
    glColor3f(0.5, 0.5, 0.5)  # Medium gray
    draw_circle(0, 0, 12)
    
    glPopMatrix()

def draw_ground():
    """Draw ground/base"""
    glColor3f(0.2, 0.6, 0.2)  # Green grass
    glBegin(GL_QUADS)
    glVertex2f(-400, -300)
    glVertex2f(400, -300)
    glVertex2f(400, -250)
    glVertex2f(-400, -250)
    glEnd()

def draw_clouds():
    """Draw decorative clouds"""
    glColor3f(1.0, 1.0, 1.0)  # White
    
    # Cloud 1
    draw_circle(-250, 200, 25)
    draw_circle(-230, 210, 30)
    draw_circle(-210, 200, 25)
    
    # Cloud 2
    draw_circle(200, 180, 30)
    draw_circle(230, 190, 35)
    draw_circle(260, 180, 30)

def draw_sun():
    """Draw sun"""
    glColor3f(1.0, 0.9, 0.0)  # Yellow
    draw_circle(300, 220, 40)

def draw_text(x, y, text):
    """Draw text on screen"""
    glColor3f(0.0, 0.0, 0.0)  # Black text
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def display():
    """Main display function"""
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    # Draw scene elements
    draw_sun()
    draw_clouds()
    draw_ground()
    draw_windmill()
    
    # Display controls
    draw_text(-380, 270, "Controls:")
    draw_text(-380, 250, "SPACE - Pause/Resume")
    draw_text(-380, 230, "UP - Increase Speed")
    draw_text(-380, 210, "DOWN - Decrease Speed")
    draw_text(-380, 190, "L - Increase Size")
    draw_text(-380, 170, "S - Decrease Size")
    draw_text(-380, 150, "R - Reset")
    draw_text(-380, 130, "ESC - Exit")
    
    # Display status
    status = "PAUSED" if is_paused else "RUNNING"
    draw_text(230, 270, f"Status: {status}")
    draw_text(230, 250, f"Speed: {rotation_speed:.1f}")
    draw_text(230, 230, f"Scale: {windmill_scale:.2f}x")
    
    glutSwapBuffers()

def update(value):
    """Update animation (called every frame)"""
    global rotation_angle
    
    if not is_paused:
        rotation_angle += rotation_speed
        if rotation_angle >= 360:
            rotation_angle -= 360
    
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)  # ~60 FPS

def keyboard(key, x, y):
    """Handle keyboard input"""
    global rotation_speed, is_paused, rotation_angle, windmill_scale
    
    if key == b' ':  # Spacebar - pause/resume
        is_paused = not is_paused
    elif key == b'l' or key == b'L':  # Increase size
        windmill_scale = min(windmill_scale + 0.1, 3.0)
    elif key == b's' or key == b'S':  # Decrease size
        windmill_scale = max(windmill_scale - 0.1, 0.2)
    elif key == b'r' or key == b'R':  # Reset
        rotation_angle = 0.0
        rotation_speed = 2.0
        windmill_scale = 1.0
        is_paused = False
    elif key == b'\x1b':  # ESC - exit
        exit(0)
    
    glutPostRedisplay()

def special_keys(key, x, y):
    """Handle special keyboard keys"""
    global rotation_speed
    
    if key == GLUT_KEY_UP:  # Increase speed
        rotation_speed = min(rotation_speed + 0.5, 10.0)
    elif key == GLUT_KEY_DOWN:  # Decrease speed
        rotation_speed = max(rotation_speed - 0.5, 0.0)
    
    glutPostRedisplay()

def reshape(width, height):
    """Handle window reshape"""
    global window_width, window_height
    window_width = width
    window_height = height
    glViewport(0, 0, width, height)

def main():
    """Main function to initialize and run the program"""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Rotating Windmill Simulation - COMP 342")
    
    init()
    
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutTimerFunc(0, update, 0)
    
    print("=== Rotating Windmill Simulation ===")
    print("Controls:")
    print("  SPACE    - Pause/Resume animation")
    print("  UP/DOWN  - Increase/Decrease rotation speed")
    print("  L        - Increase windmill size")
    print("  S        - Decrease windmill size")
    print("  R        - Reset animation")
    print("  ESC      - Exit program")
    print("\nProject by: Siddhanta Sapkota & Suraj Sharma Paudel")
    print("Course: COMP 342 - Computer Graphics")
    
    glutMainLoop()

if __name__ == "__main__":
    main()