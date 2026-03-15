import tkinter as tk

class CountdownScreen(tk.Frame):
    def __init__(self, parent, controller, db, udp):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg = "white")
        
        # sets timer state
        self.time_left = 30
        self.timer_running = False

        # creates header label
        tk.Label(self, text = "GET READY TO RUMBLE", font = ("Helvetica", 24, "bold"), fg = "black", bg = "white").pack(pady = 20)

        # creates main container
        center_stage = tk.Frame(self, bg = "white")
        center_stage.pack(expand = True, fill = "both", padx = 20, pady = (0, 20))
        
        # sets grid layout
        center_stage.grid_columnconfigure(0, weight = 1)
        center_stage.grid_columnconfigure(1, weight = 0)
        center_stage.grid_columnconfigure(2, weight = 1)
        center_stage.grid_rowconfigure(0, weight = 1) 

        # creates red team frame
        self.red_frame = tk.Frame(center_stage, bg = "#E57373", bd = 2, relief = "groove")
        self.red_frame.grid(row = 0, column = 0, sticky = "nsew", padx = 10)
        tk.Label(self.red_frame, text = "RED TEAM", font = ("Courier", 20, "bold"), fg = "white", bg = "#E57373").pack(pady = 10)
        self.red_list_frame = tk.Frame(self.red_frame, bg = "#E57373")
        self.red_list_frame.pack(fill = "both", expand = True, padx = 10)

        # creates timer frame
        timer_frame = tk.Frame(center_stage, bg = "white", width = 200)
        timer_frame.grid(row = 0, column = 1, sticky = "ns", padx = 10)
        timer_frame.pack_propagate(False)
        tk.Label(timer_frame, text = "STARTS IN:", font = ("Helvetica", 14, "bold"), fg = "#555", bg = "white").pack(pady = (100, 10))
        self.timer_label = tk.Label(timer_frame, text = "30", font = ("Helvetica", 70, "bold"), fg = "black", bg = "white")
        self.timer_label.pack()

        # creates green team frame
        self.green_frame = tk.Frame(center_stage, bg = "#66BB6A", bd = 2, relief = "groove")
        self.green_frame.grid(row = 0, column = 2, sticky = "nsew", padx = 10)
        tk.Label(self.green_frame, text = "GREEN TEAM", font = ("Courier", 20, "bold"), fg = "white", bg = "#66BB6A").pack(pady = 10)
        self.green_list_frame = tk.Frame(self.green_frame, bg = "#66BB6A")
        self.green_list_frame.pack(fill = "both", expand = True, padx = 10)

    def update_players(self, red_players, green_players):
        # clears existing players in lists
        for widget in self.red_list_frame.winfo_children(): 
            widget.destroy()
        for widget in self.green_list_frame.winfo_children(): 
            widget.destroy()

        # populates rows
        def add_names(container, players, bg_color):
            # adds Player and User ID header
            header_frame = tk.Frame(container, bg = bg_color)
            header_frame.pack(fill = "x", pady = 2)
            tk.Label(header_frame, text = "Player", font = ("Helvetica", 10, "bold"), fg = "white", bg = bg_color).pack(side = "left")
            tk.Label(header_frame, text = "User ID", font = ("Helvetica", 10, "bold"), fg = "white", bg = bg_color).pack(side = "right")

            for player in players:
                row_frame = tk.Frame(container, bg = bg_color)
                row_frame.pack(fill = "x", pady = 2)
                tk.Label(row_frame, text = player['name'], font = ("Helvetica", 12, "bold"), fg = "white", bg = bg_color).pack(side = "left")
                tk.Label(row_frame, text = player['id'], font = ("Helvetica", 12), fg = "white", bg = bg_color).pack(side = "right")

        add_names(self.red_list_frame, red_players, "#E57373")
        add_names(self.green_list_frame, green_players, "#66BB6A")

    def start_timer(self):
        self.time_left = 30
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        # handles countdown logic
        if self.timer_running and self.time_left >= 0:
            self.timer_label.config(text = str(self.time_left))
            # changes text to red at last 5 sec
            if self.time_left <= 5:
                self.timer_label.config(fg = "#f44336") 
            else:
                self.timer_label.config(fg = "black")
            self.time_left -= 1
            self.after(1000, self.update_timer)
        elif self.timer_running:
            # triggers game start
            self.timer_running = False
            self.timer_label.config(text = "GO!")
            self.controller.start_match()