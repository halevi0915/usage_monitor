import socket, platform, psutil
from shared.models import Packet

def get_data(type):
    match type:
        case "general":
            info = {
                "hostname": socket.gethostname(),
                "ip_address": socket.gethostbyname(socket.gethostname()),
                "os": platform.system(),
                "os_version": platform.version(),
                "architecture": platform.architecture()[0],
            }
        case "system":
            info = {
                "core_count": psutil.cpu_count(logical=False),
                "uptime": psutil.boot_time(),
                "cpu_percent": psutil.cpu_percent(interval=None),
                "cpu_freq": psutil.cpu_freq().current,
                "virtual_memory_total": psutil.virtual_memory().total,
                "virtual_memory_percent": psutil.virtual_memory().percent,
            }
        case "disk":
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