import socket, threading, time, random
from shared.conf import *
from shared.models import *

class Client:
    def __init__(self):
        self.lock = threading.Lock()
        self.connected = False
        self.reconnect_loop()

#=============================================================#

    def reconnect_loop(self):
        try:
            while True:
                try:
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.settimeout(SOCK_TIMEOUT)
                    self.sock.connect((IP, PORT))
                    print("[CONNECTED]")
                    self.connected = True
                    self.buffer = b''

                    recv_t = threading.Thread(target=self.recv_loop)
                    send_t = threading.Thread(target=self.send_loop)

                    recv_t.start()
                    send_t.start()

                    recv_t.join()
                    send_t.join()

                except socket.timeout: pass
                except Exception as e:
                    if getattr(e, "errno", None) != 111: print(f"[Connection Error] - {e}")

                self.sock.close()
                print("[RECONNECTING]")
                time.sleep(RECONNECT_DELAY)

        except KeyboardInterrupt:
            print(f"[SHUTDOWN]")
            self.disconnect()

#=============================================================#

    def send_loop(self):
        while self.connected:
            self.send(Packet(type=random.choice(["general", "system", "disk"])))
            time.sleep(REQUEST_DELAY)

#=============================================================#

    def recv_loop(self):
        while self.connected:
            try:
                raw_packet = self.sock.recv(MAX_MSG_SIZE)
                if not raw_packet:
                    self.disconnect()
                    continue
                self.buffer += raw_packet
                while b'\n' in self.buffer:
                    packet, self.buffer = self.buffer.split(b'\n', 1)
                    msg = Packet.model_validate_json(packet.decode())
                    self.process_msg(msg)
            except socket.timeout: pass
            except Exception as e:
                print(f"[Recv Error] - {e}")
                self.disconnect()

#=============================================================#

    def process_msg(self, msg):
        match msg.type:
            case "general":
                print(f"[GeneralInfo] {msg.content["hostname"]}")
            case "system":
                print(f"[SystemInfo] {msg.content["cpu_percent"]}")
            case "disk":
                print(f"[DisklInfo] {len(msg.content["partitions"])}")

    def send(self, packet):
        try:
            print(f"[SENT] {packet}")
            self.sock.sendall(packet.model_dump_json().encode() + b'\n')
        except Exception as e:
            print(f"[Send Error] - {e}")
            self.disconnect()

    def disconnect(self):
        with self.lock:
            if not self.connected: return
            print("[DISCONNECTING]")
            self.connected = False
            self.sock.close()

#=============================================================#
IP = input("Server IP: ").strip() or "127.0.0.1"

Client()
