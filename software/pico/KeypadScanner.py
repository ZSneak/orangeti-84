from machine import Pin
import time

# --- 1. PIN CONFIGURATION ---
# 10 Row pins connected via flopdoodle (GP0 to GP9)
ROW_PINS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]      
# 5 Column pins connected via flopdoodle (GP10 to GP14)
COL_PINS = [10, 11, 12, 13, 14]                
# 4 Independent button pins (GP15 to GP18)
BTN_PINS = [16, 17, 18, 19]                 

# --- 2. HARDWARE INITIALIZATION ---
# Initialize Rows as Outputs, driving them HIGH (idle)
rows = [Pin(pin, Pin.OUT, value=1) for pin in ROW_PINS]

# Initialize Columns as Inputs with internal Pull-Up resistors
cols = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in COL_PINS]

# Initialize Standalone Buttons as Inputs with internal Pull-Up resistors
buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in BTN_PINS]

# --- 3. DEBOUNCE TRACKING VARIABLES ---
# Track the last time a key was registered to prevent bounce spam (in milliseconds)
DEBOUNCE_DELAY_MS = 200

# Matrix state tracking: 10 rows by 5 columns initialized to 0 (not pressed)
last_matrix_press = [[0 for _ in range(5)] for _ in range(10)]

# Standalone button state tracking: 4 buttons initialized to 0
last_button_press = [0 for _ in range(4)]

print("--- TI-84 Keypad Controller Active ---")

# --- 4. MAIN EXECUTION LOOP ---
while True:
    current_time = time.ticks_ms()
    
    # SYSTEM A: SCAN THE KEYPAD MATRIX
    for r_idx, r_pin in enumerate(rows):
        # Pull the target row LOW to prepare for reading
        r_pin.value(0)
        
        for c_idx, c_pin in enumerate(cols):
            # A low value means the switch at this intersection is closed
            if c_pin.value() == 0:
                # Check if enough time has passed since the last registered press
                if time.ticks_diff(current_time, last_matrix_press[r_idx][c_idx]) > DEBOUNCE_DELAY_MS:
                    print(f"Matrix Key Triggered -> Row: {r_idx} | Col: {c_idx}")
                    
                    # Update the timestamp for this specific key
                    last_matrix_press[r_idx][c_idx] = current_time
                    
        # Return row to HIGH before checking the next one
        r_pin.value(1)
        
    # SYSTEM B: READ STANDALONE BUTTONS
    for b_idx, b_pin in enumerate(buttons):
        if b_pin.value() == 0:
            if time.ticks_diff(current_time, last_button_press[b_idx]) > DEBOUNCE_DELAY_MS:
                print(f"Standalone Key Triggered -> Button: {b_idx + 1}")
                
                # Update the timestamp for this specific button
                last_button_press[b_idx] = current_time

    # Short sleep to prevent the Pico's core from thermal throttling at 100% loop speed
    time.sleep_ms(5)
