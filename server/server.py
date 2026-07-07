import socket, threading
from server.data_collection import get_data
from shared.conf import *
from shared.models import *

class Client:
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        self.buffer = b''

class Server:
    def __init__(self):
        self.client = None
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(SOCK_TIMEOUT)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))
        self.sock.listen()
        print(f"[LISTENING]: {HOST}:{PORT}") #logs

#=============================================================#

    def run(self):
        try:
            while self.running:
                try:
                    sock, addr = self.sock.accept()
                    client = Client(sock, addr)
                    client.sock.settimeout(SOCK_TIMEOUT)
                    if self.client is None:
                        print(f"[CONNECTED]: {client.addr[0]}:{client.addr[1]}") #logs
                        self.client = client
                        threading.Thread(target=self.handle_client, args=(client,)).start()
                    else:
                        print(f"[REJECTED]: {client.addr[0]}:{client.addr[1]}") #logs
                        self.send(client, Packet(type=-1))
                        self.disconnect_client(client)
                except socket.timeout: pass
                except OSError: pass
                except Exception as e: print(f"[Accept Error] - {e}") #logs
        except KeyboardInterrupt: self.shutdown()

#=============================================================#

    def handle_client(self, client):
        while self.client and self.running:
            try:
                raw_packet = client.sock.recv(MAX_MSG_SIZE)
                if not raw_packet:
                    self.disconnect_client(client)
                    continue
                client.buffer += raw_packet
                while b'\n' in client.buffer:
                    packet, client.buffer = self.client.buffer.split(b'\n', 1)
                    msg = Packet.model_validate_json(packet.decode())
                    self.process_msg(client, msg)
            except socket.timeout: pass
            except OSError: pass
            except Exception as e:
                print(f"[Recv Error {client.addr[0]}:{client.addr[1]}] - {e}") #logs
                self.disconnect_client(client)

#=============================================================#

    def process_msg(self, client, msg):
        print(f"[RECEIVED]: {client.addr[0]}:{client.addr[1]} - {msg}") #logs
        self.send(client, get_data(msg.type))

    def send(self, client, packet):
        try:
            if self.client:
                print(f"[SENT]: {client.addr[0]}:{client.addr[1]} - {packet}") #logs
                client.sock.sendall(packet.model_dump_json().encode() + b'\n')
        except Exception as e:
            print(f"[Send Error {client.addr[0]}:{client.addr[1]}] - {e}") #logs
            self.disconnect_client(client)

    def shutdown(self):
        self.running = False
        try:
            if self.sock: self.sock.shutdown(socket.SHUT_RDWR)
        except: pass
        try:
            if self.sock: self.sock.close()
        except: pass
        if self.client:
            self.disconnect_client(self.client)
            self.client = None
        print(f"[SHUTDOWN]") #logs

    def disconnect_client(self, client):
        if client is None: return
        if client == self.client: self.client = None
        try: client.sock.shutdown(socket.SHUT_RDWR)
        except: pass
        try: client.sock.close()
        except: pass
        print(f"[DISCONNECTED]: {client.addr[0]}:{client.addr[1]}") #logs