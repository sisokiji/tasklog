import sys
import os
import csv
import re
import glob
import shutil
import datetime
import subprocess
import numpy as np

TASKLIST_PATH = "./tasks.csv"
TASKLOG_PATH = "./" + datetime.date.today().strftime("%Y%m%d") + ".txt"

def load_tasklist(filepath):
    with open(filepath) as f:
        reader = csv.reader(f)
        tasks_arr = np.array([row for row in reader])
        tasks = tasks_arr[:, 1]
        return list(map(lambda x: x.strip(), tasks))

def load_tasklog(filepath):
    with open(filepath, "a+") as f:
        pass
    with open(filepath, "r+") as f:
        return f.readlines()

def archive_logfile():
    archive_dir = 'archive'
    if not os.path.exists(archive_dir): 
        os.makedirs(archive_dir)
    files = glob.glob("./*")
    for file in files:
        if re.match(r"./\d{8}.txt", file) and file != TASKLOG_PATH:
            shutil.move(file, archive_dir)

def append_log(filepath, taskname):
    with open(filepath, "a+") as f:
        timeStr = datetime.datetime.today().strftime("%H:%M")
        f.write("{}~ {}".format(timeStr, taskname))

def log_endtime(filepath, tasklog):
    if len(tasklog) == 0 or tasklog[-1].endswith("\n"):
        return

    lastline = tasklog[-1]
    timeStr = datetime.datetime.today().strftime("%H:%M")
    lastline_with_end_time = re.sub("(\d\d:\d\d~)( )", "\\g<1>"+str(timeStr)+" ", lastline)
    lastline_with_end_time += "\n"
    tasklog[-1] = lastline_with_end_time

    with open(filepath, "w") as f:
        f.writelines(tasklog)

if __name__ == "__main__":
    archive_logfile()

    if len(sys.argv) <  2:
        subprocess.Popen([r"/usr/bin/code", TASKLIST_PATH])
    elif sys.argv[1] == "0":
        tasklog = load_tasklog(TASKLOG_PATH)
        log_endtime(TASKLOG_PATH, tasklog)

    else :
        tasklog = load_tasklog(TASKLOG_PATH)   
        tasks = load_tasklist(TASKLIST_PATH)
        tasknum = int(sys.argv[1])
        taskname = tasks[tasknum-1]

        if len(tasklog)==0 or tasklog[-1].endswith("\n"):
            append_log(TASKLOG_PATH, taskname)
        else:
            log_endtime(TASKLOG_PATH, tasklog)
            append_log(TASKLOG_PATH, taskname)
