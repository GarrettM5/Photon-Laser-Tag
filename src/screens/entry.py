import tkinter as tk
from tkinter import simpledialog

class PlayerEntryScreen(tk.Frame):
    def __init__(self, parent, controller, db, udp):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.udp = udp
        self.configure(bg="#121212")

        # create top menu bar for network settings
        self.menubar = tk.Menu(parent)
        settings_menu = tk.Menu(self.menubar, tearoff=0)
        settings_menu.add_command(label="Change Network", command=self.change_network)
        self.menubar.add_cascade(label="Settings", menu=settings_menu)

        # create screen header
        tk.Label(self, text="EDIT CURRENT GAME", font=("Helvetica", 20, "bold"), fg="white", bg="#121212").pack(pady=10)

        # create main container for the team tables
        center_stage = tk.Frame(self, bg="#121212")
        center_stage.pack(expand=True, fill="both", padx=20)

        # create red team panel
        self.red_frame = tk.Frame(center_stage, bg="#8B0000", bd=2, relief="groove")
        self.red_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        tk.Label(self.red_frame, text="RED TEAM", font=("Courier", 18, "bold"), fg="white", bg="#8B0000").pack(pady=5)
        self.red_entries = self.create_team_grid(self.red_frame)

        # create green team panel
        self.green_frame = tk.Frame(center_stage, bg="#006400", bd=2, relief="groove")
        self.green_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)
        tk.Label(self.green_frame, text="GREEN TEAM", font=("Courier", 18, "bold"), fg="white", bg="#006400").pack(pady=5)
        self.green_entries = self.create_team_grid(self.green_frame)

        # create footer with clear and start buttons
        footer_frame = tk.Frame(self, bg="#121212")
        footer_frame.pack(side="bottom", fill="x", pady=10)
        
        self.clear_button = tk.Button(footer_frame, text="F12: Clear Players", font=("Helvetica", 10, "bold"), bg="#8B0000", fg="white", padx=15, pady=8, command=self.clear_entries)
        self.clear_button.pack(side="left", padx=20)
        
        self.start_button = tk.Button(footer_frame, text="F5: Start Game", font=("Helvetica", 10, "bold"), bg="#006400", fg="white", padx=15, pady=8, command=self.start_game)
        self.start_button.pack(side="right", padx=20)

        # bind keyboard shortcuts to functions
        parent.bind("<F5>", self.start_game)
        parent.bind("<F12>", self.clear_entries)

    def create_team_grid(self, parent_frame):
        # setup grid container
        container = tk.Frame(parent_frame, bg=parent_frame["bg"])
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # set relative column widths (codename box is wider)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=3) 
        container.grid_columnconfigure(2, weight=1)

        # create column headers
        tk.Label(container, text="User ID", font=("Helvetica", 10, "bold"), fg="white", bg=parent_frame["bg"]).grid(row=0, column=0, sticky="ew")
        tk.Label(container, text="Codename", font=("Helvetica", 10, "bold"), fg="white", bg=parent_frame["bg"]).grid(row=0, column=1, sticky="ew")
        tk.Label(container, text="Equipment ID", font=("Helvetica", 10, "bold"), fg="white", bg=parent_frame["bg"]).grid(row=0, column=2, sticky="ew")

        entries =[]
        # loop to create 15 rows of input fields
        for i in range(15):
            container.grid_rowconfigure(i + 1, weight=1)
            
            # create text boxes for id, name, and equipment
            id_entry = tk.Entry(container, font=("Helvetica", 10), justify="center", bg="#2C2C2C", fg="white", insertbackground="white")
            id_entry.grid(row=i + 1, column=0, padx=4, pady=2, sticky="ew") 
            
            name_entry = tk.Entry(container, font=("Helvetica", 10), justify="center", bg="#2C2C2C", fg="white", insertbackground="white")
            name_entry.grid(row=i + 1, column=1, padx=4, pady=2, sticky="ew")
            
            eq_entry = tk.Entry(container, font=("Helvetica", 10), justify="center", bg="#2C2C2C", fg="white", insertbackground="white")
            eq_entry.grid(row=i + 1, column=2, padx=4, pady=2, sticky="ew")

            # bind enter key to trigger database lookup and udp broadcasts
            id_entry.bind("<Return>", lambda e, id_entry=id_entry, name_entry=name_entry, eq_entry=eq_entry: self.on_id_entered(id_entry, name_entry, eq_entry))
            eq_entry.bind("<Return>", lambda e, id_entry=id_entry, name_entry=name_entry, eq_entry=eq_entry: self.on_eq_entered(id_entry, name_entry, eq_entry))

            # store the row elements in a dictionary for easy access later
            entries.append({"id": id_entry, "name": name_entry, "eq": eq_entry})
            
        return entries

    def on_id_entered(self, id_entry, name_entry, eq_entry):
        # grab the user id and ensure it is a valid number
        user_id = id_entry.get().strip()
        if not user_id.isdigit():
            if user_id:
                id_entry.delete(0, tk.END)
            return
            
        try:
            # check if player exists in database
            codename = self.db.get_player_name(user_id)
            if codename:
                # if found, auto-fill codename and lock the box
                name_entry.delete(0, tk.END)
                name_entry.insert(0, codename)
                name_entry.config(state="disabled", disabledbackground="#4A4A4A", disabledforeground="#A0A0A0")
            else:
                # if new player, unlock box and focus cursor so user can type name
                name_entry.config(state="normal", bg="#2C2C2C")
                name_entry.delete(0, tk.END)
                name_entry.focus_set() 
                return
                
            # move cursor to equipment box if name was found
            eq_entry.focus_set()
        except Exception as e:
            print(f"DB Error: {e}")

    def on_eq_entered(self, id_entry, name_entry, eq_entry):
        # grab all values from the row
        user_id = id_entry.get().strip()
        codename = name_entry.get().strip()
        eq_id = eq_entry.get().strip()
        
        # ensure equipment id is a valid number
        if not eq_id.isdigit():
            if eq_id:
                eq_entry.delete(0, tk.END)
            return

        # save the player to the database if it is a new entry
        if user_id and codename:
            try:
                self.db.add_player(user_id, codename)
            except Exception as e:
                print(f"Error saving to DB: {e}")

        # broadcast equipment id to the network
        try:
            self.udp.broadcast_equipment_code(int(eq_id))
        except ValueError:
            pass
    
    def change_network(self):
        # open popup to change udp ip address
        new_ip = simpledialog.askstring("Network Settings", "Enter Target IP:", initialvalue=self.udp.ip_address)
        if new_ip:
            self.udp.ip_address = new_ip
            print(f"Network changed to {new_ip}")

    def clear_entries(self, event=None):
        # loop through all rows and clear text boxes
        for row in self.red_entries + self.green_entries:
            row["id"].delete(0, tk.END)
            row["name"].config(state="normal", bg="#2C2C2C")
            row["name"].delete(0, tk.END)
            row["eq"].delete(0, tk.END)

    def start_game(self, event=None):
        # scrape valid player data from the text boxes to send to the next screen
        red_team_data = []
        green_team_data =[]

        # process red team
        for row in self.red_entries:
            player_id = row['id'].get().strip()
            player_name = row['name'].get().strip()
            eq_id = row['eq'].get().strip()
            if player_id and player_name and eq_id:
                red_team_data.append({'id': player_id, 'name': player_name, 'eq': eq_id})

        # process green team
        for row in self.green_entries:
            player_id = row['id'].get().strip()
            player_name = row['name'].get().strip()
            eq_id = row['eq'].get().strip()
            if player_id and player_name and eq_id:
                green_team_data.append({'id': player_id, 'name': player_name, 'eq': eq_id})

        # trigger screen transition
        self.controller.go_to_countdown(red_team_data, green_team_data)

    def show_menubar(self):
        # displays the top menu bar when this screen is active
        self.controller.config(menu=self.menubar)
