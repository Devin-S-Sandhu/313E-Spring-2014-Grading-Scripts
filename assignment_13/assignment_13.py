from os.path import os, exists
from datetime import datetime, timedelta
from functools import *
import math
import subprocess
import sys
import re
import difflib
import time

pipes = {'stdout':subprocess.PIPE, 'stdin':subprocess.PIPE, 'stderr':subprocess.PIPE}

outputFilename = 'assignment_13.txt'
filename = "TestBinaryTree.py"
dateString = "4-12-2014 23:30:00"

outputFile = open(outputFilename, 'a')

def main():
  out = subprocess.getoutput('ls ./')
  CSIDS = out.split("\n")
  if len(sys.argv) == 3:
    outputFile.write('CSID\tGrade\tComments\n')
    lowerBound = sys.argv[1]
    upperBound = sys.argv[2] + '~';
    myList = []
    count = 0
    for item in CSIDS:
      if lowerBound <= item <= upperBound:
        if "." not in item :
          myList.append(item)
    for csid in myList :
      count += 1
      os.system('clear')
      print('======================')
      print(csid + " " + str(count) + " out of " + str(len(myList)))
      print('======================')
      assign13(csid, True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign13(csid, False)
  outputFile.close()

def assign13(csid, writeToFile) :
  fileToGrade = ""
  late = 0
  grade = 70
  style = 30
  wrongFileName = False
  header = True
  comments = []

  os.chdir(csid)
  if writeToFile: outputFile.write(csid + "\t")
  files = os.listdir('.')

  #filename checking
  for f in files :
    splitted = subprocess.getoutput('ls -l ' + f).split()
    if f == filename :
      fileToGrade = filename
      late = isLate(splitted)
      break
    elif f == filename.lower() :
      fileToGrade = filename.lower()
      late = isLate(splitted)
      wrongFileName = True
      break

  #really odd filename
  if fileToGrade == "" :
    print(subprocess.getoutput('ls -l'))
    fileToGrade = input("Which file should I grade? ")
    if fileToGrade == "" :
      if writeToFile:
        outputFile.write("0\tno file\n")
      os.chdir("..")
      return
    else :
      splitted = subprocess.getoutput('ls -l ' + fileToGrade.replace(' ','\ ')).split()
      late = isLate(splitted)
      wrongFileName = True

  #grading time!
  '''
  5 tests (13 pts each)
  - isSimilar (3 pts)
  - printLevel (6 pts)
  - getHeight (2 pts)
  - numNodes (2 pts)

  format (5 pts)
  '''
  grade = 5
  for run in range(1, 6):
    print('===== Test', run, '=====')
    cur, timeout = 0, 15
    os.system('cp ../input' + str(run) + '.txt input.txt')
    sub = subprocess.Popen(['python3', filename], **pipes)
    while cur < timeout and sub.poll() is None:
      cur += 1
      time.sleep(1)

    if sub.poll() is None:
      sub.terminate()
      comments.append('test', run, 'did not terminate (-10)')
    else:
      output = sub.communicate()[0].decode('utf-8')
      correct = []
      for line in open('../output' + str(run) + '.txt', 'r').read().split('\n'):
        line.strip()
        if line != '':
          correct.append(line)
      student = []
      for line in output.split('\n'):
        line.strip()
        if line != '':
          student.append(line)

      if len(student) != len(correct):
        comments.append('incorrect format (-5)')
        grade = 0
        break
      else:
        if student[0].strip() != correct[0].strip():
          comments.append('failed isSimilar in test ' + str(run) + '(-3)')
        else:
          grade += 3

        numWrong = 0
        for i in range(1,7):
          if ':' in student[i]:
            sout = set()
            for j in student[i].split(':')[1].strip().split(' '):
              if j != '':
                sout.add(int(j))
            cout = set()
            for j in correct[i].split(':')[1].strip().split(' '):
              if j != '':
                cout.add(int(j))
            if sout != cout:
              numWrong += 1
        grade += (6 - numWrong)
        if numWrong != 0:
          comments.append('failed printLevel in test ' + str(run) + '(-' + str(numWrong) + ')')

        getHeight = 0
        numNodes = 0
        for i in range(7,11):
          if student[i] == correct[i]:
            if i % 2 == 1:
              getHeight += 1
            else:
              numNodes += 1

        grade = grade + getHeight + numNodes
        if getHeight != 2:
          comments.append('failed getHeight in test ' + str(run) + '(-' + str(2 - getHeight) + ')')
        if numNodes != 2:
          comments.append('failed numNodes in test ' + str(run) + '(-' + str(2 - numNodes) + ')')

  if grade == 70:
    print("<('.')^ Perfection ^('.')>")
  else:
    print(grade,'/ 70')

  #checking for header and style
  input("Hit Enter to cat first 20 lines (header)")
  print(subprocess.getoutput('head -20 ' + fileToGrade))
  headerInput = input("Header(y/n, hit enter for y): ")
  if headerInput == 'y' or headerInput == '':
    header = True
  else :
    header = False
  input("Hit Enter to cat whole file (style/comments)")
  print(subprocess.getoutput('cat ' + fileToGrade))
  style = input("Style/Other (Out of 30, hit enter for 30): ")
  gen_comments = input("General Comments?: ").rstrip().lstrip()
  gen_comments = gen_comments if len(gen_comments) is not 0 else "style"
  if not style.isdigit():
    style = 30
  else :
    style = int(style)
  if (gen_comments != "style" or style != 30):
    gen_comments += " (%+d)" % (style - 30)
    comments.append("%s" % gen_comments)

  #writing grade time!
  if late == -1:
    if writeToFile: outputFile.write('0\t More than 7 days late')
    print('Late more than 7 days!')
  else :
    if late == 3:
      comments.append("3-7 days late (-30)")
      grade -= 30
    elif late == 2:
      comments.append("2 days late (-20)")
      grade -= 20
    elif late == 1:
      comments.append("1 day late (-10)")
      grade -= 10

    if wrongFileName or not header:
      grade -= 5
      if wrongFileName and header:
        comments.append("wrong filename (-5)")
      elif header and not wrongFileName:
        comments.append("malformed header (-5)")
      else:
        comments.append("wrong filename and malformed header (-5)")

    if writeToFile: outputFile.write(str(grade+style) + "\t" + ', '.join(comments))

  if writeToFile: outputFile.write('\n')
  os.chdir("..")

#returns the number of days late an assignment is
def isLate(splitted):
  dueDate = datetime.strptime(dateString,"%m-%d-%Y %H:%M:%S")
  lateOne = dueDate + timedelta(days=1)
  lateTwo = lateOne + timedelta(days=1)
  lateSev = dueDate + timedelta(days=7)
  turninDate = datetime.strptime(splitted[5] + " " +(("0" + splitted[6]) if len(splitted[6]) == 1 else splitted[6])+ " " + splitted[7] +" 2014", "%b %d %H:%M %Y")
  if turninDate <= dueDate:
    return 0
  elif turninDate <= lateOne:
    return 1
  elif turninDate <= lateTwo:
    return 2
  elif turninDate <= lateSev:
    return 3
  else :
    return -1
  return 0

main()