import socket

class UDPServer:
    def __init__(self):
        # define ports and addresses for game communication
        self.broadcast_port = 7500
        self.receive_port = 7501
        self.ip_address = "127.0.0.1" 
        self.local_address = "0.0.0.0" 

        # setup socket for broadcasting data to the game hardware
        self.broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # setup socket for receiving data from the game hardware
        self.receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_sock.bind((self.local_address, self.receive_port))
        
        # sets non-blocking to false so the ui does not freeze while waiting for data
        self.receive_sock.setblocking(False) 

    def broadcast_equipment_code(self, equipment_id):
        # wrapper method to send specific equipment ids
        if not equipment_id: 
            return
        self.broadcast_code(equipment_id)

    def broadcast_code(self, code):
        # broadcasts any general code (like 202, 221, or equipment ids)
        try:
            # encode the string to bytes before sending
            message = str(code).encode('utf-8')
            self.broadcast_sock.sendto(message, (self.ip_address, self.broadcast_port))
            print(f"Network Broadcast: {code}")
        except Exception as e:
            pass

    def receive_data(self):
        # reads incoming data if available, returns none if empty
        try:
            data, _ = self.receive_sock.recvfrom(1024)
            return data.decode('utf-8')
        except BlockingIOError:
            # expected error when no data is waiting to be read
            return None
        except Exception as e:
            return None
