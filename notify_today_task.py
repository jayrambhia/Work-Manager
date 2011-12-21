#!/usr/bin/python2.7

import os
import gdbm
import datetime
import pickle
from operator import itemgetter
import time

def notify(str1):
  os.system("notify-send Todays_Task " + str1)
  return

def get_task_list(date,tmdb):
  task_list=[]
  task_key = pickle.dumps(date)
  try:
    task_list = pickle.loads(tmdb[task_key])
    task_list = sorted(task_list,key=itemgetter(1,2)) # Sort task_list according to status and priority.
  except KeyError:
    return task_list
  return task_list

def main():
  date = datetime.date.today().timetuple()[:3]
  DB = gdbm.open('/home/jay/Python/Workspace/TaskManager/Taskmanager','c') # Directory of the database
  task_key = pickle.dumps(date)
  task_list=get_task_list(date,DB)
  str1="'"
  if task_list:
    for i in range(len(task_list)):
      if task_list[i][1]==0:
        str1 = str1 + '\n->' + task_list[i][0] + '\t--Incomplete'
      else:
        str1 = str1 + '\n->' + task_list[i][0]
  else:
    str1 = str1 + 'No Task'
  str1 = str1 + "'"
  if task_list:
#    time.sleep(6) Delyas the log in
    for i in range(len(task_list)):
      notify(str1)
  else:
    notify(str1)


if __name__ == '__main__':
  main()
