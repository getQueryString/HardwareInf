# https://psutil.readthedocs.io/en/latest/ & Copyright© by Fin

import os
import webbrowser
import psutil
import GPUtil
import platform

from datetime import datetime
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk


def checkPlatform():
    if os.name == "nt" or os.name == "dos":
        os.system("cls")
    elif os.name == "linux" or os.name == "linux2" or os.name == "osx" or os.name == "posix":
        os.system("clear")
    else:
        print("UNKNOWN OS")


def GitHubLink():
    webbrowser.open_new(r"https://github.com/getQueryString?tab=repositories")


def menu_file_action():
    print("DATEI")


def menu_info_action():
    print("Programmed by getQueryString  Copyright© by Fin 2021")


def menu_github_action():
    webbrowser.open_new(r"https://github.com/getQueryString/HardwareInf/blob/master/InfMain.py")


def action():
    checkPlatform()
    # System info
    print("-" * 40, "Sys Info", "-" * 40)
    uname = platform.uname()
    print(f"System:                                 {uname.system}")
    print(f"Node name:                              {uname.node}")
    print(f"Release:                                {uname.release}")
    print(f"Version:                                {uname.version}")
    print(f"Machine:                                {uname.machine}")
    print(f"Processor:                              {uname.processor}")

    # Boot time
    print("-" * 40, "Boot time", "-" * 39)
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    print(f"Boot time:                              {bt.day}.{bt.month}.{bt.year} {bt.hour}:{bt.minute}.{bt.second}")

    # CPU info
    print("-" * 40, "CPU info", "-" * 40)
    print("Actual Cores:                          ", psutil.cpu_count(logical=False))
    print("Logical Cores:                         ", psutil.cpu_count(logical=True))
    print(f"Max Frequency:                          {psutil.cpu_freq().current:.1f}Mhz")
    print(f"Current Frequency:                      {psutil.cpu_freq().current:.1f}Mhz")
    print(f"CPU usage:                              {psutil.cpu_percent()}%")
    print("CPU usage/core:")
    for i, perc in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"\tCore {i}:                         {perc}%")

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
    print(f"Total:                                  {adjust_size(virtual_mem.total)}")
    print(f"Available:                              {adjust_size(virtual_mem.available)}")
    print(f"Used:                                   {adjust_size(virtual_mem.used)}")
    print(f"Percentage:                             {virtual_mem.percent}%")
    print("-" * 20, "SWAP", "-" * 20)
    swap = psutil.swap_memory()
    print(f"Total:                                  {adjust_size(swap.total)}")
    print(f"Free:                                   {adjust_size(swap.free)}")
    print(f"Used:                                   {adjust_size(swap.used)}")
    print(f"Percentage:                             {swap.percent}%")

    # Disk info
    print("-" * 40, "Disk info", "-" * 39)
    partitions = psutil.disk_partitions()
    for p in partitions:
        print(f"Device:                                 {p.device}")
        print(f"\tMountpoint:                     {p.mountpoint}")
        print(f"\tFile system type:               {p.fstype}")
        try:
            partitions_usage = psutil.disk_usage(p.mountpoint)
        except PermissionError:
            continue
        print(f"Total size:                             {adjust_size(partitions_usage.total)}")
        print(f"Used:                                   {adjust_size(partitions_usage.used)}")
        print(f"Free:                                   {adjust_size(partitions_usage.free)}")
        print(f"Percentage:                             {partitions_usage.percent}%")
    disk_io = psutil.disk_io_counters()
    print(f"Read since boot:                        {adjust_size(disk_io.read_bytes)}")
    print(f"Written since boot:                     {adjust_size(disk_io.write_bytes)}")

    # GPU info
    print("-" * 40, "GPU info", "-" * 40)
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        print(f"ID:                                     {gpu.id}, Name: {gpu.name}")
        print(f"\tLoad:                           {gpu.load * 100}%")
        print(f"\tFree Mem:                       {gpu.memoryFree}MB")
        print(f"\tUsed Mem:                       {gpu.memoryUsed}MB")
        print(f"\tTotal Mem:                      {gpu.memoryTotal}MB")
        print(f"\tTemperature:                    {gpu.temperature} °C")

    # Network info
    print("-" * 40, "Network info", "-" * 36)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print(f"Interface:                              {interface_name}")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"\tIP Address:                     {address.address}")
                print(f"\tNetmask:                        {address.netmask}")
                print(f"\tBroadcast IP:                   {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"\tMAC Address:              {address.address}")
                print(f"\tNetmask:                      {address.netmask}")
                print(f"\tBroadcast MAC:            {address.broadcast}")
    net_io = psutil.net_io_counters()
    print(f"Total Bytes send:                       {adjust_size(net_io.bytes_sent)}")
    print(f"Total Bytes received:                   {adjust_size(net_io.bytes_recv)}")
    print(f"Total Packets send:                     {adjust_size(net_io.packets_sent)}")
    print(f"Total Packts received:                  {adjust_size(net_io.packets_recv)}")
    print(f"Total errors while receiving:           {net_io.errin}")
    print(f"Total errors while sending:             {net_io.errout}")
    print(f"Incoming packets which were dropped:    {net_io.dropin}")
    print(f"Outgoing packets which were dropped:    {net_io.dropout}")

    # Battery info
    print("-" * 40, "Battery info", "-" * 36)
    print(f"Sensor battery:")
    print(f"\t{psutil.sensors_battery()}")
    print()
    # wait = input("Done! Press any key...")

    # name = input("Name: ")
    # print("Moin " + name)


def Settings():
    # Window settings
    Tool = Tk()
    Tool.title("Hardware Check")
    Tool.geometry("1280x720")
    Tool.resizable(False, False)

    Tool.icon = PhotoImage(file="icon.png")
    Tool.iconphoto(False, Tool.icon)
    background_image = Image.open("background.png")
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = Label(Tool, image=background_photo)
    background_label.image = background_photo
    background_label.place(relwidth=1, relheight=1)

    # Buttons
    Tool.check_button = Button(Tool, text="Check Hardware", command=action, cursor="hand2")
    # Tool.check_button.config(font=("courier new", 12, "bold"))
    Tool.check_button_label = Label(Tool, text="Information about the hardware is listed",
                                    font=("courier new", 12, "bold"))
    Tool.exit_button = Button(Tool, text="Exit", command=quit, cursor="hand2")
    Tool.exit_button_label = Label(Tool, text="Quit the program",
                                   font=("courier new", 12, "bold"))
    # Links
    """
    link = Label(text="GitHub", cursor="hand2", font=("courier new", 12, "bold"), background="yellow")
    link.bind("<Button-1>", GitHubLink)
    link.place(x=100, y=0, width=50, height=20)
    link.pack(side=BOTTOM)
    """

    # Button Settings
    Tool.check_button.place(x=200, y=100, width=250, height=100)
    Tool.check_button_label.place(x=120, y=220, width=405, height=20)
    Tool.exit_button.place(x=830, y=100, width=250, height=100)
    Tool.exit_button_label.place(x=870, y=220, width=165, height=20)

    # Menu strip
    menu = Menu(Tool)
    menu_file = Menu(menu, tearoff=0)
    menu_info = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=menu_file)
    menu_file.add_command(label="Anwenden", command=menu_file_action)
    menu_file.add_separator()
    menu_file.add_command(label="Exit", command=quit)

    menu.add_cascade(label="Info", menu=menu_info)
    menu_info.add_command(label="About", command=menu_info_action)
    menu_info.add_separator()
    menu_info.add_command(label="Source Code", command=menu_github_action)
    Tool.config(menu=menu)

    mainloop()


Settings()
