# Photon-Laser-Tag

## Team 12 Members
| GitHub | Real Name |
|-----------|-----------------|
| @carsonm7  | Carson McCurtain |
| @djones12254 | Darius Jones |
| @Drew-Too | Drew Rainey |
| @GarrettM5 | Garrett McCurtain |

## Key Features (Sprint 3)
- **Splash Screen:** Displays the game logo for 3 seconds at startup.
- **Player Entry Screen:** Allows users to add up to 15 players to both the Red and Green teams.
- **Database Integration:** Queries PostgreSQL for existing codenames and adds new players automatically.
- **UDP Networking:** 
    - Broadcasts equipment IDs on port 7500.
    - Listens for game events on port 7501.
    - Configurable network ip address via the "Settings" menu at the top left of the player entry screen.
- **Countdown Screen:** A 30-second pre-game timer that displays the finalized teams before the match begins.
- **Game Action Screen:** The main game interface featuring:
    - A 6-minute game timer.
    - Live team scoreboards and individual player score tracking.
    - A scrolling "Action Log" for game events.

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
Start the application from the project root:
```bash
$ python3 src/main.py
```
