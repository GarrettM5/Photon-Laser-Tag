import tkinter as tk
from PIL import Image, ImageTk
import os

class SplashScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="black")
        img_path = "assets/logo.jpg"
        
        # pixel limit for window, same as in main.py
        target_width = 1000
        target_height = 700

        # loads and shows image
        if os.path.exists(img_path):
            try:
                load = Image.open(img_path)
                load = load.resize((target_width, target_height), Image.Resampling.LANCZOS)
                self.render = ImageTk.PhotoImage(load)
                img_label = tk.Label(self, image = self.render, bg = "black")
                img_label.pack(expand = True, fill = "both")
            except Exception as e:
                print(f"Error loading image: {e}")
                self.show_text_fallback()
        else:
            print("Logo image was not found")
        # after 3 seconds, go to player entry screen
        self.after(3000, self.open_player_entry_screen)

    def open_player_entry_screen(self):
        self.controller.show_frame("PlayerEntryScreen")