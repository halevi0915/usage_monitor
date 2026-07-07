import socket, platform, psutil
from shared.models import Packet

def get_data(type):
    match type:
        case 0:
            info = {
                "hostname": socket.gethostname(),
                "ip_address": socket.gethostbyname(socket.gethostname()),
                "os": platform.system(),
            }
        case 1:
            info = {
                "core_count": psutil.cpu_count(logical=False),
                "uptime": psutil.boot_time(),
                "cpu_percent": psutil.cpu_percent(interval=None),
                "cpu_freq": psutil.cpu_freq().current,
                "virtual_memory_total": psutil.virtual_memory().total,
                "virtual_memory_percent": psutil.virtual_memory().percent,
            }
        case 2:
            info = {
                "partitions": [{
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total": psutil.disk_usage(partition.mountpoint).total,
                    "percent": psutil.disk_usage(partition.mountpoint).percent,
                } for partition in psutil.disk_partitions()]
            }
        case _: raise ValueError
    return Packet(type=type, content=info)