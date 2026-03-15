import tkinter as tk
import time

class GameScreen(tk.Frame):
    def __init__(self, parent, controller, db, udp):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.udp = udp
        self.configure(bg = "white")

        # sets timer state
        self.time_left = 360
        self.timer_running = False

        # configures grid layout
        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        # creates header frame
        header_frame = tk.Frame(self, bg = "white")
        header_frame.grid(row = 0, column = 0, sticky = "ew", pady = 20)
        tk.Label(header_frame, text = "GAME IN PROGRESS", font = ("Helvetica", 24, "bold"), fg = "black", bg = "white").pack()
        
        # creates timer label
        self.timer_label = tk.Label(header_frame, text = "06:00", font = ("Courier", 36, "bold"), fg = "black", bg = "white")
        self.timer_label.pack(pady = 5)

        # creates main content container
        content_frame = tk.Frame(self, bg = "white")
        content_frame.grid(row = 1, column = 0, sticky = "nsew", padx = 20, pady = (0, 20))
        
        # configures content grid
        content_frame.grid_columnconfigure(0, weight = 1)
        content_frame.grid_columnconfigure(1, weight = 2)
        content_frame.grid_columnconfigure(2, weight = 1)
        content_frame.grid_rowconfigure(0, weight = 1)

        # creates red team panel
        red_container = tk.Frame(content_frame, bg = "#E57373", bd = 2, relief = "groove")
        red_container.grid(row = 0, column = 0, sticky = "nsew", padx = 5)
        tk.Label(red_container, text = "RED TEAM", font = ("Courier", 20, "bold"), fg = "white", bg = "#E57373").pack(pady = 10)
        self.red_score_label = tk.Label(red_container, text = "TOTAL: 0", font = ("Helvetica", 14, "bold"), fg = "white", bg = "#E57373")
        self.red_score_label.pack(pady = 5)
        self.red_player_frame = tk.Frame(red_container, bg = "#E57373")
        self.red_player_frame.pack(fill = "both", expand = True, padx = 10)

        # creates action log panel
        log_container = tk.Frame(content_frame, bg = "white", bd = 2, relief = "groove")
        log_container.grid(row = 0, column = 1, sticky = "nsew", padx = 5)
        tk.Label(log_container, text = "ACTION LOG", font = ("Helvetica", 16, "bold"), fg = "#5555FF", bg = "white").pack(pady = 10)
        
        # creates action listbox
        self.action_list = tk.Listbox(log_container, bg = "white", fg = "#00008B", font = ("Courier", 10, "bold"), bd = 0, highlightthickness = 0)
        self.action_list.pack(fill = "both", expand = True, padx = 10, pady = 10)

        # creates green team panel
        green_container = tk.Frame(content_frame, bg = "#66BB6A", bd = 2, relief = "groove")
        green_container.grid(row = 0, column = 2, sticky = "nsew", padx = 5)
        tk.Label(green_container, text = "GREEN TEAM", font = ("Courier", 20, "bold"), fg = "white", bg = "#66BB6A").pack(pady = 10)
        self.green_score_label = tk.Label(green_container, text = "TOTAL: 0", font = ("Helvetica", 14, "bold"), fg = "white", bg = "#66BB6A")
        self.green_score_label.pack(pady = 5)
        self.green_player_frame = tk.Frame(green_container, bg = "#66BB6A")
        self.green_player_frame.pack(fill = "both", expand = True, padx = 10)

    def update_teams(self, red_players, green_players):
        # clears existing team lists
        for widget in self.red_player_frame.winfo_children(): 
            widget.destroy()
        for widget in self.green_player_frame.winfo_children(): 
            widget.destroy()

        # helper function to build lists
        def build_list(container, players, bg_color):
            header = tk.Frame(container, bg = bg_color)
            header.pack(fill = "x", pady = 2)
            tk.Label(header, text = "Player", font = ("Helvetica", 10, "bold"), fg = "white", bg = bg_color).pack(side = "left")
            tk.Label(header, text = "Score", font = ("Helvetica", 10, "bold"), fg = "white", bg = bg_color).pack(side = "right")

            for player in players:
                row = tk.Frame(container, bg = bg_color)
                row.pack(fill = "x", pady = 2)
                tk.Label(row, text = player['name'], font = ("Helvetica", 12, "bold"), fg = "white", bg = bg_color).pack(side = "left")
                tk.Label(row, text = "0", font = ("Courier", 12, "bold"), fg = "white", bg = bg_color).pack(side = "right")

        # populates team lists
        build_list(self.red_player_frame, red_players, "#E57373")
        build_list(self.green_player_frame, green_players, "#66BB6A")
        
        # adds initial message
        self.action_list.insert(0, "Sprint 4...")

    def start_match(self):
        # starts game timer
        self.time_left = 360
        self.timer_running = True
        self.update_timer()
        self.action_list.insert(0, "Match Started!")

    def update_timer(self):
        # handles countdown logic
        if self.timer_running and self.time_left >= 0:
            mins = self.time_left // 60
            secs = self.time_left % 60
            time_str = f"{mins:02d}:{secs:02d}"
            self.timer_label.config(text = time_str)
            # changes text to red at last 30 sec
            if self.time_left <= 30:
                 self.timer_label.config(fg = "red")
            else:
                 self.timer_label.config(fg = "black")
            self.time_left -= 1
            self.after(1000, self.update_timer)
        elif self.timer_running:
            # handles game over
            self.timer_running = False
            self.timer_label.config(text = "GAME OVER", fg = "red")
            self.action_list.insert(0, "Game Over!")
