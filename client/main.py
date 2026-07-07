import sys, threading, time
from rich.live import Live

from client.client import Client
from client.ui import UI
from shared.conf import FPS

class LocalInfo:
    def __init__(self):
        self.general_info = None
        self.system_info = None
        self.disk_info = None

        self.current_tab = 0
        self.connected = False
        self.running = True


def main():

    if len(sys.argv) < 2:
        print("Usage: python -m client.main <host>")
        return

    local_info = LocalInfo()

    client = Client(local_info)
    ui = UI(local_info)

    threading.Thread(target=client.run, args=(sys.argv[1],), daemon=True).start()
    threading.Thread(target=ui.input_loop, daemon=True).start()

    try:
        with Live(ui.layout, refresh_per_second=FPS, screen=True):
            while local_info.running:
                ui.update()
                time.sleep(1 / FPS)

    except KeyboardInterrupt: pass
    finally: local_info.running = False

if __name__ == "__main__": main()