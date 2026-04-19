import psycopg2
from psycopg2 import OperationalError

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        # connects to photon postgresql database
        try:
            self.conn = psycopg2.connect(
                dbname="photon",
                # user="student",     
                # password="student", 
                # host="127.0.0.1"
            )
            print("Database Connected Successfully")
        except OperationalError as e:
            print(f"Database Connection Failed: {e}")

    def get_player_name(self, player_id):
        # Looks up players codename basad on their user ID
        if not self.conn: 
            return None
        try:
            cursor = self.conn.cursor()
            query = "SELECT codename FROM players WHERE id = %s"
            cursor.execute(query, (player_id,))
            result = cursor.fetchone()

            # return the name if found, otherwise return none
            if result:
                return result[0] # return the name found
            return None
        except Exception as e:
            print(f"Error fetching player: {e}")
            return None

    def add_player(self, player_id, codename):
        # adds a new player or updates an existing one if user ID already exists
        if not self.conn: return
        try:
            cursor = self.conn.cursor()
            # update existing player to prevent db crash from duplicate ids
            if self.get_player_name(player_id):
                query = "UPDATE players SET codename = %s WHERE id = %s"
                cursor.execute(query, (codename, player_id))
            # insert brand new player
            else:
                query = "INSERT INTO players (id, codename) VALUES (%s, %s)"
                cursor.execute(query, (player_id, codename))
                
            # save changes to the database
            self.conn.commit() 
            print(f"Saved Player {player_id}: {codename}")
        except Exception as e:
            print(f"Error saving player: {e}")
            # undo the transaction if an error occurred
            self.conn.rollback()

    def close(self):
        # safely close the database connectio
        if self.conn:
            self.conn.close()
