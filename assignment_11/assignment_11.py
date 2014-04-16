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

outputFilename = 'assignment_11.txt'
outputFile = open(outputFilename, 'a')
filename = "Josephus.py"
dateString = "3-28-2014 23:30:00"

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
      assign11(csid, True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign11(csid, False)
  outputFile.close()

def assign11(csid, writeToFile) :
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
  First file: 16 points + 1 point for survivor
  Second file: 16 points + 1 point for survivor
  Third file: 16 points + 1 point for survivor
  Fourth file: 18 points + 1 point for survivor
  Total 70 points

  Extra Credit: 10 points
  Total 80 points
  '''
  if not (fileToGrade == '' and late != -1):

    index = 1
    print('\n==================================FILE 1===================================\n')

    
    testsFailed = ""

    #copying file to read and correct output file to the current directory
    os.system('cp ../josephus.txt josephus.txt') #TODO Read from EVERY josephus1234.txt
    correctFile = open('../output.txt', 'r') #TODO Read from EVERY output1234.txt
    correctLines = correctFile.read().splitlines()

    #Getting output from student
    outputLines = subprocess.getoutput('python3 ' + fileToGrade).splitlines()

    #Length of the files (output and correct)
    olen = len(outputLines)
    clen = len(correctLines)
    minLen = min(len(outputLines), len(correctLines)) 
    
    #Lengths don't match
    if(clen != olen):
      grade -= 1
      #They didn't output last surviving soldier
      if(clen == (olen + 1)):
        testsFailed += "Didn't print surviving soldier \n"
    
    #Check that all the other lines are the same
    for i in range(minLen):
      if outputLines[i] != correctLines[i]:
        grade -= 16
        testsFailed += "Didn't print surviving soldier \n"
        break
    
    #write to the comments file
    if len(testsFailed) != 0:
      comments.append("On josephus1.txt: " + testsFailed)
    else:
      print('Passed all tests on file 1')

    # print('\n============================FILE 2===================================\n')
    # os.system('cp ../josephus2.txt josephus.txt')
    # outputLines2 = subprocess.getoutput('python3 ' + fileToGrade).splitlines()
    # correctFile2 = open('../output2.txt', 'r')
    # correctLines2 = correctFile2.read().splitlines()
    # minLen2 = min(len(outputLines2), len(correctLines2))
    # testsFailed2 = []
    # for j in range(minLen2):
    #   if outputLines2[j] == correctLines2[j]:
    #     grade += 1
    #   else:
    #     print('\tTheir Output')
    #     print('\t' + outputLines2[j])
    #     print('\tCorrect Output')
    #     print('\t' + correctLines2[j])
    #     correctInput = input("Is this line ok? (y/h/n, h is for half, hit enter for y): ")
    #     if correctInput == 'y' or correctInput == '':
    #       grade += 1
    #     elif correctInput == 'h':
    #       grade += 0.5
    #       testsFailed2.append(j)
    #     else:
    #       testsFailed2.append(j)

    # if len(testsFailed2) != 0:
    #   comments.append("File 2: Failed lines: " + ' '.join(str(x) for x in testsFailed2))
    # else:
    #   print('Passed all tests on file 2')

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

main()
