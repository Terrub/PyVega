#! /usr/bin/python

import pyglet

from pyglet.window import key, NoSuchConfigException


def onKeyPressHandler(p_key, p_mods):
    """
    :param p_key:
    :param p_mods:
    """
    format_str = 'Key pressed: "{}" mods: {}'
    char = key.symbol_string(p_key)
    label.text = format_str.format(char, p_mods)


def onDrawHandler():
    window.clear()
    label.x = window.width // 2
    label.y = 0 + label.content_height
    label.draw()

    image.blit(window.width // 2, window.height // 2)


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
# window.push_handlers(pyglet.window.event.WindowEventLogger())
window.on_key_press = onKeyPressHandler
window.on_draw = onDrawHandler

image = pyglet.resource.image('StN_logo.jpg')

label = pyglet.text.Label(
    text='Press a key',
    font_name='Times New Roman',
    font_size=36,
    anchor_x='center',
    anchor_y='top'
)

pyglet.app.run()
