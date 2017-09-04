#! /usr/bin/python

import pyglet

from pyglet.window import NoSuchConfigException

from pyglet.gl import *

fps_display = pyglet.clock.ClockDisplay()

def onDrawHandler():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glDrawArrays(GL_TRIANGLES, 0, len(vertices) // 3)

    pyglet.graphics.draw(
        2,
        pyglet.gl.GL_POINTS,
        ('v2i', (10, 15, 30, 35)),
        ('c3B', (0, 0, 255, 0, 255, 0))
    )

    pyglet.graphics.draw(
        2,
        pyglet.gl.GL_POINTS,
        ('v3f', (10.0, 17.5, 0.0, 30.0, 37.5, 0.0))
    )

    pyglet.graphics.draw_indexed(
        4,
        pyglet.gl.GL_TRIANGLES,
        [0, 1, 2, 0, 2, 3],
        ('v2i', (100, 100,
                 150, 100,
                 150, 150,
                 100, 150))
    )

    vertex_list = pyglet.graphics.vertex_list(
        3,
        ('v2i', (10, 150,
                 30, 350,
                 30, 150)),
        ('c3B', (255, 0, 255,
                 255, 255, 0,
                 0, 255, 255))
    )
    vertex_list.draw(pyglet.gl.GL_TRIANGLES)

    fps_display.draw()

def onResizeHandler(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65, width / float(height), .1, 1000)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED


# This describes the system we;re running on
platform = pyglet.window.get_platform()
# This gets the default display device (e.g.: graphics card)
display = platform.get_default_display()
screen = display.get_default_screen()
# Check if we can find a right most screen
for available_screen in display.get_screens():
    if available_screen.x != 0:
        screen = available_screen

try:
    # try to employ multisampling
    template = Config(
        sample_buffers=1,
        samples=4,
        alpha_size=8
    )
    config = screen.get_best_config(template)
    print("Using multisampling")
except NoSuchConfigException:
    template = pyglet.gl.Config()
    config = screen.get_best_config(template)
    print("resort to best default config")

context = config.create_context(None)
window = pyglet.window.Window(
    context=context,
    fullscreen=True
)

full_width = window.width
quarter_width = full_width // 4
half_width = full_width // 2

full_height = window.height
half_height = full_height // 2
quarter_height = full_height // 4
three_quarter_height = 3 * quarter_height

vertices = [
    0, 0, 0,
    full_width, 0, 0,
    half_width, half_height, 0,
    quarter_width, quarter_height, 0,
    quarter_width, three_quarter_height, 0,
    half_width, half_height, 0
]

vertices_gl = (GLfloat * len(vertices))(*vertices)

glEnableClientState(GL_VERTEX_ARRAY)
glVertexPointer(3, GL_FLOAT, 0, vertices_gl)

window.on_draw = onDrawHandler
# window.on_resize = onResizeHandler

pyglet.app.run()
