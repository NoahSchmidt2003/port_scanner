#!/bin/python3

import sys
import socket
from datetime import datetime
import threading

# Define our target


# Add a pretty banner
print("-" * 50)
print("Time started: " + str(datetime.now()))
startime = datetime.now()
print("-" * 50)

taget = ""
ip_arr = []
done = 0
open_ports_total = {}


def get_ip():
    f = open(sys.argv[1], "r")
    for line in f:
        line = line[:-1]
        ip_arr.append(line)


def scan(ip):
    global done
    open_ports = []
    try:
        target = socket.gethostbyname(ip)
    except socket.gaierror:
        return
    try:
        for port in range(0, 1023):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(0.01)
            result = s.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            s.close()
        done = done + 1
        open_ports_total[ip] = open_ports
    except KeyboardInterrupt:
        print("\nExiting programm.")
        return
    except socket.gaierror:
        print("\nCouldn't resolve hostname.")
        return
    except socket.error:
        print("Coudln't connect so server.")
        return
    except socket.timeout:
        return
    return


if __name__ == "__main__":
    if len(sys.argv) == 2:
        get_ip()
    else:
        print("Invalid amount of arguments ")
        print("Syntax: python3 scanner.py <youriplist.txt>")
        sys.exit()
    for i in ip_arr:
        open_ports_total.update({i: None})

    threads = list()
    for ip in ip_arr:
        thread = threading.Thread(target=scan, args=(ip,))
        threads.append(thread)
        thread.start()
    for index, th in enumerate(threads):
        th.join()

    for ip in ip_arr:
        print("Report for ip %s" % ip)
        print("Open Ports:")
        item = open_ports_total[ip]
        for i in item:
            print(i)
        print("-" * 50)

    print("Time ended: " + str(datetime.now()))
    endtime = datetime.now()
    time_delta = endtime - startime
    print("The scan took: " + str(time_delta))
    sys.exit()
