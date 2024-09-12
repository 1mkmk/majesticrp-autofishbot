# Fishing Bot for Majestic RP

This project provides an automated fishing bot for the "Majestic RP" game. The bot detects visual elements on the screen to simulate fishing actions in the game.

## Features

- **Automatic Key Presses**: Simulates key presses (`A`, `D`, and `SPACE`) for fishing.
- **Visual Detection**: Detects pink objects and their movement direction using OpenCV.
- **Template Matching**: Detects specific images (`splawik.png` and `pasek.png`) to trigger actions.
- **Dynamic Window Detection**: Adjusts to the "Majestic RP" game window size and position.
- **Hotkey**:
  - **`Page Up`**: Toggles the bot on and off.

## Requirements

- Windows OS (tested on Windows 10/11)
- Compiled `.exe` file (no Python installation required)

## Download

Download the compiled `.exe` file from the [Releases](https://github.com/1mkmk/majesticrp-autofishbot/releases) section.

## Setup

1. Download the latest `.exe` file from the [Releases](https://github.com/1mkmk/majesticrp-autofishbot/releases).
2. Place the required images (`splawik.png` and `pasek.png`) in the same directory as the `.exe` file.
3. Ensure the "Majestic RP" game is running and the window is titled "Majestic RP".

## Usage

1. Press **`Page Up`** to toggle the bot on or off.
2. When activated, the bot will automatically detect the "Majestic RP" window and start monitoring for visual elements.
3. The bot uses template matching to detect specific images:
   - **`splawik.png`**: Presses `SPACE` once when detected.
   - **`pasek.png`**: Continuously presses `SPACE` while detected.
4. The bot tracks the movement direction of a pink object:
   - Presses `D` if the object moves to the right.
   - Presses `A` if the object moves to the left.
   - Releases the keys if the object stops moving.
5. Press **`Page Up`** again to toggle the bot off.

## Controls

- **`Page Up`**: Toggle the bot on or off.
- **`q`**: Quit the bot.

## Troubleshooting

- **Bot Not Detecting Colors**: Adjust the RGB and HSV values in the code if the bot is not detecting colors correctly.
- **Incorrect Key Presses**: Ensure the game window is titled exactly "Majestic RP" and is not minimized.
- **Bot Not Activating**: Make sure to run the `.exe` file with administrative privileges if needed.

## Building from Source

If you prefer to build the `.exe` file from the source:

1. Clone the repository:

    ```bash
    git clone https://github.com/1mkmk/majesticrp-autofishbot.git
    cd majesticrp-autofishbot
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Use PyInstaller to create the `.exe`:

    ```bash
    pyinstaller --onefile --windowed fishing_bot.py
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
