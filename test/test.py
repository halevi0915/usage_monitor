from systeminfo import CpuInfo, MemoryInfo, DiskInfo, SensorInfo, ProcessInfo
import app.conf as conf
import readchar
import threading
import time
import os

cpu = CpuInfo()
mem = MemoryInfo()
disk = DiskInfo()
sensor = SensorInfo()
process = ProcessInfo()
running = True
delay = 1

def keyboard_thread():
    global running
    while running:
        if readchar.readkey() == "q":
            running = False

threading.Thread(target=keyboard_thread, daemon=True).start()

while running:
    os.system("clear")
    print("Press 'q' to quit.")

    print(f"CPU Cores: {cpu.count}")
    for i, core in enumerate(cpu.cores):
        print(f"Core {i}:")
        print(f"  Time: {core.time}")
        print(f"  Percent: {core.percent}%")
        print(f"  Frequency: {core.freq} GHz")
    cpu.update()
    
    print("\nMemory Information:")
    print(f"Memory Total: {mem.total/1024/1024:.2f} MB")
    print(f"Memory Used: {mem.used/1024/1024:.2f} MB")
    print(f"Memory Free: {mem.free/1024/1024:.2f} MB")
    print(f"Memory Percent: {mem.percent}%")
    print(f"Swap Total: {mem.swap_total/1024/1024:.2f} MB")
    print(f"Swap Used: {mem.swap_used/1024/1024:.2f} MB")
    print(f"Swap Free: {mem.swap_free/1024/1024:.2f} MB")
    print(f"Swap Percent: {mem.swap_percent}%")
    mem.update()

    print("\nDisk Partitions:")
    for partition in disk.partitions:
        print(f"  Device: {partition.device}")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  Filesystem Type: {partition.fstype}")
        print(f"  Options: {partition.opts}")
        print(f"  Total Size: {partition.total/1024/1024:.2f} MB")
        print(f"  Used Size: {partition.used/1024/1024:.2f} MB")
        print(f"  Free Size: {partition.free/1024/1024:.2f} MB")
        print(f"  Percent Used: {partition.percent}%")
    disk.update()

    print("\nSensor Information:")
    if sensor.temperatures:
        print("Temperatures:")
        for name, entries in sensor.temperatures.items():
            print(f"  {name}:")
            for entry in entries:
                print(f"    Label: {entry.label}, Current: {entry.current}°C, High: {entry.high}°C, Critical: {entry.critical}°C")
    else:
        print("No temperature sensors found.")
    if sensor.fans:
        print("Fans:")
        for name, entries in sensor.fans.items():
            print(f"  {name}:")
            for entry in entries:
                print(f"    Label: {entry.label}, Current: {entry.current} RPM")
    else:
        print("No fan sensors found.")
    if sensor.battery:
        print("Battery:")
        print(f"  Percent: {sensor.battery.percent}%")
        print(f"  Time Left: {sensor.battery.secsleft} seconds")
        print(f"  Power Plugged: {'Yes' if sensor.battery.power_plugged else 'No'}")
    else:
        print("No battery sensor found.")
    sensor.update()

    print("\nProcess Information:")
    print(f"Total Processes: {process.total_processes}")
    for proc in process.processes:
        print(f"  PID: {proc.pid}, Name: {proc.name}, Status: {proc.status}, Memory: {proc.memory_info.rss/1024/1024:.2f} MB, CPU Percent: {proc.cpu_percent}%")

    process.update()

    time.sleep(delay)

print("STOPPED")