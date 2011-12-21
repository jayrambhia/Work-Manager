#!/usr/bin/python2.7

'''
Today Date added
Show List added
Date string added
Change date added
Validity check of date added
Add Task added
Get Int input added
Task Status added
Check Task added
Remove Task added
Getting Task according to date added
Show Menu added
Priority added
List sorted according to priority and status
Change Priority added
A function named sync_DB added to sync the database
negative days also included in changing the dates
Number of days(from today) included in getting the date of the task
Notes and Description Added
View notes and Description added
change_date() function modified. Now looks good.
check_valid(date) funciton modified.
'''

import pickle
import gdbm
import time
import datetime
from operator import itemgetter

def check_valid(date):
  year, mon, day = date
  year = str(year)
  mon = str(mon)
  day = str(day)
  date = year+mon+day
  try:
    time.strptime(date,'%Y%m%d')
    return 1
  except ValueError:
    return 0

def change_date(num):
  sec = num*24*3600
  sec = time.time()+sec
  t = time.ctime(sec)
  t_struct = time.strptime(t)
  new_date = t_struct[0:3]
  return new_date    
  
def get_date_string(date):
  year, mon, day = date
  string = str(mon)+'/'+str(day)+'/'+str(year)
  return string
  
def get_today():
  date_today = datetime.date.today().timetuple()[:3]
  return date_today
  
def get_task_date():
  date_today = get_today()
  print '1. Task for today\n2. Task for tomorrow\n3. Task for yesterday.\n4. Task for some other day.\n5. Exit'
  n=get_int('Choose an option:\t')
  
  if n==1:
    date=date_today
  elif n==2:
    date = change_date(1)
  elif n==3:
    date = change_date(-1)
  elif n==4:
    date = get_task_from_date()
  elif n==5:
    return
            
  else:
    print 'Incorrect option'
    date=get_task_date(tmdb)
  
  return date
  
def get_task_from_date():
  date_today = get_today()
  print 'Today is', get_date_string(date_today)
  print '1. Number of days after Today.\n2. Number of days before today.\n3. Specific Date.\n4. Exit.'
  n = get_int()
  
  if n==1 or n==2:
    num = get_int('Number of days\t')
    if n==1:
      date = change_date(num)
    else:
      date = change_date(-num)
  else:
    print 'Number of days should be less than 30'
    date = get_task_from_date()
  elif n==3:
    print 'Enter date(month day year):'
    d = raw_input().split()
    date = (int(d[2]),int(d[0]),int(d[1]))
    if not check_valid(date):
      date = get_task_from_date()
  elif n==4:
    return
  else:
    print 'Invalid option'
    date = get_task_from_date()
  return date     

def get_task_list(date,tmdb):
  task_list=[]
  task_key = pickle.dumps(date)
  try:
    task_list = pickle.loads(tmdb[task_key])
    task_list = sorted(task_list,key=itemgetter(1,2)) # Sort task_list according to status and priority.
  except KeyError:
    return task_list
  return task_list
  
def get_int(string=''):
  while True:
    try:
      n=int(raw_input(string))
      break
    except ValueError:
      print 'Enter int'
  return n

def get_task_num(date,tmdb):
  show_task(date,tmdb)
  task_list = get_task_list(date,tmdb)
  if task_list:
    n=get_int('Enter the number of the task(0 to exit)')
    
    if n<0 or n>len(task_list):
      print 'Invalid option'
      n = get_task_num(date,tmdb)
      return n 
    elif n==0:
      return 0
    else:
      return n
          
def show_task_main(tmdb):
  print 'Show Task'
  date = get_task_date()
    
  if date:
    show_task(date,tmdb)
    return
  else:
    return
      
def show_task(date,tmdb):
  print
  date_today = get_today()
  if date == date_today:
    print "Today's tasks."
  elif date[0:2]==date_today[0:2]:
    if date[2]==date_today[2]-1:
      print "Yesterday's tasks."
    elif date[2]==date_today[2]+1:
      print "Tomorrow's tasks."
    else:
      print date,'Task.'
  else:
    print date,'Task.'
  
  task_list = get_task_list(date,tmdb)
  if task_list:
    for i in range(len(task_list)):
      print str(i+1)+'.', task_list[i][0],
      if task_list[i][1] == 0:
        if task_list[i][2] == 0:
          print '\t--Urget',
        elif task_list[i][2] == 1:
          print '\t--Important',
        print '\t---Incomplete'
      else:
        print '\t---Completed'
  else:
    print 'No task for',get_date_string(date)
    print
      
def assign_task_main(tmdb):
  print 'Assign Task for'
  date = get_task_date()
  
  if date:
    assign_task(date,tmdb)
    return
  else:
    return
      
def assign_task(date,tmdb):
  task_list=get_task_list(date,tmdb)
  task='42'
  while task!='0':
    print 'Enter Task(0 to end).'
    task = raw_input()
    if task!='0':
      if task:
        priority = get_priority()
        des = get_description()
        notes = get_notes()
        task_list.append([task,0,priority,des,notes])
  tmdb = sync_DB(date,task_list,tmdb)
    
def get_description():
  des = raw_input('Add Description of the task.(Enter to exit)')
  return des

def get_notes():
  notes = raw_input('Add notes about the task.(Enter to exit)')
  return notes

def show_des_note(tmdb):
  date = get_task_date()
  if date:
    n = get_task_num(date,tmdb)
    if n:
      task_list = get_task_list(date,tmdb)
      print task_list[n-1][0]
      print '\nDescription:'
      if task_list[n-1][3]:
        print task_list[n-1][3]
      else:
        print 'No Description about this task'
      print '\nNotes:'
      if task_list[n-1][4]:
        print task_list[n-1][4],'\n'
      else:
        print 'No notes about this task.\n'
  return
  
def check_task_main(tmdb):    
  print 'Check Tasks'
  date = get_task_date()
  if date:
    check_task(date,tmdb)
    return
  else:
    return 
          
def check_task(date,tmdb):
  n = get_task_num(date,tmdb)
  if n:
    status=42
    while status!=0 and status!=1:
      status=get_int('Check(1)--Uncheck(0)--Exit(2)')
      if status==2:
        return
    task_list = get_task_list(date,tmdb)
    task_list = change_task_status(task_list,n,status)
    tmdb = sync_DB(date,task_list,tmdb)
    check_task(date,tmdb)
    return
    
def change_task_status(task_list,n,status):
  task_list[n-1][1]=status
  return task_list
  
def get_priority():
  priority = get_int('Enter Task Priority\n0-Urgent\t1-Important\t2-Normal\tChoose an option\t')
  if priority==0 or priority==1 or priority==2:
    return priority
  else:
    print 'Incorrect option'
    priority = get_priority()
    return priority
    
def change_priority_main(tmdb):
  print 'Change Priority'
  date = get_task_date()
  if date:
    change_priority(date,tmdb)
    return
  else:
    return 
    
def change_priority(date,tmdb):
  n = get_task_num(date,tmdb)
  if n:
    priority=42
    while priority!=0 and priority!=1 and priority!= 2:
      priority=get_int('Urgent(0)--Important(1)--Normal(2)--Exit(3)')
      if priority==3:
        return
    task_list = get_task_list(date,tmdb)
    task_list = change_task_priority(task_list,n,priority)
    tmdb = sync_DB(date,task_list,tmdb)
    change_priority(date,tmdb)
    return

def change_task_priority(task_list,n,priority):
  task_list[n-1][2]=priority
  return task_list
  
def remove_task_main(tmdb):
  print 'Remove Task'
  date = get_task_date()
  if date:
    remove_task(date,tmdb)
    return
  else:
    return
     
def remove_task(date,tmdb):
  n = get_task_num(date,tmdb)
  if n:
    task_list = get_task_list(date,tmdb)
    task_list.remove(task_list[n-1])
    tmdb = sync_DB(date,task_list,tmdb)
    remove_task(date,tmdb)
    return
  else:
    print 'No task.'
    return    

def sync_DB(date,task_list,tmdb):  
  task_key=pickle.dumps(date)
  task_list_str=pickle.dumps(task_list)
  tmdb[task_key]=task_list_str
  return tmdb
  
def main():
  n=42
  date = datetime.date.today().timetuple()[:3]
  tmdb=gdbm.open('Taskmanager','c')
  show_task(date,tmdb)
  date = change_date(1)
  show_task(date,tmdb)
  while n!=5:
    n=show_menu()
    if n==1:
      show_task_main(tmdb)
    elif n==2:
      assign_task_main(tmdb)
    elif n==3:
      check_task_main(tmdb)
    elif n==4:
      change_priority_main(tmdb)
    elif n==5:
      remove_task_main(tmdb)
    elif n==6:
      show_des_note(tmdb)
    elif n==7:
      return
    else:
      print 'Invalid option'
      
def show_menu():
  print '1. Show Task.\n2. Assign new task.\n3. Check task.\n4. Change Task Priority.\n5. Remove task.\n6. Show Description and Notes about the task.\n7. Exit.'
  n=get_int('Choose an option:\t')
  
  return n

if __name__ == '__main__':
  main()
