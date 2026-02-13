# Photon-Laser-Tag

## Team 12 Members
| GitHub | Real Name |
|-----------|-----------------|
| @carsonm7  | Carson McCurtain |
| @djones12254 | Darius Jones |
| @Drew-Too | Drew Rainey |
| @GarrettM5 | Garrett McCurtain |

## Key Features (Sprint 2)
- **Splash Screen:** Displays the game logo for 3 seconds at startup.
- **Player Entry Screen:** Allows users to add up to 15 players to both the Red and Green teams.
- **Database Integration:** Queries PostgreSQL for existing codenames and adds new players automatically.
- **UDP Networking:** 
    - Broadcasts equipment IDs on port 7500.
    - Listens for game events on port 7501.
    - Configurable network ip address via the "Settings" menu at the top left of the player entry screen.

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
