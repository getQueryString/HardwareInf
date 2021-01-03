# From another source

from datetime import datetime
import psutil
import platform
import GPUtil

# System info
print("-" * 40, "Sys Info", "-" * 40)
uname = platform.uname()
print(f"System:                     {uname.system}")
print(f"Node name:                  {uname.node}")
print(f"Release:                    {uname.release}")
print(f"Version:                    {uname.version}")
print(f"Machine:                    {uname.machine}")
print(f"Processor:                  {uname.processor}")

# Boot time
print("-" * 40, "Boot time", "-" * 40)
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
print(f"Boot time:                  {bt.day}.{bt.month}.{bt.year} {bt.hour}:{bt.minute}.{bt.second}")

# CPU info
print("-" * 40, "CPU info", "-" * 40)
print("Actual Cores:              ", psutil.cpu_count(logical=False))
print("Logical Cores:             ", psutil.cpu_count(logical=True))
print(f"Max Frequency:              {psutil.cpu_freq().current:.1f}Mhz")
print(f"Current Frequency:          {psutil.cpu_freq().current:.1f}Mhz")
print(f"CPU usage:                  {psutil.cpu_percent()}%")
print("CPU usage/core:")
for i, perc in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"\tCore {i}:                 {perc}%")

def adjust_size(size):
    factor = 1024
    for i in ["B", "KB", "MB", "GB", "TB"]:
        if size > factor:
            size = size / factor
        else:
            return f"{size:.3f}{i}"

# RAM info
print("-" * 40, "RAM info", "-" * 40)
virtual_mem = psutil.virtual_memory()
print(f"Total:                      {adjust_size(virtual_mem.total)}")
print(f"Available:                  {adjust_size(virtual_mem.available)}")
print(f"Used:                       {adjust_size(virtual_mem.used)}")
print(f"Percentage:                 {virtual_mem.percent}%")
print("-" * 20, "SWAP", "-" * 20)
swap = psutil.swap_memory()
print(f"Total:                      {adjust_size(swap.total)}")
print(f"Free:                       {adjust_size(swap.free)}")
print(f"Used:                       {adjust_size(swap.used)}")
print(f"Percentage:                 {swap.percent}%")

# Disk info
print("-" * 40, "Disk info", "-" * 40)
partitions = psutil.disk_partitions()
for p in partitions:
    print(f"Device:                     {p.device}")
    print(f"\tMountpoint:             {p.mountpoint}")
    print(f"\tFile system type:       {p.fstype}")
    try:
        partitions_usage = psutil.disk_usage(p.mountpoint)
    except PermissionError:
        continue
    print(f"Total size:                 {adjust_size(partitions_usage.total)}")
    print(f"Used:                       {adjust_size(partitions_usage.used)}")
    print(f"Free:                       {adjust_size(partitions_usage.free)}")
    print(f"Percentage:                 {partitions_usage.percent}%")
disk_io = psutil.disk_io_counters()
print(f"Read since boot:            {adjust_size(disk_io.read_bytes)}")
print(f"Written since boot:         {adjust_size(disk_io.write_bytes)}")

# GPU info
print("-" * 40, "GPU info", "-" * 40)
gpus = GPUtil.getGPUs()
for gpu in gpus:
    print(f"ID:                     {gpu.id}, Name: {gpu.name}")
    print(f"\tLoad:                 {gpu.load * 100}%")
    print(f"\tFree Mem:             {gpu.memoryFree}MB")
    print(f"\tUsed Mem:             {gpu.memoryUsed}MB")
    print(f"\tTotal Mem:            {gpu.memoryTotal}MB")
    print(f"\tTemperature:          {gpu.temperature} °C")

# Network info
print("-" * 40, "Network info", "-" * 40)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"Interface:                  {interface_name}")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"\tIP Address:             {address.address}")
            print(f"\tNetmask:                {address.netmask}")
            print(f"\tBroadcast IP:           {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f"\tMAC Address:    {address.address}")
            print(f"\tNetmask:            {address.netmask}")
            print(f"\tBroadcast MAC:  {address.broadcast}")
net_io = psutil.net_io_counters()
print(f"Total Bytes send:           {adjust_size(net_io.bytes_sent)}")
print(f"Total Bytes recieved:       {adjust_size(net_io.bytes_recv)}")