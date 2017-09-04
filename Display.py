#! /usr/bin/python

import pyglet
import math

from pyglet.gl import *
from pyglet.window import NoSuchConfigException

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
    template = pyglet.gl.Config(
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

fps_display = pyglet.clock.ClockDisplay()


class Circles():
    def __init__(self):
        self.circles = []

    def createCircle(self, p_x, p_y, p_r, p_num_points=12):
        verts = [p_x, p_y]
        two_pi = math.pi * 2
        seg_size = two_pi / p_num_points
        for i in range(p_num_points):
            x = math.sin(i * seg_size) * p_r + p_x
            y = math.cos(i * seg_size) * p_r + p_y
            verts += [x, y]

        indices = [i for i in range(p_num_points + 1)]
        indices.append(1)

        circle = pyglet.graphics.vertex_list_indexed(
            len(verts) // 2,
            indices,
            ('v2f', verts)
        )

        self.circles.append(circle)

    def draw(self):
        if len(self.circles) < 1:
            return

        for circle in self.circles:
            circle.draw(GL_TRIANGLE_FAN)


circles = Circles()

circles.createCircle(300, 300, 10)
circles.createCircle(500, 300, 10)


@window.event
def on_draw():
    window.clear()

    circles.draw()

    fps_display.draw()


pyglet.app.run()
