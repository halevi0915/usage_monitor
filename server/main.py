import signal, sys
from server.server import Server

def shutdown_handler(signum, frame):
    print("[SIGTERM DETECTED]")
    server.shutdown()
    sys.exit(0)

server = Server()
signal.signal(signal.SIGTERM, shutdown_handler)
server.run()