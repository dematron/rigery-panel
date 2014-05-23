#!/usr/bin/env python
__author__ = 'iLiKo'

import multiprocessing
import os
import platform
import re
import socket
import sys
import subprocess
import time
#import psutil

# Name
hostname = socket.gethostname()

# IP Address
host_ip = socket.gethostbyname(socket.gethostname())

# OS
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

# Arch
if sys.maxsize > 2**32:
    # check if arch is real 64-bit
    arch = platform.machine()
else:
    arch = platform.machine()

# Kernel and CPU (real)
kernel_cpu = platform.release() + " on " + platform.processor()

# Processor information
def get_processor_info():
    if platform.system() == "Linux":
        #command = "cat /proc/cpuinfo"
        command = subprocess.Popen(["cat", "/proc/cpuinfo"], stdout=subprocess.PIPE).communicate()[0].strip()
        return command.splitlines()[4][13:]
    elif platform.system() == "Darwin":
        return subprocess.check_output(['/usr/sbin/sysctl', "-n", "machdep.cpu.brand_string"]).strip()
    elif platform.system() == "Windows":
        return platform.processor()
    return ""

# Number of cores
cores_number = multiprocessing.cpu_count()
if cores_number > 1:
    core = str(cores_number) + " cores"
else:
    core = str(cores_number) + " core"

# System uptime
def system_uptime():
    o = os.popen("uptime").read()
    m = re.search("up ((\d+) days,)?\s+(\d+):(\d+)", o)
    if m:
        g, s = m.groups(), ""
        if g[1]:
            s = s + g[1] + " days, "
        if g[2] and int(g[2]) > 0:
            s = s + g[2] + " hours, "
        s = s + g[3] + " minutes"
    return s

# Number of running processes
def processes_numbers():
    if platform.system() == "Darwin":
        processoutput = subprocess.Popen(['launchctl', 'list'], stdout=subprocess.PIPE).stdout.read()
        process_count = len((processoutput).split('\n')) - 1
    elif platform.system() == "Linux":
        pids = []
        for subdir in os.listdir('/proc'):
            if subdir.isdigit():
                pids.append(subdir)
        process_count = len(pids)+1
    return process_count

# CPU load averages
def cpu_load_avg():
    load_avg = os.getloadavg()
    return load_avg

# CPU usage
#cpu_use = psutil.cpu_percent(interval=0)
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

def cpu_use():
    if platform.system() == "Darwin":
        proc = subprocess.Popen(['/usr/bin/top', '-l', '1', '-n' '0'], shell=False, stdout=subprocess.PIPE)
        proc_comm = proc.communicate()[0]
        top_out = proc_comm.splitlines()[3][11:]
        user = top_out.split()[0]
        system = top_out.split()[2]
        idle = top_out.split()[4]
        return user, system, idle
    elif platform.system() == "Linux":
        linux_cpu_use = cpu_percents()
        return linux_cpu_use["user"], linux_cpu_use["system"], linux_cpu_use["idle"]
#except:
#    print "CPU STATISTICS UNKNOWN: the stsci_check_cpu script encountered an error."


# Memory
#memory_usag = psutil.phymem_usage()
#mem = psutil.virtual_memory()
## If Linux
# I got the getRAMinformations method from PhJulien's post
# From here http://www.raspberrypi.org/phpBB3/viewtopic.php?f=32&t=22180
# Return the RAM informations (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM

def getRAMinformations():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

# Now, using the informations recevied from the getRAMinfo's method
# i build the getRAMpercentage method, so you can show the amount
# of ram used in percentage

def getRAMpercentage(total, used):
    return((used * 100) / total)

def linux_memory():
    infoRAM = getRAMinformations()
    totalRAM = round(int(infoRAM[0]) / 1000,1)
    usedRAM = round(int(infoRAM[1]) / 1000,1)
    freeRAM = round(int(infoRAM[2]) / 1000,1)
    percentRAM = getRAMpercentage(totalRAM, usedRAM)
    return infoRAM, totalRAM, usedRAM, freeRAM, percentRAM

if platform.system() == "Linux":
    memory = linux_memory()[1:3:1]
#elif platform.system() == "Darwin":
#    memory =

#print memory_usag
#print totalRAM
#print usedRAM
#print freeRAM
#print "Used ram: " + str(round(percentRAM,2)) + "%" # we need only 2 decimals

print "System hostname: %s (%s)" % (hostname, host_ip)
print "Operating system: %s %s" % (os_name, os_ver)
print "System architecture: %s" % arch
print "Kernel and CPU: %s" % kernel_cpu
print "Processor information: %s (%s)" % (get_processor_info(), core)
print "System uptime: %s" % system_uptime()
print "Running processes: %s" % processes_numbers()
print "CPU load averages: %.2f (1 min) %.2f (5 min) %.2f (15 min)" % (cpu_load_avg()[0], cpu_load_avg()[1], cpu_load_avg()[2])
print "CPU usage: User %s, System %s, Idle %s" % (cpu_use())
print "Memory: %s total, %s used" % memory



#print mem.total/2**30

#oss = os.uname()
#oss2 = sys.platform
#oss3 = platform.release() +" on "+ platform.processor()
#oss4 = platform.machine()
#oss5 = platform.system()
#print oss5