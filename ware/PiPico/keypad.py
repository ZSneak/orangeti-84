import usb_hid
import board
import keypad
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

row_pins = (board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12, board.GP13)
col_pins = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4)

dir_pins = (board.GP14, board.GP15, board.GP16, board.GP17)

keymap_num = 1

def GetCurrentKeymap(numb = 1):
    if numb == 1:
        return [
            Keycode.F1, Keycode.F2, Keycode.F3, Keycode.F4, Keycode.F5,
            Keycode.LEFT_SHIFT, Keycode.ESCAPE, Keycode.RIGHT_SHIFT, None, None,
            Keycode.CONTROL, Keycode.EQUALS, Keycode.END, None, None,
            Keycode.HOME, Keycode.PAGE_UP, Keycode.PAGE_DOWN, Keycode.INSERT, Keycode.DELETE,
            Keycode.D, Keycode.E, Keycode.F, Keycode.G, Keycode.H,
            Keycode.I, Keycode.J, Keycode.K, Keycode.L, Keycode.FORWARD_SLASH,
            Keycode.N, Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE, Keycode.KEYPAD_ASTERISK,
            Keycode.S, Keycode.FOUR, Keycode.FIVE, Keycode.SIX, Keycode.MINUS,
            Keycode.X, Keycode.ONE, Keycode.TWO, Keycode.THREE, Keycode.KEYPAD_PLUS,
            Keycode.F12, Keycode.ZERO, Keycode.PERIOD, Keycode.MINUS, Keycode.GRAVE_ACCENT #in the software make sure to add the grave accent to underscore conversion
            ]
    if numb == 2:
        return [None]
    else:
        raise ValueError("current keymap is not one or two twinium")


# initialization or something i guess maybe

kbd = Keyboard(usb_hid.devices)

matrix = keypad.KeyMatrix(row_pins, col_pins, columns_to_anodes=True)

print(f"guys the keyboard is ready with a {len(row_pins)} by {len(col_pins)} matrix.")

# loooooooooop

while True:
    thing = matrix.events.get()
    if thing:
        sendything = (getCurrentKeymap(keymap_num))[thing.key_number]

        if thing.pressed:
            kbd.press(keycode)
        if thing.released:
            kbd.release(keycode)