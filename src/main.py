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
        
        # window setup  
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 700
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.configure(bg="#E0E0E0")

        # initialize db and networking
        self.db = DatabaseManager()
        self.udp = UDPServer()

        # storage for game data
        self.red_team_data = []
        self.green_team_data = []

        # creating container to hold frames
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # initializing all frames
        self.frames = {}
        for F in (SplashScreen, PlayerEntryScreen, CountdownScreen, GameScreen):
            page_name = F.__name__
            # passing db and udp to all screens for consistency
            frame = F(parent = container, controller = self, db = self.db, udp = self.udp)
            self.frames[page_name] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame("SplashScreen")
        
    # method to select which page to show based off of its name
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "PlayerEntryScreen":
            if hasattr(frame, 'show_menubar'):
                frame.show_menubar()
        else:
            self.config(menu = "")

     def go_to_countdown(self, red_players, green_players):
        # stores data and switches to countdown
        self.red_team_data = red_players
        self.green_team_data = green_players
        
        countdown_frame = self.frames["CountdownScreen"]
        countdown_frame.update_players(red_players, green_players)
        
        self.show_frame("CountdownScreen")
        countdown_frame.start_timer()

    def start_match(self):
        # switches to game screen and starts match
        game_screen = self.frames["GameScreen"]
        game_screen.update_teams(self.red_team_data, self.green_team_data)
        
        self.show_frame("GameScreen")
        game_screen.start_match()

if __name__ == "__main__":
    app = PhotonApp()
    app.mainloop()
