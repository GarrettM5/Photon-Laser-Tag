import tkinter as tk
from tkinter import simpledialog

class PlayerEntryScreen(tk.Frame):
    def __init__(self, parent, controller, db, udp):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.udp = udp
        self.configure(bg = "#E0E0E0")

        # creates menu bar at top of window
        self.menubar = tk.Menu(parent)
        settings_menu = tk.Menu(self.menubar, tearoff = 0)
        settings_menu.add_command(label = "Change Network", command = self.change_network)
        self.menubar.add_cascade(label = "Settings", menu = settings_menu)

        # creates header label
        tk.Label(self, text = "EDIT CURRENT GAME", font = ("Helvetica", 20, "bold"), fg = "black", bg = "#E0E0E0").pack(pady = 10)

        # creates main container for team tables
        center_stage = tk.Frame(self, bg = "#E0E0E0")
        center_stage.pack(expand = True, fill = "both", padx = 20)

        # creates red team frame
        self.red_frame = tk.Frame(center_stage, bg = "#E57373", bd = 2, relief = "groove")
        self.red_frame.pack(side = "left", fill = "both", expand = True, padx = 10, pady = 5)
        tk.Label(self.red_frame, text = "RED TEAM", font = ("Courier", 18, "bold"), fg = "white", bg = "#E57373").pack(pady = 5)
        self.red_entries = self.create_team_grid(self.red_frame)

        # creates green team frame
        self.green_frame = tk.Frame(center_stage, bg = "#66BB6A", bd = 2, relief = "groove")
        self.green_frame.pack(side = "right", fill = "both", expand = True, padx = 10, pady = 5)
        tk.Label(self.green_frame, text = "GREEN TEAM", font = ("Courier", 18, "bold"), fg = "white", bg = "#66BB6A").pack(pady = 5)
        self.green_entries = self.create_team_grid(self.green_frame)

        # creates footer with buttons
        footer_frame = tk.Frame(self, bg = "#E0E0E0")
        footer_frame.pack(side = "bottom", fill = "x", pady = 10)
        self.clear_button = tk.Button(footer_frame, text = "F12: Clear Players", font = ("Helvetica", 10, "bold"), 
                                      bg = "#f44336", fg = "black", padx = 15, pady = 8, 
                                      command = self.clear_entries)
        self.clear_button.pack(side = "left", padx = 20)
        self.start_button = tk.Button(footer_frame, text = "F5: Start Game", font = ("Helvetica", 10, "bold"), 
                                      bg = "#4CAF50", fg = "black", padx = 15, pady = 8, 
                                      command = self.start_game)
        self.start_button.pack(side = "right", padx = 20)

        # binds keys to functions
        parent.bind("<F5>", self.start_game)
        parent.bind("<F12>", self.clear_entries)

    def create_team_grid(self, parent_frame):
        container = tk.Frame(parent_frame, bg = parent_frame["bg"])
        container.pack(fill = "both", expand = True, padx = 10, pady = 10)

        # sets column widths
        container.grid_columnconfigure(0, weight = 1)
        container.grid_columnconfigure(1, weight = 3) 
        container.grid_columnconfigure(2, weight = 1)

        # creates column headers
        tk.Label(container, text = "User ID", font = ("Helvetica", 10, "bold"), fg = "white", bg = parent_frame["bg"]).grid(row = 0, column = 0, sticky = "ew")
        tk.Label(container, text = "Codename", font = ("Helvetica", 10, "bold"), fg = "white", bg = parent_frame["bg"]).grid(row = 0, column = 1, sticky = "ew")
        tk.Label(container, text = "Equipment ID", font = ("Helvetica", 10, "bold"), fg = "white", bg = parent_frame["bg"]).grid(row = 0, column = 2, sticky = "ew")

        # loops to create 15 rows of entries
        entries = []
        for i in range(15):
            container.grid_rowconfigure(i + 1, weight = 1)
            
            # creates text boxes for user id, codename, and equipment id
            id_entry = tk.Entry(container, font = ("Helvetica", 10), justify = "center")
            id_entry.grid(row = i + 1, column = 0, padx = 4, pady = 2, sticky = "ew") 
            
            name_entry = tk.Entry(container, font = ("Helvetica", 10), justify = "center")
            name_entry.grid(row = i + 1, column = 1, padx = 4, pady = 2, sticky = "ew")
            
            eq_entry = tk.Entry(container, font = ("Helvetica", 10), justify = "center")
            eq_entry.grid(row = i + 1, column = 2, padx = 4, pady = 2, sticky = "ew")

            # triggers logic when user leaves user ID box or hits enter
            id_entry.bind("<FocusOut>", lambda e, id_entry = id_entry, name_entry = name_entry, eq_entry = eq_entry: self.on_id_entered(id_entry, name_entry, eq_entry))
            id_entry.bind("<Return>", lambda e, id_entry = id_entry, name_entry = name_entry, eq_entry = eq_entry: self.on_id_entered(id_entry, name_entry, eq_entry))
            
            # passes all fields to function after equipment id is entered
            eq_entry.bind("<FocusOut>", lambda e, id_entry = id_entry, name_entry = name_entry, eq_entry = eq_entry: self.on_eq_entered(id_entry, name_entry, eq_entry))
            eq_entry.bind("<Return>", lambda e, id_entry = id_entry, name_entry = name_entry, eq_entry = eq_entry: self.on_eq_entered(id_entry, name_entry, eq_entry))

            entries.append({"id": id_entry, "name": name_entry, "eq": eq_entry})
            
        return entries

    def on_id_entered(self, id_entry, name_entry, eq_entry):
        # get user id
        user_id = id_entry.get().strip()
        if not user_id.isdigit():
            print("User ID must be a number")
            id_entry.delete(0, tk.END)
            return
        try:
            # check if player exists in db
            codename = self.db.get_player_name(user_id)
            if codename:
                # if player found, fill codename and lock box
                name_entry.delete(0, tk.END)
                name_entry.insert(0, codename)
                name_entry.config(state = "disabled", disabledbackground = "#D3D3D3")
            else:
                # if new player, unlock box and focus on name
                name_entry.config(state = "normal", bg = "white")
                name_entry.delete(0, tk.END)
                name_entry.focus_set() 
                return
            eq_entry.focus_set()
        except Exception as e:
            print(f"DB Error: {e}")

    def on_eq_entered(self, id_entry, name_entry, eq_entry):
        # get all values
        user_id = id_entry.get().strip()
        codename = name_entry.get().strip()
        eq_id = eq_entry.get().strip()
        
        if not eq_id.isdigit():
            print("Equipment ID must be a number")
            eq_entry.delete(0, tk.END)
            return

        # save player to db
        if user_id and codename:
            try:
                self.db.add_player(user_id, codename)
            except Exception as e:
                print(f"Error saving to DB: {e}")

        # broadcast equipment id to network
        try:
            self.udp.broadcast_equipment_code(int(eq_id))
        except ValueError:
            pass
    
    def change_network(self):
        # open popup to change udp ip address
        new_ip = simpledialog.askstring("Network Settings", "Enter Target IP:", initialvalue = self.udp.ip_address)
        if new_ip:
            self.udp.ip_address = new_ip
            print(f"Network changed to {new_ip}")

    def clear_entries(self, event = None):
        # loop through all rows and clear text boxes
        for row in self.red_entries + self.green_entries:
            row["id"].delete(0, tk.END)
            row["name"].config(state = "normal", bg = "white")
            row["name"].delete(0, tk.END)
            row["eq"].delete(0, tk.END)

    def start_game(self, event = None):
        print("Starting Game...")

    def show_menubar(self):
        self.controller.config(menu = self.menubar)