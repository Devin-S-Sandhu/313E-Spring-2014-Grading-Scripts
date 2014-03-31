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

outputFilename = 'assignment_09.txt'
outputFile = open(outputFilename, 'a')
filename = "MagicSquare.py"
dateString = "3-19-2014 23:30:00"

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
      assign09(csid, True)

  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================') 
    assign09(csid, False)
  outputFile.close()

def checkFormatting(square):
  try:
    lenRows = set(len(r) for r in square)
    if len(square) == 3:
      return len(lenRows) == 1 and len(set(r.count(' ') for r in square)) == 1
    else: #might do something fancier, but this should work
      return len(lenRows) == 1

  except:
    print("ran into an error in checkFormatting\n",sys.exc_info())
    print('Input:\n' + str(square))
    return False


def checkMagicSquare(strSquare):
  try:
    square = []
    for r in strSquare:
      square.append([int(x) for x in r.split()])

    sums = []
    #rows
    for row in square:
      sums.append(sum(row))
    #cols
    for x in range(len(square)):
      temp = 0
      for row in square:
        temp += row[x]
      sums.append(temp)
    #diagonals
    diagOne = 0
    diagTwo = 0
    for x in range(len(square)):
      diagOne += square[x][x]
      diagTwo += square[len(square)-x-1][len(square)-x-1]
    sums.append(diagOne)
    sums.append(diagTwo)
    return sums.count(sums[0]) == len(sums) and len(square) == len(square[0])
  except:
    print("ran into an error in checkMagicSquare\n",sys.exc_info())
    print('Input:\n' + str(strSquare))
    return False

def checkPermutations(squares):
  for square in squares:
    if not checkMagicSquare(square):
      return False

  # these are the unique 3x3 squares
  correctSet = {'492357816','276951438','618753294','834159672','294753618','672159834','816357492','438951276'}
  squareSet = set()
  for square in squares:
    s = ''.join(square).replace(' ','')
    squareSet.add(s)
  return len(correctSet) - len(squareSet) == len(correctSet-squareSet)


def assign09(csid, writeToFile) :
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
  30: for 3 x 3 squares
    15: unique squares
    15: correct number for squares
  40: for the rest
    10: magic square of size 7
    10: magic square of size 9
    10: reprompts user for bad input, and 3x3 square
    10: formatting
  '''
  grade = 70

  #Test these squares
  inputText = ['7','9','2\n3']
  inputNums = [7,9,3]
  output = []
  formatting = True
  if not (fileToGrade == '' and late != -1):
    #grab output
    for text in inputText:
      try:
        process = subprocess.Popen(['python3', fileToGrade], **pipes)
        out = process.communicate(bytes(text, 'UTF-8'))[0]
        output.append(str(out)[2:-1].split('\\n'))
      except KeyboardInterrupt:
        print(' passed ^C on input',text)

    #test output
    checkPermutations = True
    for (out,test) in zip(output,inputNums):
      out = [x.rstrip() for x in out]
      out = list(filter(None,out))

      filtered = []
      for line in out:
        if 'square' not in line and 'odd' not in line:
          filtered.append(line)
      if len(filtered) != test + (3*8):
        print()

      square = [filtered[y] for y in range(test)]
      if formatting and not checkFormatting(square):
        formatting = False
        grade -= 10
        comment = "incorrectly formatted square (-10)"
        print(comment)
        for row in square:
          print('\t' + str(row))
        comments.append(comment)
      if not checkMagicSquare(square):
        grade -= 10
        comment = "%dx%d magic square isn't well formed (-10)"%(test,test)
        if test == 3:
          comment += ', might not have reprompted for input when given an even number'
        print(comment)
        for row in square:
          print('\t' + str(row))
        comments.append(comment)

      if checkPermutations: #only check permutations once
        checkPermutations = False
        trimmed = filtered[test:]
        for x in range(0,len(trimmed),3):
          square = []
          square.append(trimmed[x])
          square.append(trimmed[x+1])
          square.append(trimmed[x+2])
          permutations.append(square)
        if len(permutations) != 8:
          grade -= 15
          comment = 'outputted %d 3x3 squares instead of 8 (-15)'%len(permutations)
          print(comment)
          comments.append(comment)
        if not checkPermutations(permutations):
          grade -= 15
          comment = 'incorrect set of unique 3x3 squares (-15)'
          print(comment)
          comments.append(comment)

      if len(filtered) != test + (3*8):
        s = 'more' if len(filtered) > test + (3*8) else 'less'
        print('!!!\nparsed output contains %s lines than expected'%s)
        print('dumping raw output for test %dx%d'%(test,test))
        for line in out:
          print(line)
        off = input('Points off (enter is 0 too): ')
        off = off.strip()
        if off.isdigit():
          comment = input('Comment: ')
          comments.append(comment)
          grade -= int(off)

  if grade == 70:
    print("<('.')^ Perfection ^('.')>")      
  else:
    print("Grade: %d/70"%grade)      

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
