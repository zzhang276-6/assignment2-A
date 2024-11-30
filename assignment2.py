#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py
Author: "zzhang276"
Semester: "Enter FALL 2024"

The python code in this file is original work written by
"Student Name". No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. I have not shared this python script
with anyone or anything except for submission for grading.
I understand that the Academic Honesty Policy will be enforced and
violators will be reported and appropriate action will be taken.

Description: This script visualizes system memory usage and memory usage of specific programs in a user-friendly bar graph format.

'''


import argparse #Used to parse command line arguments
import os, sys #Used to interact with the Python interpreter and OS

def parse_command_args() -> object:
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",epilog="Copyright 2023")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("-H", "--human-readable", action='store_true', help="human-readable format.")
    parser.add_argument("program", type=str, nargs='?', help="if a program is specified, show memory use of all associated processes. Show only total use is not.")
    args = parser.parse_args()
    return args
# create argparse function
# -H human readable
# -r running only

def percent_to_graph(percent: float, length: int=20) -> str:
    "turns a percent 0.0 - 1.0 into a bar graph"
    ...
# percent to graph function
    num_hashes = int(percent * length)
    num_spaces = length - num_hashes
    bar = '#' * num_hashes + ' ' * num_spaces
    return bar
#This function converts a percentage between 0.0 and 1.0 into a bar graph consisting of # symbols and spaces.
def get_sys_mem() -> int:
    ...
    "Return total system memory in kB"
    #The get_sys_mem function reads and returns the total system memory (in kB) from the /proc/meminfo file.
    with open("/proc/meminfo", 'r') as f:
        for line in f:
            if line.startswith("MemTotal"):
                mem_total = int(line.split()[1])
                return mem_total
def get_avail_mem() -> int:
    "return total memory that is currently in use"
    ...
    #The get_avail_mem function retrieves and returns the available system memory (in KB) from the /proc/meminfo file.
    with open("/proc/meminfo", "r") as f:
        for line in f:
            if line.startswith("MemAvailable"):
                mem_available = int(line.split()[1])
                return mem_available
def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    #The pids_of_prog function uses the pidof command to retrieve all of the process IDs (PIDs) that are associated with a given program name.
    ...
    try:
        result = os.popen(f'pidof {app_name}').read().strip()
        if result:
            return result.split()
        return []
    except Exception as e:
        print(f"Error finding pids: {e}", file=sys.stderr)
        return []

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the resident memory used, zero if not found"
    #The rss_mem_of_pid function reads the /proc/[pid]/status file to retrieve the Resident Set Size (RSS) memory associated with a given process, and returns the value in kB.
    ...
    try:
        with open(f'/proc/{proc_id}/status', 'r') as file:
            for line in file:
                if line.startswith('VmRSS'):
                    return int(line.split()[1])
    except FileNotFoundError:
        return 0
    return 0
def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    #This function converts memory sizes from KiB to a higher unit (e.g., MiB, GiB) and returns the value in a human-readable format. The function allows specifying the number of decimal places to display.
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
        args = parse_command_args()

        # 获取系统总内存和可用内存
        total_mem = get_sys_mem()
        avail_mem = get_avail_mem()
        used_mem = total_mem - avail_mem
        used_percent = used_mem / total_mem

        if not args.program:
            # Displays the total system memory usage when no program is specified.
            #The script calculates the total system memory usage and displays it as a bar graph.
            if args.human_readable:
                total_mem_str = bytes_to_human_r(total_mem)
                used_mem_str = bytes_to_human_r(used_mem)
            else:
                total_mem_str = f"{total_mem} kB"
                used_mem_str = f"{used_mem} kB"

            print(
                f"Memory [{percent_to_graph(used_percent, args.length)} | {used_percent * 100:.2f}%] {used_mem_str}/{total_mem_str}")

        else:
            # Displays the memory usage of the specified program
            pids = pids_of_prog(args.program)
            total_rss_mem = sum(rss_mem_of_pid(pid) for pid in pids)
            used_percent = total_rss_mem / total_mem

            if args.human_readable:
                total_rss_mem_str = bytes_to_human_r(total_rss_mem)
                total_mem_str = bytes_to_human_r(total_mem)
            else:
                total_rss_mem_str = f"{total_rss_mem} kB"
                total_mem_str = f"{total_mem} kB"

            # Displays the memory usage of the specified program

            for pid in pids:
                rss_mem = rss_mem_of_pid(pid)
                rss_percent = rss_mem / total_mem
                rss_mem_str = bytes_to_human_r(rss_mem) if args.human_readable else f"{rss_mem} kB"
            print(
                f"{pid:<10} [{percent_to_graph(rss_percent, args.length):<20} | {rss_percent * 100:4.0f}%] {rss_mem_str}/{total_mem_str}")

            # Printing Total Memory Usage
            print(
                f"{args.program:<15} [{percent_to_graph(used_percent, args.length)} | {used_percent * 100:.2f}%] {total_rss_mem_str}/{total_mem_str}")

   #The script gets the PIDs associated with the program.
    # process args
    # if no parameter passed,
    # open meminfo.
    # get used memory
    # get total memory
    # call percent to graph
    # print

    # if a parameter passed:
    # get pids from pidof
    # lookup each process id in /proc
    # read memory used
    # add to total used
    # percent to graph
    # take total our of total system memory? or total used memory? total used memory.
    # percent to graph.