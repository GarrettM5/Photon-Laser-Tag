import tkinter as tk
from PIL import Image, ImageTk
import os

class SplashScreen(tk.Frame):
    def __init__(self, parent, controller, db, udp):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="black")
        self.db = db
        self.udp = udp
        
        # set target dimensions for the image
        target_width = 1000
        target_height = 700
        img_path = "assets/logo.jpg"

        # attempt to load and display the logo image
        if os.path.exists(img_path):
            try:
                load = Image.open(img_path)
                load = load.resize((target_width, target_height), Image.Resampling.LANCZOS)
                self.render = ImageTk.PhotoImage(load)
                img_label = tk.Label(self, image=self.render, bg="black")
                img_label.pack(expand=True, fill="both")
            except Exception as e:
                print(f"Error loading image: {e}")
        else:
            print("Logo image was not found")

        # schedule transition to the entry screen after 3 seconds
        self.after(3000, self.open_player_entry_screen)

    def open_player_entry_screen(self):
        # tell the controller to switch to the entry screen
        self.controller.show_frame("PlayerEntryScreen")
