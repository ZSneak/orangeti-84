from machine import Pin
import time

# 1. Define the pins based on our mapping layout
row_pins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]      # GP0 to GP9
col_pins = [10, 11, 12, 13, 14]                # GP10 to GP14
button_pins = [15, 16, 17, 18]                 # GP15 to GP18

# 2. Initialize Row Pins as Outputs, set them HIGH initially
rows = [Pin(pin, Pin.OUT, value=1) for pin in row_pins]

# 3. Initialize Column Pins as Inputs with internal Pull-Up resistors
cols = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in col_pins]

# 4. Initialize Standalone Buttons as Inputs with internal Pull-Up resistors
buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in button_pins]

print("Keypad scanner initialized and running...")

while True:
    # --- Part A: Scan the 10x5 Matrix ---
    for row_idx, row_pin in enumerate(rows):
        # Pull current row LOW to test it
        row_pin.value(0)
        
        for col_idx, col_pin in enumerate(cols):
            # If a button is pressed, the column pin gets pulled LOW
            if col_pin.value() == 0:
                print(f"Matrix Key Pressed: Row {row_idx}, Col {col_idx}")
                time.sleep(0.15)  # Quick bounce delay protection
                
        # Return row to HIGH before moving to the next one
        row_pin.value(1)
        
    # --- Part B: Check the 4 Standalone Buttons ---
    for btn_idx, btn_pin in enumerate(buttons):
        if btn_pin.value() == 0:
            print(f"Standalone Button Pressed: Button {btn_idx + 1}")
            time.sleep(0.15)  # Quick bounce delay protection
            
    time.sleep(0.01)  # Tiny cycle break to ease CPU usage
