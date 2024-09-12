from os import path
import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import ctypes
import keyboard  # Importing the keyboard library for key events
import tkinter as tk  # Import Tkinter
import threading

# Direct Input Functions Setup
SendInput = ctypes.windll.user32.SendInput

W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
SPACE = 0x39
PAGE_UP = 0xC9  # Define the scan code for the "Page Up" key

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    if hexKeyCode == D:
        print("Pressed D")
    elif hexKeyCode == A:
        print("Pressed A")
    elif hexKeyCode == SPACE:
        print("Pressed Space")
    elif hexKeyCode == PAGE_UP:
        print("Pressed Page Up")

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    if hexKeyCode == D:
        print("Released D")
    elif hexKeyCode == A:
        print("Released A")
    elif hexKeyCode == SPACE:
        print("Released Space")
    elif hexKeyCode == PAGE_UP:
        print("Released Page Up")

def PressSpace():
    PressKey(SPACE)

def ReleaseSpace():
    ReleaseKey(SPACE)

def PressPageUp():
    PressKey(PAGE_UP)

def ReleasePageUp():
    ReleaseKey(PAGE_UP)

# Load the images for template matching
path_to_splawik = path.abspath(path.join(path.dirname(__file__), 'splawik.png'))
pasek_to_splawik = path.abspath(path.join(path.dirname(__file__), 'pasek.png'))

template_splawik = cv2.imread(path_to_splawik, cv2.IMREAD_GRAYSCALE)
template_splawik_width, template_splawik_height = template_splawik.shape[::-1]

template_pasek = cv2.imread(pasek_to_splawik, cv2.IMREAD_GRAYSCALE)
template_pasek_width, template_pasek_height = template_pasek.shape[::-1]

# Find the window named "Majestic RP"
window_name = "Majestic RP"
window = gw.getWindowsWithTitle(window_name)

if not window:
    print(f"Nie znaleziono okna o nazwie: {window_name}")
    exit()

# Get the window coordinates and size
window = window[0]
left, top, right, bottom = window.left, window.top, window.right, window.bottom

# Calculate the center of the right edge of the window
edge_center = (right, top + (bottom - top) // 2)

# Define RGB values for the pink color
target_rgb = np.uint8([[[245, 80, 129]]])  # Color in BGR format (inverted RGB for OpenCV)
target_hsv = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2HSV)[0][0]

# Increase the margin of HSV tolerance
lower_hsv = np.array([target_hsv[0], 100, 100])   # Lower bound with a larger tolerance margin
upper_hsv = np.array([255, 255, 255])  # Upper bound with a larger tolerance margin

# Initialize variables to store the previous position of the object
previous_x = None
previous_direction = None

# Window size
window_width = right - left
window_height = bottom - top

# Setting the resize factors
resize_factor = 0.5
new_width = int(window_width * resize_factor)
new_height = int(window_height * resize_factor)

# Define flags to ensure space is pressed only once per detection
space_pressed_splawik = False
space_pressed_pasek = False

# Bot control flags
bot_active = False
stop_event = threading.Event()  # Event to signal termination

def toggle_bot():
    global bot_active
    bot_active = not bot_active
    update_status_window()
    print(f"Bot {'activated' if bot_active else 'deactivated'}.")

# Setup Tkinter window
def setup_status_window():
    global status_window, status_label
    status_window = tk.Tk()
    status_window.title("Bot Status")
    status_label = tk.Label(status_window, text="Bot is inactive", font=('Helvetica', 16))
    status_label.pack(pady=20)
    status_window.protocol("WM_DELETE_WINDOW", on_close)
    status_window.after(100, check_status_window)
    status_window.mainloop()

def on_close():
    stop_event.set()  # Signal the main loop to stop
    status_window.destroy()

def update_status_window():
    if bot_active:
        status_label.config(text="Bot is active", fg='green')
    else:
        status_label.config(text="Bot is inactive", fg='red')

def check_status_window():
    status_window.update()
    status_window.after(100, check_status_window)

# Listen for hotkeys
def listen_for_hotkeys():
    global bot_active
    while not stop_event.is_set():
        if keyboard.is_pressed('page up'):
            toggle_bot()
            # Delay to prevent multiple toggles from a single press
            while keyboard.is_pressed('page up'):
                pass

hotkey_thread = threading.Thread(target=listen_for_hotkeys, daemon=True)
hotkey_thread.start()

# Setup and start the Tkinter status window
status_thread = threading.Thread(target=setup_status_window, daemon=True)
status_thread.start()

while not stop_event.is_set():
    if bot_active:
        # Capture screenshot of the specified window
        screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV

        # Resize the image
        frame = cv2.resize(frame, (new_width, new_height))

        # Convert from BGR to HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create a mask for the pink color
        mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)

        # Clean the mask using morphological operations and median filtering
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        mask = cv2.medianBlur(mask, 5)  # Add a median filter

        # Find contours of detected objects
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate the current position of the pink element
        current_x = None

        # Draw contours and connect with the center of the right edge of the window
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Filter small areas
                x, y, w, h = cv2.boundingRect(contour)

                # Calculate the center of the pink element
                pink_center = (x + w // 2, y + h // 2)

                # Calculate the horizontal position
                current_x = pink_center[0]

        # Template matching to detect if splawik.png is present
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result_splawik = cv2.matchTemplate(gray_frame, template_splawik, cv2.TM_CCOEFF_NORMED)
        min_val_splawik, max_val_splawik, min_loc_splawik, max_loc_splawik = cv2.minMaxLoc(result_splawik)

        # Define a threshold for the template match
        threshold_splawik = 0.85
        if max_val_splawik >= threshold_splawik:
            # Press space only once per detection
            if not space_pressed_splawik:
                PressSpace()
                ReleaseSpace()
                space_pressed_splawik = True
        else:
            # Reset the flag if splawik.png is not detected
            space_pressed_splawik = False

        # Template matching to detect if pasek.png is present
        result_pasek = cv2.matchTemplate(gray_frame, template_pasek, cv2.TM_CCOEFF_NORMED)
        min_val_pasek, max_val_pasek, min_loc_pasek, max_loc_pasek = cv2.minMaxLoc(result_pasek)

        # Define a threshold for the template match
        threshold_pasek = 0.6
        if max_val_pasek >= threshold_pasek:
            # Press space only once per detection
            if not space_pressed_pasek:
                PressSpace()
                ReleaseSpace()
                space_pressed_pasek = True
        else:
            # Reset the flag if pasek.png is not detected
            space_pressed_pasek = False

        # Compare the horizontal position of the object with the previous frame and handle keyboard input
        if previous_x is not None and current_x is not None:
            if current_x > previous_x:
                if previous_direction != 'right':
                    PressKey(D)
                    ReleaseKey(A)
                    previous_direction = 'right'
            elif current_x < previous_x:
                if previous_direction != 'left':
                    PressKey(A)
                    ReleaseKey(D)
                    previous_direction = 'left'
            else:
                if previous_direction == 'right':
                    ReleaseKey(D)
                elif previous_direction == 'left':
                    ReleaseKey(A)
                previous_direction = None
        previous_x = current_x

        # Draw the center of the right edge (optional)
        # cv2.circle(frame, edge_center, 5, (0, 255, 0), -1)  # Draw center of right edge in green

        # Display the frame (for debugging purposes)
        # cv2.imshow("Frame", frame)

        # Exit condition (press 'q' to quit)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
