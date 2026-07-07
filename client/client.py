import socket, threading, time
from shared.conf import *
from shared.models import *

class Client:
    def __init__(self, local_info):
        self.lock = threading.Lock()
        self.local_info = local_info

#=============================================================#

    def run(self, ip):
        try:
            while self.local_info.running:
                try:
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.settimeout(SOCK_TIMEOUT)
                    self.sock.connect((ip, PORT))
                    print("[CONNECTED]")
                    self.local_info.connected = True
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
        while self.local_info.connected:
            self.send(Packet(type=self.local_info.current_tab))
            time.sleep(REQUEST_DELAY)

#=============================================================#

    def recv_loop(self):
        while self.local_info.connected:
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
            case 0: self.local_info.general_info = msg.content
            case 1: self.local_info.system_info = msg.content
            case 2: self.local_info.disk_info = msg.content
            case -1: print(f"ERROR: {msg.content}")


    def send(self, packet):
        try:
            #print(f"[SENT] {packet}")
            self.sock.sendall(packet.model_dump_json().encode() + b'\n')
        except Exception as e:
            print(f"[Send Error] - {e}")
            self.disconnect()

    def disconnect(self):
        with self.lock:
            if not self.local_info.connected: return
            print("[DISCONNECTING]")
            self.local_info.connected = False
            self.sock.close()
