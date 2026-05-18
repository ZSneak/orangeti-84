from machine import Pin
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# --- 1. INITIALIZE USB KEYBOARD ---
kbd = Keyboard(usb_hid.devices)

# --- 2. PIN CONFIGURATION ---
ROW_PINS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]      
COL_PINS = [10, 11, 12, 13, 14]                
BTN_PINS = [15, 16, 17, 18]                 

rows = [Pin(pin, Pin.OUT, value=1) for pin in ROW_PINS]
cols = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in COL_PINS]
buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in BTN_PINS]

# --- 3. THE KEYMAP LAYOUT ---
# Map your 10x5 matrix intersections to actual USB Keyboard keys.
# Adjust these Keycodes to match the actual layout of your TI-84 layout!
MATRIX_KEYMAP = [
    # Col 0          Col 1          Col 2          Col 3          Col 4
    [Keycode.ONE,   Keycode.TWO,   Keycode.THREE, Keycode.FOUR,  Keycode.FIVE],  # Row 0
    [Keycode.SIX,   Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE,  Keycode.ZERO],  # Row 1
    [Keycode.A,     Keycode.B,     Keycode.C,     Keycode.D,     Keycode.E],     # Row 2
    [Keycode.F,     Keycode.G,     Keycode.H,     Keycode.I,     Keycode.J],     # Row 3
    [Keycode.K,     Keycode.L,     Keycode.M,     Keycode.N,     Keycode.O],     # Row 4
    [Keycode.P,     Keycode.Q,     Keycode.R,     Keycode.S,     Keycode.T],     # Row 5
    [Keycode.U,     Keycode.V,     Keycode.W,     Keycode.X,     Keycode.Y],     # Row 6
    [Keycode.Z,     Keycode.ENTER, Keycode.SPACE, Keycode.BACKSPACE, Keycode.ESCAPE], # Row 7
    [Keycode.UP_ARROW, Keycode.DOWN_ARROW, Keycode.LEFT_ARROW, Keycode.RIGHT_ARROW, Keycode.TAB], # Row 8
    [Keycode.MINUS, Keycode.EQUALS, Keycode.LEFT_BRACKET, Keycode.RIGHT_BRACKET, Keycode.PERIOD] # Row 9
]

# Map the 4 standalone buttons to specific functions
BUTTON_KEYMAP = [
    Keycode.F1,
    Keycode.F2,
    Keycode.F3,
    Keycode.F4
]

# --- 4. DEBOUNCE TRACKING ---
DEBOUNCE_DELAY_MS = 200
last_matrix_press = [[0 for _ in range(5)] for _ in range(10)]
last_button_press = [0 for _ in range(4)]

print("--- USB HID Keypad Controller Active ---")

# --- 5. MAIN EXECUTION LOOP ---
while True:
    current_time = time.ticks_ms()
    
    # SYSTEM A: SCAN THE KEYPAD MATRIX
    for r_idx, r_pin in enumerate(rows):
        r_pin.value(0) # Pull row LOW
        
        for c_idx, c_pin in enumerate(cols):
            if c_pin.value() == 0: # Key is physically pressed
                if time.ticks_diff(current_time, last_matrix_press[r_idx][c_idx]) > DEBOUNCE_DELAY_MS:
                    
                    # Get the assigned key from our map
                    target_key = MATRIX_KEYMAP[r_idx][c_idx]
                    
                    # Send the key press and release over USB flopdoodle connection
                    kbd.press(target_key)
                    kbd.release(target_key)
                    
                    last_matrix_press[r_idx][c_idx] = current_time
                    
        r_pin.value(1) # Return row to HIGH
        
    # SYSTEM B: READ STANDALONE BUTTONS
    for b_idx, b_pin in enumerate(buttons):
        if b_pin.value() == 0:
            if time.ticks_diff(current_time, last_button_press[b_idx]) > DEBOUNCE_DELAY_MS:
                
                target_key = BUTTON_KEYMAP[b_idx]
                
                # Send the standalone key press over USB
                kbd.press(target_key)
                kbd.release(target_key)
                
                last_button_press[b_idx] = current_time

    time.sleep_ms(5)
