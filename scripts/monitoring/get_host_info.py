#!/usr/bin/env python
# coding=utf-8

__author__ = 'iLiKo'

import fcntl
import multiprocessing
import os
import platform
import re
import socket
import struct
import subprocess
import sys
import time

# Name
def get_hostname():
    return socket.gethostname()

# IP Address
def get_interface_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

def get_lan_ip():
    interfaces = []
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127."):
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
    for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip

# OS
def get_os_info():
    os_name = platform.system()
    os_ver = ""
    os_ver_mac = platform.mac_ver()[0]
    if os_name == "Darwin":
        os_ver = os_ver_mac
        os_name = 'Mac OS'
        if os_ver_mac >= "10.0":
            os_name = "Mac OS X"

    if os_name == "Linux":
        os_name = platform.linux_distribution()[0]
        if platform.linux_distribution()[2] != '':
            os_ver = platform.linux_distribution()[1] + ' ' + '(' + platform.linux_distribution()[2] + ')'
        else:
            os_name = platform.linux_distribution()[1]
    return {"os_name": os_name, "os_version": os_ver}

# Arch
def get_arch():
    if sys.maxsize > 2**32:
        # check if arch is real 64-bit
        arch = platform.machine()
    else:
        arch = platform.machine()
    return arch

# Kernel and CPU (real)
def get_kernel_cpu():
    return platform.release() + " on " + platform.processor()

# Processor information
def get_processor_info():
    if platform.system() == "Linux":
        command = subprocess.Popen(["cat", "/proc/cpuinfo"], stdout=subprocess.PIPE).communicate()[0].strip()
        return command.splitlines()[4][13:]
    elif platform.system() == "Darwin":
        return subprocess.check_output(['/usr/sbin/sysctl', "-n", "machdep.cpu.brand_string"]).strip()
    elif platform.system() == "Windows":
        return platform.processor()
    else:
        return ""

# Number of cores
def get_core_info():
    cores_number = multiprocessing.cpu_count()
    if cores_number > 1:
        core = str(cores_number) + " cores"
    else:
        core = str(cores_number) + " core"
    return core

# System uptime
def get_system_uptime():
    o = os.popen("uptime").read()
    if o.find("min") != -1:
        if o.find("days") != -1:
            m = re.search("up ((\d+) days,)?\s+(\d+) min,", o)
            g, s = m.groups(), ""
            if g[1]:
                if int(g[1]) == 1:
                    s = s + g[1] + " day, 0 hours, "
                else:
                    s = s + g[1] + " days, 0 hours, "
            if int(g[2]) == 1:
                s = s + g[2] + " minute"
            else:
                s = s + g[2] + " minutes"
        else:
            m = re.search("up ((\d+) min,)", o)
            g, s = m.groups(), ""
            if g[1] and int(g[1]) > 0:
                if int(g[1]) == 1:
                    s = s + g[1] + " minute"
                else:
                    s = s + g[1] + " minutes"
    else:
        m = re.search("up ((\d+) days,)?\s+(\d+):(\d+)", o)
        g, s = m.groups(), ""
        if g[1]:
            if int(g[1]) == 1:
                s = s + g[1] + " day, "
            else:
                s = s + g[1] + " days, "
        if g[2] and int(g[2]) > 0:
            if int(g[2]) == 1:
                s = s + g[2] + " hour, "
            else:
                s = s + g[2] + " hours, "
        if int(g[3]) == 1:
            s = s + g[3] + " minute"
        else:
            s = s + g[3] + " minutes"
    return s

# Linux-only alternative (for memory)
"""
#----------------------------------------
# Gives a human-readable uptime string
def uptime():

     try:
         f = open("/proc/uptime")
         contents = f.read().split()
         f.close()
     except:
        return "Cannot open uptime file: /proc/uptime"

     total_seconds = float(contents[0])

     # Helper vars:
     MINUTE  = 60
     HOUR    = MINUTE * 60
     DAY     = HOUR * 24

     # Get the days, hours, etc:
     days    = int( total_seconds / DAY )
     hours   = int( ( total_seconds % DAY ) / HOUR )
     minutes = int( ( total_seconds % HOUR ) / MINUTE )
     seconds = int( total_seconds % MINUTE )

     # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
     string = ""
     if days > 0:
         string += str(days) + " " + (days == 1 and "day" or "days") + ", "
     if len(string) > 0 or hours > 0:
         string += str(hours) + " " + (hours == 1 and "hour" or "hours") + ", "
     if len(string) > 0 or minutes > 0:
         string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes") + ", "
     string += str(seconds) + " " + (seconds == 1 and "second" or "seconds")

     return string

#print "The system uptime is:", uptime()
"""

# Number of running processes
def get_processes_numbers():
    process_count = 0
    if platform.system() == "Linux":
        pids = []
        for subdir in os.listdir('/proc'):
            if subdir.isdigit():
                pids.append(subdir)
        process_count = len(pids)+1
    elif platform.system() == "Darwin":
        processoutput = subprocess.Popen(['launchctl', 'list'], stdout=subprocess.PIPE).stdout.read()
        process_count = len((processoutput).split('\n')) - 1
    return process_count

# CPU load averages
def get_cpu_load_avg():
    load_avg = os.getloadavg()
    return load_avg

# CPU usage
def __cpu_time_deltas(sample_duration):
    """Return a sequence of cpu time deltas for a sample period.
    Elapsed cpu time samples taken at 'sample_time (seconds)' apart.

    Each value in the sequence is the amount of time, measured in units
    of USER_HZ (1/100ths of a second on most architectures), that the system
    spent in each cpu mode: (user, nice, system, idle, iowait, irq, softirq, [steal], [guest]).

    on SMP systems, these are aggregates of all processors/cores.
    """

    with open('/proc/stat') as f1:
        with open('/proc/stat') as f2:
            line1 = f1.readline()
            time.sleep(sample_duration)
            line2 = f2.readline()
    deltas = [int(b) - int(a) for a, b in zip(line1.split()[1:], line2.split()[1:])]
    return deltas

def cpu_percents(sample_duration=1):
    """Return a dictionary of usage percentages and cpu modes.
    Elapsed cpu time samples taken at 'sample_time (seconds)' apart.

    cpu modes: 'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq'

    On SMP systems, these are aggregates of all processors/cores.
    """

    deltas = __cpu_time_deltas(sample_duration)
    total = sum(deltas)
    percents = [100 - (100 * (float(total - x) / total)) for x in deltas]
    return {
        'user': percents[0],
        'nice': percents[1],
        'system': percents[2],
        'idle': percents[3],
        'iowait': percents[4],
        'irq': percents[5],
        'softirq': percents[6],
    }

def get_cpu_use():
    if platform.system() == "Linux":
        linux_cpu_use = cpu_percents()
        return dict(user="%.2f" % linux_cpu_use["user"], system="%.2f" % linux_cpu_use["system"],
                    idle="%.2f" % linux_cpu_use["idle"])
    elif platform.system() == "Darwin":
        proc = subprocess.Popen(['/usr/bin/top', '-l', '1', '-n' '0'], shell=False, stdout=subprocess.PIPE)
        proc_comm = proc.communicate()[0]
        top_out = proc_comm.splitlines()[3][11:]
        user = top_out.split()[0]
        system = top_out.split()[2]
        idle = top_out.split()[4]
        return {"user": user, "system": system, "idle": idle}
    else:
        return {"user": "unknown", "system": "unknown", "idle": "unknown"}

# Memory
## If Linux
# I got the getRAMinformations method from PhJulien's post
# From here http://www.raspberrypi.org/phpBB3/viewtopic.php?f=32&t=22180
# Return the RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM

def getRAMinformations():
    p = os.popen('free')
    i = 0
    while 1:
        i += 1
        line = p.readline()
        if i == 2:
            return line.split()[1:4]

# Now, using the information received from the getRAMinfo's method
# i build the getRAMpercentage method, so you can show the amount
# of ram used in percentage

def getRAMpercentage(total, used):
    return (used * 100) / total

def linux_memory():
    infoRAM = getRAMinformations()
    totalRAM = round(int(infoRAM[0]) / 1000, 1)
    usedRAM = round(int(infoRAM[1]) / 1000, 1)
    freeRAM = round(int(infoRAM[2]) / 1000, 1)
    percentRAM = getRAMpercentage(totalRAM, usedRAM)
    return infoRAM, totalRAM, usedRAM, freeRAM, percentRAM

def get_linux_memory():
    if platform.system() == "Linux":
        memory = linux_memory()[1:4:1]
    elif platform.system() == "Darwin":
        memory = ("unknown", "unknown", "unknown")
    else:
        memory = ("unknown", "unknown", "unknown")
    result = {
        "memory_total": memory[0],
        "memory_used": memory[1],
        "memory_free": memory[2]
    }
    return result

def get_host_info():
    cpu_load_avg = get_cpu_load_avg()
    host_info = {
        "hostname": get_hostname(),
        "lan_ip": get_lan_ip(),
        "architecture": get_arch(),
        "kernel_cpu": get_kernel_cpu(),
        "processor_info": get_processor_info(),
        "core_info": get_core_info(),
        "system_uptime": get_system_uptime(),
        "processes": get_processes_numbers(),
        "cpu_load_avg_0": cpu_load_avg[0],
        "cpu_load_avg_1": cpu_load_avg[1],
        "cpu_load_avg_2": cpu_load_avg[2],
    }
    host_info.update(get_linux_memory())
    host_info.update(get_cpu_use())
    host_info.update(get_os_info())
    return host_info

if __name__ == "__main__":
    cpu_use = get_cpu_use()
    os_info = get_os_info()
    memory = get_linux_memory()
    print "System hostname: %s (%s)" % (get_hostname(), get_lan_ip())
    print "Operating system: %s %s" % (os_info["os_name"], os_info["os_version"])
    print "System architecture: %s" % get_arch()
    print "Kernel and CPU: %s" % get_kernel_cpu()
    print "Processor information: %s (%s)" % (get_processor_info(), get_core_info())
    print "System uptime: %s" % get_system_uptime()
    print "Running processes: %s" % get_processes_numbers()
    print "CPU load averages: {0:.2f} (1 min) {1:.2f} (5 min) {2:.2f} (15 min)".format(get_cpu_load_avg()[0],
                                                                                       get_cpu_load_avg()[1],
                                                                                       get_cpu_load_avg()[2])
    print "CPU usage: User {0:s}, System {1:s}, Idle {2:s}".format(cpu_use["user"], cpu_use["system"], cpu_use["idle"])
    print "Memory: %s total, %s used, %s free" % (memory["memory_total"], memory["memory_used"], memory["memory_free"])

    print get_host_info()