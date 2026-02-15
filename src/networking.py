import socket

class UDPServer:
    def __init__(self):
        self.broadcast_port = 7500
        self.receive_port = 7501
        self.ip_address = "127.0.0.1" # same as localhost
        self.local_address = "0.0.0.0" 

        # setup socket for sending data
        self.broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # setup socket for receiving data
        self.receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_sock.bind((self.local_address, self.receive_port))
        self.receive_sock.setblocking(False)

    def broadcast_equipment_code(self, equipment_id):
        # sends the equipment ID to the game server
        if not equipment_id:
            return
        try:
            message = str(equipment_id).encode('utf-8')
            # send to port 7500
            self.broadcast_sock.sendto(message, (self.ip_address, self.broadcast_port))
            print(f"Broadcasting Equipment ID {equipment_id} to {self.ip_address}:{self.broadcast_port}")
        except Exception as e:
            print(f"Error broadcasting: {e}")
