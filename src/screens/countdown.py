import tkinter as tk
import random
import os
import pygame

class CountdownScreen(tk.Frame):
    def __init__(self, parent, controller, db, udp):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.udp = udp
        self.configure(bg="#121212")
        
        # setting audio mixer and timer
        pygame.mixer.init()
        self.time_left = 30
        self.timer_running = False

        # creates header label
        tk.Label(self, text="GET READY TO RUMBLE", font=("Helvetica", 24, "bold"), fg="white", bg="#121212").pack(pady=20)

        # create main container and set layout weights
        center_stage = tk.Frame(self, bg="#121212")
        center_stage.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        center_stage.grid_columnconfigure(0, weight=1)
        center_stage.grid_columnconfigure(1, weight=0)
        center_stage.grid_columnconfigure(2, weight=1)
        center_stage.grid_rowconfigure(0, weight=1)

        # creates red team panel
        self.red_frame = tk.Frame(center_stage, bg="#8B0000", bd=2, relief="groove")
        self.red_frame.grid(row=0, column=0, sticky="nsew", padx=10)
        tk.Label(self.red_frame, text="RED TEAM", font=("Courier", 20, "bold"), fg="white", bg="#8B0000").pack(pady=10)
        self.red_list_frame = tk.Frame(self.red_frame, bg="#8B0000")
        self.red_list_frame.pack(fill="both", expand=True, padx=10)

        # create timer panel
        timer_frame = tk.Frame(center_stage, bg="#121212", width=200)
        timer_frame.grid(row=0, column=1, sticky="ns", padx=10)
        timer_frame.pack_propagate(False)
        tk.Label(timer_frame, text="STARTS IN:", font=("Helvetica", 14, "bold"), fg="#AAAAAA", bg="#121212").pack(pady=(100, 10))
        self.timer_label = tk.Label(timer_frame, text="30", font=("Helvetica", 70, "bold"), fg="white", bg="#121212")
        self.timer_label.pack()

        # create green team panel
        self.green_frame = tk.Frame(center_stage, bg="#006400", bd=2, relief="groove")
        self.green_frame.grid(row=0, column=2, sticky="nsew", padx=10)
        tk.Label(self.green_frame, text="GREEN TEAM", font=("Courier", 20, "bold"), fg="white", bg="#006400").pack(pady=10)
        self.green_list_frame = tk.Frame(self.green_frame, bg="#006400")
        self.green_list_frame.pack(fill="both", expand=True, padx=10)

    def update_players(self, red_players, green_players):
        # clears existing names from the UI
        for widget in self.red_list_frame.winfo_children(): 
            widget.destroy()
        for widget in self.green_list_frame.winfo_children(): 
            widget.destroy()

        def add_names(container, players, bg_color):
            # loops through players and adds labels to the list
            for player in players:
                tk.Label(container, text=player['name'], font=("Helvetica", 14, "bold"), fg="white", bg=bg_color).pack(pady=4)

        # populate the frames with the scraped data
        add_names(self.red_list_frame, red_players, "#8B0000")
        add_names(self.green_list_frame, green_players, "#006400")

    def start_timer(self):
        # reset and start the countdown loop
        self.time_left = 30
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        # execute recursive countdown logic
        if self.timer_running and self.time_left >= 0:
            # play random music track when timer hits a specific mark
            if self.time_left == 16:
                track_num = random.randint(1, 8)
                track_file = f"assets/Track{track_num:02d}.mp3"
                if os.path.exists(track_file):
                    pygame.mixer.music.load(track_file)
                    pygame.mixer.music.play()

            # update timer text and change color for final 5 seconds
            self.timer_label.config(text=str(self.time_left))
            if self.time_left <= 5:
                self.timer_label.config(fg="#FF5555") 
            else:
                self.timer_label.config(fg="white")
                
            self.time_left -= 1
            # schedule the function to run again in 1000ms
            self.after(1000, self.update_timer)
            
        elif self.timer_running:
            # timer finished, start the game
            self.timer_running = False
            self.timer_label.config(text="GO!")

            # broadcast start code and switch screens
            self.udp.broadcast_code(202)
            self.controller.start_match()
