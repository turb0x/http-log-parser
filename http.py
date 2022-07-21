import re
import sys
from collections import defaultdict

listDefault = []  # empty list


def counter():
    global ipCounter, statusCounter, totalCounter
    ipCounter = defaultdict(list)  # dictionary
    statusCounter = defaultdict(int)  # dictionary
    totalCounter = 0
                            # ip-------------------------------------request---status--bytes
    for pos in re.finditer(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - .*?HTTP/1.1" (\d+) (\d+)', log):
        totalCounter += 1  # counting everything
        ip = pos[1]
        status = pos[2]
        bytes = int(pos[3])
        ipCounter[(ip, status)].append(bytes)  # the dict has ip, status and bytes
        statusCounter[status] += 1  # this dict has only status


# task 1 - group by ip or sc
def ipGroup(log):
    for pos in re.finditer(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.*?)\] (.*?)(\d+) (\d+)', log):
        ip = pos[1]
        date = pos[2]
        request = pos[3]
        status = pos[4]
        bytes = pos[5]
        found = [ip, date, request, status, int(bytes)]  # formatting all the data
        listDefault.append(found)  # and appending to list


def statusGroup(log):
    for pos in re.finditer(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.*?)\] (.*?)(\d+) (\d+)', log):
        ip = pos[1]
        date = pos[2]
        request = pos[3]
        status = pos[4]
        bytes = pos[5]
        found = [status, ip, date, request, int(bytes)]  # same as ip
        listDefault.append(found)  # same as ip


# task 2 - calculate for each groups
def ipCount(log):
    counter()
    for a, b in ipCounter.items():
        count = len(b)
        percentage = '{percent:.2%}'.format(percent =count / totalCounter)  # getting the percentage from ip dict
        total_bytes = sum(b)
        ip = a[0]
        status = a[1]
        counted = [ip, status, count, percentage, total_bytes]
        listDefault.append(counted)


def statusCount(log):
    counter()
    for a, b in statusCounter.items():
        count = b
        percentage = '{percent:.2%}'.format(percent =count / totalCounter)  # getting the percentage from status dict
        counted = [a, percentage]
        listDefault.append(counted)


def help():
    print("USAGE: http.py [log_file] [-argument] [optional size]")
    print("-ipgroup - shows the log grouped by ip")
    print("-statusgroup - shows the log grouped by status")
    print("-ipcount - counts the ips, percentage and total bytes transferred")
    print("-statuscount - shows the status and percentage")


if __name__ == '__main__':
    if len(sys.argv) > 4:
        print("Too much arguments.")
        help()
        exit()
    if len(sys.argv) > 2 :
        filename = sys.argv[1]
        command = sys.argv[2]
        with open(filename, 'r') as logfile:
            log = logfile.read()
            if command == "-ipgroup":
                ipGroup(log)
                try:  # task 4 - limit the size
                    size = sys.argv[3]
                    print(*sorted(listDefault[:int(size)], key=lambda l: (l[4]), reverse=True), sep="\n")
                    print("[IP | Date | Request | Status | Bytes]")
                except:
                    print(*sorted(listDefault, key=lambda l: (l[4]), reverse=True), sep="\n")  # task 3 - descending order
                    print("[IP | Date | Request | Status | Bytes]")
            elif command == "-statusgroup":
                statusGroup(log)
                try:  # task 4 - limit the size
                    size = sys.argv[3]
                    print(*sorted(listDefault[:int(size)], key=lambda l: (l[4]), reverse=True), sep="\n")
                    print("[Status | IP | Date | Request | Bytes]")
                except:
                    print(*sorted(listDefault, key=lambda l: (l[4]), reverse=True), sep="\n") # task 3 - descending order
                    print("[Status | IP | Date | Request | Bytes]")
            elif command == "-ipcount":
                ipCount(log)
                try:  # task 4 - limit the size
                    size = sys.argv[3]
                    print(*sorted(listDefault[:int(size)], key=lambda l: (l[4]), reverse=True), sep="\n")
                    print("[IP | Status | Count | Percentage | Total bytes]")
                except:
                    print(*sorted(listDefault, key=lambda l: (l[4]), reverse=True), sep="\n") # task 3 - descending order
                    print("[IP | Status | Count | Percentage | Total bytes]")
            elif command == "-statuscount":
                statusCount(log)
                try:  # task 4 - limit the size
                    size = sys.argv[3]
                    print(*sorted(listDefault[:int(size)], key=lambda l: (l[1]), reverse=True), sep="\n")
                    print("[Status | Percentage]")
                except:
                    print(*sorted(listDefault, key=lambda l: (l[1]), reverse=True), sep="\n" )# task 3 - descending order
                    print("[Status | Percentage]")
            else:
                print("Incorrect arguments.")
                help()
    else:
        print("Incorrect arguments.")
        help()
