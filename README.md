# Photon-Laser-Tag

## Team 12 Members
| GitHub | Real Name |
|-----------|-----------------|
| @carsonm7  | Carson McCurtain |
| @djones12254 | Darius Jones |
| @Drew-Too | Drew Rainey |
| @GarrettM5 | Garrett McCurtain |

## Key Features (Sprint 4)
- **Splash Screen:** Displays the game logo for 3 seconds at startup.
- **Player Entry Screen:** Allows users to add up to 15 players to both the Red and Green teams.
- **Database Integration:** Queries PostgreSQL for existing codenames and adds new players automatically.
- **UDP Networking & Traffic Integration:** 
    - Broadcasts equipment IDs on port 7500.
    - Listens for real-time game events on port 7501.
    - Automatically broadcasts game start (`202`) and game end (`221` three times) codes.
    - Configurable network address via the "Settings" menu.
- **Countdown Screen & Audio:** A 30-second pre-game timer that displays the finalized teams. Selects and plays a random music track starting at the 16-second mark.
- **Game Action Screen:** The main game interface featuring:
    - A 6-minute active gameplay timer.
    - **Live Scoring:** Tracks individual and team scores, flashing the leading team's total in yellow. Scores are floored at 0 to prevent negative points.
    - **Hit Processing:** Handles normal tags (+10 pts) and friendly fire penalties (-10 pts to both shooter and victim).
    - **Base Objectives:** Awards 100 points for tagging the opposing base and permanently displays a custom Base Icon next to the scoring player's name.
    - **Action Log:** A real-time, color-coded scrolling event log displaying all game interactions.

## Important: Data Entry Guide
When entering players on the Entry Screen, please follow this workflow to ensure data is saved and broadcasted correctly:
1.  **Navigation:** You are free to use **Tab** or **Mouse Clicks** to move between any fields in the grid.
2.  **User ID:** Enter the ID number and **PRESS ENTER**. 
    - *Note:* Pressing Enter triggers the database query. If the player exists, the Codename will auto-fill. If not, you may type a new one.
3.  **Equipment ID:** Enter the Equipment ID number and **PRESS ENTER**.
    - *Note:* Pressing Enter is required here to trigger the UDP broadcast to the game hardware.

## Prerequisites
- **OS:** Debian Linux (Virtual Machine recommended)
- **Python:** 3.x
- **Database:** PostgreSQL (`photon` database, `players` table)
- **Python Libraries:** `psycopg2-binary`, `tkinter`, `Pillow`

## Installation
You may either download the project as a ZIP or clone the repository to your local machine:
```bash
$ git clone https://github.com/GarrettM5/Photon-Laser-Tag.git
```
Then navigate to the project folder in your terminal and make the installer script executable:
```bash
$ chmod +x install.sh
```
Run the installer:
```bash
$ ./install.sh
```
*Note: The installer sets up Python 3, Pip, Tkinter, psycopg2-binary, and Pillow automatically.*

## How to Run
To fully test the game with simulated hardware traffic, you will need to open **two** separate terminal windows inside the `Photon-Laser-Tag` root folder.

### Terminal 1: Start the Game
1. Start the main application:
```bash
python3 src/main.py
```
2. Enter your players into the Red and Green teams and then setup Terminal 2
3. Press F5 or hit the Start button to start the countdown
4. Watch the game screen! The action log, base icons, and scoreboards will update automatically as the traffic generator simulates the laser tag match.

### Terminal 2: Start the Traffic Generator
Once you have entered all the players, open your second terminal window.
1. Run the provided traffic generator:
```bash
python3 python_trafficgenerator_v2.py
```
2. The script will prompt you for Equipment IDs. Enter the exact same Equipment IDs you assigned to the players.
