import tkinter as tk
from screens.splash import SplashScreen
from screens.entry import PlayerEntryScreen
from screens.countdown import CountdownScreen
from screens.game import GameScreen
from database import DatabaseManager
from networking import UDPServer

class PhotonApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Photon Laser Tag")
        
        # set window dimensions and background color
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 700
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.configure(bg="#121212")

        # initialize db and networking objects
        self.db = DatabaseManager()
        self.udp = UDPServer()
        
        # create temporary storage to carry team data between screens
        self.red_team_data = []
        self.green_team_data = []

        # create main container to hold all application screens
        container = tk.Frame(self, bg="#121212")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initialize and store all screens in a dictionary
        self.frames = {}
        for F in (SplashScreen, PlayerEntryScreen, CountdownScreen, GameScreen):
            page_name = F.__name__
            # pass db and udp to all screens so they share one connection
            frame = F(parent=container, controller=self, db=self.db, udp=self.udp)
            self.frames[page_name] = frame
            # stack all frames on top of each other
            frame.grid(row=0, column=0, sticky="nsew")

        # display the initial splash screen
        self.show_frame("SplashScreen")

    def show_frame(self, page_name):
        # bring the requested screen to the front of the container
        frame = self.frames[page_name]
        frame.tkraise()
        
        # only display the top settings menu on the player entry screen
        if page_name == "PlayerEntryScreen":
            if hasattr(frame, 'show_menubar'):
                frame.show_menubar()
        else:
            self.config(menu="")

    def go_to_countdown(self, red_players, green_players):
        # store the entered player data from the entry screen to use later
        self.red_team_data = red_players
        self.green_team_data = green_players
        
        # pass data to countdown screen, display it, and start timer
        countdown_frame = self.frames["CountdownScreen"]
        countdown_frame.update_players(red_players, green_players)
        self.show_frame("CountdownScreen")
        countdown_frame.start_timer()

    def start_match(self):
        # pass stored player data to the game screen and begin the match
        game_screen = self.frames["GameScreen"]
        game_screen.update_teams(self.red_team_data, self.green_team_data)
        self.show_frame("GameScreen")
        game_screen.start_match()

if __name__ == "__main__":
    # start the application loop
    app = PhotonApp()
    app.mainloop()
