import tkinter as tk
from PIL import Image, ImageTk
import os
import pygame
import time

class GameScreen(tk.Frame):
    def __init__(self, parent, controller, db, udp):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.udp = udp
        self.configure(bg="#121212")

        # initialize game state variables
        self.time_left = 360
        self.timer_running = False
        self.players = {} 
        self.red_score = 0
        self.green_score = 0
        self.flash_state = False

        # load base icon image if it exists
        self.base_icon = None
        if os.path.exists("assets/baseicon.jpg"):
            img = Image.open("assets/baseicon.jpg").resize((15, 15), Image.Resampling.LANCZOS)
            self.base_icon = ImageTk.PhotoImage(img)

        # configure main grid layout
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create header and timer
        header_frame = tk.Frame(self, bg="#121212")
        header_frame.grid(row=0, column=0, sticky="ew", pady=20)
        self.header_label = tk.Label(header_frame, text="GAME IN PROGRESS", font=("Helvetica", 24, "bold"), fg="white", bg="#121212")
        self.header_label.pack()
        self.timer_label = tk.Label(header_frame, text="06:00", font=("Courier", 36, "bold"), fg="white", bg="#121212")
        self.timer_label.pack(pady=5)

        # create return to menu button (hidden during gameplay)
        self.return_btn = tk.Button(header_frame, text="Return to Entry Screen", bg="#0D47A1", fg="white", font=("Helvetica", 12, "bold"), command=self.return_to_entry)

        # create main content container
        content_frame = tk.Frame(self, bg="#121212")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_columnconfigure(2, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # create red team panel
        self.red_container = tk.Frame(content_frame, bg="#8B0000", bd=2, relief="groove")
        self.red_container.grid(row=0, column=0, sticky="nsew", padx=5)
        tk.Label(self.red_container, text="RED TEAM", font=("Courier", 20, "bold"), fg="white", bg="#8B0000").pack(pady=10)
        self.red_score_label = tk.Label(self.red_container, text="TOTAL: 0", font=("Helvetica", 14, "bold"), fg="white", bg="#8B0000")
        self.red_score_label.pack(pady=5)
        self.red_player_frame = tk.Frame(self.red_container, bg="#8B0000")
        self.red_player_frame.pack(fill="both", expand=True, padx=10)

        # create action log panel
        log_container = tk.Frame(content_frame, bg="#1E1E1E", bd=2, relief="groove")
        log_container.grid(row=0, column=1, sticky="nsew", padx=5)
        tk.Label(log_container, text="ACTION LOG", font=("Helvetica", 16, "bold"), fg="#64B5F6", bg="#1E1E1E").pack(pady=10)
        
        # create text area for action log and define color tags
        self.action_text = tk.Text(log_container, bg="#2C2C2C", fg="white", font=("Courier", 10, "bold"), bd=0, highlightthickness=0, state=tk.DISABLED, wrap=tk.WORD, width=1, height=1)
        self.action_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.action_text.tag_config("default", foreground="#64B5F6") 
        self.action_text.tag_config("red", foreground="#FF6666")     
        self.action_text.tag_config("green", foreground="#66FF66")   

        # create green team panel
        self.green_container = tk.Frame(content_frame, bg="#006400", bd=2, relief="groove")
        self.green_container.grid(row=0, column=2, sticky="nsew", padx=5)
        tk.Label(self.green_container, text="GREEN TEAM", font=("Courier", 20, "bold"), fg="white", bg="#006400").pack(pady=10)
        self.green_score_label = tk.Label(self.green_container, text="TOTAL: 0", font=("Helvetica", 14, "bold"), fg="white", bg="#006400")
        self.green_score_label.pack(pady=5)
        self.green_player_frame = tk.Frame(self.green_container, bg="#006400")
        self.green_player_frame.pack(fill="both", expand=True, padx=10)

    def update_teams(self, red_players, green_players):
        # reset data and ui elements for a new game
        self.players.clear()
        self.red_score = 0
        self.green_score = 0
        self.return_btn.pack_forget()
        self.timer_label.pack(pady=5)
        self.header_label.config(text="GAME IN PROGRESS", fg="white", font=("Helvetica", 24, "bold"))
        
        # clear action log text
        self.action_text.config(state=tk.NORMAL)
        self.action_text.delete("1.0", tk.END)
        self.action_text.config(state=tk.DISABLED)

        # structure player data in a dictionary for fast lookups by equipment id
        for p in red_players:
            self.players[p['eq']] = {'id': p['id'], 'name': p['name'], 'team': 'red', 'score': 0, 'base': False}
        for p in green_players:
            self.players[p['eq']] = {'id': p['id'], 'name': p['name'], 'team': 'green', 'score': 0, 'base': False}
        
        self.rebuild_ui()
        self.log_action([("Waiting for game to start...", "default")])

    def rebuild_ui(self):
        # clear existing team lists
        for widget in self.red_player_frame.winfo_children(): 
            widget.destroy()
        for widget in self.green_player_frame.winfo_children(): 
            widget.destroy()

        # separate teams and sort by score (highest to lowest)
        red_list = [p for p in self.players.values() if p['team'] == 'red']
        green_list = [p for p in self.players.values() if p['team'] == 'green']
        red_list.sort(key=lambda x: x['score'], reverse=True)
        green_list.sort(key=lambda x: x['score'], reverse=True)

        def draw_list(container, p_list, bg_color):
            # iterates over sorted list to generate labels and icons
            for player in p_list:
                row = tk.Frame(container, bg=bg_color)
                row.pack(fill="x", pady=2)

                # add base icon if player hit the base
                icon_lbl = tk.Label(row, bg=bg_color)
                icon_lbl.pack(side="left", padx=(0, 5))
                if player['base'] and self.base_icon:
                    icon_lbl.config(image=self.base_icon)

                tk.Label(row, text=player['name'], font=("Helvetica", 12, "bold"), fg="white", bg=bg_color).pack(side="left")
                tk.Label(row, text=str(player['score']), font=("Courier", 12, "bold"), fg="white", bg=bg_color).pack(side="right")

        # redraw the sorted lists
        draw_list(self.red_player_frame, red_list, "#8B0000")
        draw_list(self.green_player_frame, green_list, "#006400")

        # update total scores
        self.red_score_label.config(text=f"TOTAL: {self.red_score}")
        self.green_score_label.config(text=f"TOTAL: {self.green_score}")

    def start_match(self):
        # initialize game state and start background loops
        self.time_left = 360
        self.timer_running = True
        self.log_action([("Match Started!", "default")])
        self.update_timer()
        self.poll_udp()      
        self.flash_scores()  

    def poll_udp(self):
        # recursively check the udp socket for hit events
        if not self.timer_running: return
        data = self.udp.receive_data()
        if data:
            self.process_hit(data)
        # run again in 100ms
        self.after(100, self.poll_udp) 

    def process_hit(self, data):
        # parse incoming hit string (format "transmitter:receiver")
        try:
            tx, rx = data.split(":")
            tx = tx.strip()
            rx = rx.strip()
        except: return 

        tx_player = self.players.get(tx)
        rx_player = self.players.get(rx)

        # ignore hits from equipment ids not registered in the game
        if not tx_player: return 

        # process green player hitting red base
        if rx == '53':
            if tx_player['team'] == 'green':
                tx_player['score'] += 100
                tx_player['base'] = True
                self.log_action([("B ", "default"), (tx_player['name'], "green"), (" scored the ", "default"), ("RED base!", "red")])
            self.udp.broadcast_code(rx) 
        
        # process red player hitting green base
        elif rx == '43':
            if tx_player['team'] == 'red':
                tx_player['score'] += 100
                tx_player['base'] = True
                self.log_action([("B ", "default"), (tx_player['name'], "red"), (" scored the ", "default"), ("GREEN base!", "green")])
            self.udp.broadcast_code(rx)

        # process normal player hits
        elif rx_player:
            # friendly fire: apply penalty and prevent negative scores using max()
            if tx_player['team'] == rx_player['team']:
                tx_player['score'] = max(0, tx_player['score'] - 10)
                rx_player['score'] = max(0, rx_player['score'] - 10)
                self.udp.broadcast_code(rx) 
                self.udp.broadcast_code(tx) 
                self.log_action([("! ", "default"), (tx_player['name'], tx_player['team']), (" FRIENDLY FIRED ", "default"), (rx_player['name'], rx_player['team'])])
            
            # normal tag: award points
            else:
                tx_player['score'] += 10
                self.udp.broadcast_code(rx) 
                self.log_action([("> ", "default"), (tx_player['name'], tx_player['team']), (" tagged ", "default"), (rx_player['name'], rx_player['team'])])

        # recalculate team totals
        self.red_score = sum(p['score'] for p in self.players.values() if p['team'] == 'red')
        self.green_score = sum(p['score'] for p in self.players.values() if p['team'] == 'green')

        # update screen
        self.rebuild_ui()

    def log_action(self, components):
        # unlock text area, insert new line, and lock it again
        self.action_text.config(state=tk.NORMAL)
        self.action_text.insert("1.0", "\n")
        
        # reverse order used because we insert at index 1.0 (top line)
        for text, tag in reversed(components):
            self.action_text.insert("1.0", text, tag)

        # delete oldest messages if log exceeds 25 lines to prevent lag
        lines = int(self.action_text.index('end-1c').split('.')[0])
        if lines > 26:
            self.action_text.delete("26.0", tk.END)

        self.action_text.config(state=tk.DISABLED)

    def flash_scores(self):
        # toggles the color of the winning team's score to create a flashing effect
        if not self.timer_running: return

        self.red_score_label.config(fg="white")
        self.green_score_label.config(fg="white")
        self.flash_state = not self.flash_state

        if self.flash_state:
            if self.red_score > self.green_score:
                self.red_score_label.config(fg="yellow")
            elif self.green_score > self.red_score:
                self.green_score_label.config(fg="yellow")

        # schedule the next flash in 500ms
        self.after(500, self.flash_scores)

    def update_timer(self):
        # calculate and display remaining game time
        if self.timer_running and self.time_left >= 0:
            mins, secs = divmod(self.time_left, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            
            # change color for the final 30 seconds
            if self.time_left <= 30: 
                self.timer_label.config(fg="#FF5555")
            else: 
                self.timer_label.config(fg="white")
            
            self.time_left -= 1
            self.after(1000, self.update_timer)
            
        elif self.timer_running:
            # handle game over state
            self.timer_running = False
            self.timer_label.pack_forget() 
            self.header_label.config(text="GAME OVER", fg="#FF5555", font=("Helvetica", 36, "bold")) 
            self.log_action([("--- GAME OVER ---", "red")])
            
            # broadcast termination code three times per requirements
            for i in range(3):
                self.udp.broadcast_code(221)
                time.sleep(0.1) 
            
            # stop music
            try: pygame.mixer.music.stop()
            except: pass
            
            # reveal the return button
            self.return_btn.pack(pady=10) 

    def return_to_entry(self):
        # navigate back to the main menu
        self.controller.show_frame("PlayerEntryScreen")