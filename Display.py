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


class Circle():
    def __init__(self, p_x, p_y, p_radius, p_num_points=12):
        self.x = p_x
        self.y = p_y
        self.radius = p_radius
        self.num_points = p_num_points

        indices = [i for i in range(self.num_points + 1)]
        indices.append(1)

        self.__vertex_list_indexed = pyglet.graphics.vertex_list_indexed(
            self.num_points + 1,  # number of points + the centre point
            indices,
            'v2f'
        )

    def draw(self):
        self.vertex_list_indexed.draw(GL_TRIANGLE_FAN)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value
        self.__vertext_list_outdated = True

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value
        self.__vertext_list_outdated = True

    @property
    def vertex_list_indexed(self):
        if self.__vertext_list_outdated:
            # print("outdated vertex list, recalculating")
            x = self.x
            y = self.y
            r = self.radius
            n = self.num_points

            verts = [x, y]
            two_pi = math.pi * 2
            seg_size = two_pi / n
            for i in range(n):
                x = math.sin(i * seg_size) * r + x
                y = math.cos(i * seg_size) * r + y
                verts += [x, y]

            self.__vertex_list_indexed.vertices = verts
            self.__vertext_list_outdated = False

        return self.__vertex_list_indexed


class Circles():
    def __init__(self):
        self.circles = []

    def draw(self):
        if len(self.circles) < 1:
            return

        for circle in self.circles:
            circle.draw()

    def add(self, p_circle):
        self.circles.append(p_circle)


circles = Circles()

circle1 = Circle(0, 0, 3)
circles.add(circle1)
# circles.add(Circle(500, 300, 10))


@window.event
def on_draw():
    window.clear()

    circles.draw()

    fps_display.draw()

from pyglet.window import key

@window.event
def on_key_release(p_key, p_mods):
    if p_key == key.LEFT:
        circle1.x -= 10
    elif p_key == key.RIGHT:
        circle1.x += 10

@window.event
def on_mouse_motion(x, y, dx, dy):
    circle1.x += dx
    circle1.y += dy

# window.push_handlers(pyglet.window.event.WindowEventLogger())
# window.set_mouse_visible(False)
window.set_exclusive_mouse(True)

pyglet.app.run()
