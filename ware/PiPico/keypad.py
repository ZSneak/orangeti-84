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
            
        ]
    if numb == 2:
        return
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