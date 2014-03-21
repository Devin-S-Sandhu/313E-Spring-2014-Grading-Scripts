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

outputFilename = 'assignment_06.txt'
filename = "BabyNames.py"
dateString = "2-21-2013 23:00:00"

outputFile = open(outputFilename, 'a')

def main():
  out = subprocess.getoutput('ls ./')
  CSIDS = out.split("\n")
  if len(sys.argv) == 3:
    outputFile.write('CSID\tGrade\tComments\n')
    #for id to id support
    lowerBound = sys.argv[1].replace('/','')
    upperBound = sys.argv[2] + '~'
    myList = []
    count = 0
    for item in CSIDS:
      if lowerBound <= item <= upperBound:
        if "." not in item :
          myList.append(item)
    for csid in myList :
      count += 1
      os.system('reset')
      print('======================')
      print(csid + " " + str(count) + " out of " + str(len(myList)))
      print('======================')
      assign06(csid, True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('reset')
    print('======================')
    print(csid)
    print('======================')
    assign06(csid, False)
  outputFile.close()

def assign06(csid, writeToFile) :
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
  5 handles wrong input
  5 handles non existant names
  60 options 1 - 6
  (5 off for wrong ordering, 10 for wrong names, 5 for wrong name singular)
  -5 formatting
  -10 for no try except
  -15 for no while loop
  -20 for not reading from web
  '''
  inputList = ['1','test','1','Devin','2','Daniel','3','1950','4','5','6','A']
  ignore = ['The names are in alphabetical']
  if not (fileToGrade == '' and late != -1):
    try:
      process = subprocess.Popen(['python3',fileToGrade], **pipes)
      out = process.communicate(bytes('\n'.join(inputList), 'UTF-8'))[0]
      answers = str(out)[2:-1].replace(':','\\n').split('\\n')
      answers = list(filter(None, [line.strip() for line in answers]))

      os.chdir('..')
      process = subprocess.Popen(['python3','BabyNames.py'], **pipes)
      correctOut = process.communicate(bytes('\n'.join(inputList), 'UTF-8'))[0]
      correctAnswers = str(correctOut)[2:-1].replace(':','\\n').split('\\n')
      correctAnswers = list(filter(None, [line.strip() for line in correctAnswers]))

      os.chdir(csid)
    except KeyboardInterrupt:
      print(' passed ^C')

    temp = []
    for a in answers:
      if a not in ignore:
        temp.append(a)
      else:
        print('ignoring: ' + a)
    answers = temp
    input('done ignoring, continue?')

    perfect = True
    for (theirs,ours) in zip(answers,correctAnswers):
      if theirs.replace(' display','') != ours.replace(' display',''):
        print('\t!!!Mismatch\n'+theirs+'\n'+ours)
        perfect = False
      elif not perfect:
        print(theirs+'\n'+ours)

    print()
    if len(answers) != len(correctAnswers):
      print(len(answers),'!=',len(correctAnswers))
      for x in range(len(correctAnswers) - len(answers)):
        print(correctAnswers[len(correctAnswers)-x -1])

  if not perfect:
    grade = input('Enter a grade out of 70: ')
    if grade == '':
      grade = 70
    else:
      grade = int(grade)
  if grade == 70:
    print('Perfection =D')
  else:
    print('Grade: ' + str(grade)+'/70')

  # style time!
  input("Hit Enter to cat whole file (style/comments)")
  print(subprocess.getoutput('cat ' + fileToGrade))

  #looking for try except block
  usedTry, usedExcept,tryExceptPoints = False, False,0
  f = open(fileToGrade, 'r')
  for line in f:
    if 'try:' in line:
      usedTry = True
    if 'except' in line:
      usedExcept = True
    if usedTry and usedExcept:
      break
  f.close()
  if not (usedTry and usedExcept):
    noTryExcept = input("!!!\ncouldn't find try except block\nhit enter to take of 10 points: ")
    if noTryExcept == "":
      tryExceptPoints = 10
      comments.append('no try except block (-10)')
  #-10 for no header
  headerInput = input("Header(y/n, hit enter for y): ")
  if headerInput == 'y' or headerInput == '':
    header = True
  else :
    header = False

  style = input("Style/Other (Out of 30, hit enter for 30): ")
  gen_comments = input("General Comments?: ").rstrip().lstrip()
  gen_comments = gen_comments if len(gen_comments) is not 0 else "style"
  if not style.isdigit():
    style = 30
  else :
    style = int(style)
  style -= tryExceptPoints
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
      elif not header and not wrongFileName:
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
  turninDate = datetime.strptime(splitted[5] + " " +(("0" + splitted[6]) if len(splitted[6]) == 1 else splitted[6])+ " " + splitted[7] +" 2013", "%b %d %H:%M %Y")
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

main()
