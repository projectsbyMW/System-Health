from tqdm import tqdm
from time import sleep
import psutil
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("system_health.log"), 
              logging.StreamHandler(sys.stdout)],)

RAM_THRESHOLD = 80

CPU_THRESHOLD = 80

DISK_THRESHOLD = 80

#Change the Running Processes Threshold based on your computer. 
PROC_THRESHOLD = 600

mem = psutil.virtual_memory().percent

cpu = psutil.cpu_percent(interval=0.5)

disk = psutil.disk_usage('/').percent

proc = len(psutil.pids())
process = proc/PROC_THRESHOLD *100

def monitor():
    a = 1

    if mem > RAM_THRESHOLD:
        logging.warning(f"Memory usage higher than recommended: {mem}%")
        a = 0

    if cpu > CPU_THRESHOLD:
        logging.warning(f"CPU usage higher than recommended: {cpu}%")
        a = 0

    if disk > DISK_THRESHOLD:
        logging.warning(f"Disk space lower than recommended: {disk} %")
        a = 0

    if proc > PROC_THRESHOLD:
        logging.warning(f"No. of over-running processes: {proc} %")
        a = 0

    return a

def display():
    with tqdm(total=100, desc=' cpu%', position=1) as cpubar, \
        tqdm(total=100, desc=' ram%', position=0) as rambar, \
            tqdm(total=100, desc='disc%', position=2) as discbar, \
                tqdm(total=100, desc='proc%', position=3) as procbar:
        while True:
            rambar.n=mem
            cpubar.n=cpu
            discbar.n=disk
            procbar.n=process
            if monitor() == 0:
                break
            rambar.refresh()
            cpubar.refresh()
            discbar.refresh()
            procbar.refresh()
            sleep(0.5)


#This script keeps running till some health check fails. Use Ctrl + C to manually exit.
if __name__ == "__main__":
    display()
