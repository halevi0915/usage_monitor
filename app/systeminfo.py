import psutil

class Core:
    def __init__(self, count, time, percent, freq):
        self.count = count
        self.time = time
        self.percent = percent
        self.freq = freq

class CpuInfo:
    def __init__(self):
        self.update()
    
    def update(self):
        self.count = psutil.cpu_count(logical=False)
        self.uptime = psutil.boot_time()
        self.cores = []

        for i in range(self.count):
            self.cores.append(
                Core(
                    count=i,
                    time=psutil.cpu_times(percpu=True)[i],
                    percent=psutil.cpu_percent(interval=None, percpu=True)[i],
                    freq=[freq.current/1000 for freq in psutil.cpu_freq(percpu=True)][i]
                )
            )

class MemoryInfo:
    def __init__(self):
        self.update()
    
    def update(self):
        self.total = psutil.virtual_memory().total
        self.used = psutil.virtual_memory().used
        self.free = psutil.virtual_memory().free
        self.percent = psutil.virtual_memory().percent
        self.swap_total = psutil.swap_memory().total
        self.swap_used = psutil.swap_memory().used
        self.swap_free = psutil.swap_memory().free
        self.swap_percent = psutil.swap_memory().percent

class Partition:
    def __init__(self, device, mountpoint, fstype, opts, total, used, free, percent):
        self.device = device
        self.mountpoint = mountpoint
        self.fstype = fstype
        self.opts = opts
        self.total = total
        self.used = used
        self.free = free
        self.percent = percent

class DiskInfo:
    def __init__(self):
        self.update()
    
    def update(self):
        self.partitions = []
        for partition in psutil.disk_partitions():
            self.partitions.append(Partition(
                device=partition.device,
                mountpoint=partition.mountpoint,
                fstype=partition.fstype,
                opts=partition.opts,
                total=psutil.disk_usage(partition.mountpoint).total,
                used=psutil.disk_usage(partition.mountpoint).used,
                free=psutil.disk_usage(partition.mountpoint).free,
                percent=psutil.disk_usage(partition.mountpoint).percent
            ))

class SensorInfo:
    def __init__(self):
        self.update()
    
    def update(self):
        self.temperatures = psutil.sensors_temperatures()
        self.fans = psutil.sensors_fans()
        self.battery = psutil.sensors_battery()

class Process:
    def __init__(self, pid, name, status, username, memory_info, cpu_percent):
        self.pid = pid
        self.name = name
        self.status = status
        self.username = username
        self.memory_info = memory_info
        self.cpu_percent = cpu_percent
    
class ProcessInfo:
    def __init__(self):
        self.update()
    
    def update(self):
        self.total_processes = len(psutil.pids())

        self.processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status', 'username', 'memory_info', 'cpu_percent']):
            try:
                process = Process(
                    pid=proc.info['pid'],
                    name=proc.info['name'],
                    status=proc.info['status'],
                    username=proc.info['username'],
                    memory_info=proc.info['memory_info'],
                    cpu_percent=proc.info['cpu_percent']
                )
                self.processes.append(process)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass