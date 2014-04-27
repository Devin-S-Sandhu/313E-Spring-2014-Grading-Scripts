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

outputFilename = 'assignment_14.txt'
filename = "BST_Cipher.py"
dateString = "4-21-2014 23:30:00"

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
      assign14(csid, True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign14(csid, False)
  outputFile.close()

def assign14(csid, writeToFile) :
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
  75 points (caps at 70)
  10 7 pt runs
  5 for formatting
  '''

  #fillerText = ['Substitution Cipher','Enter Plain Text to be Encoded: Encoded Text: ','Enter Encoded Text to be Decoded: Decoded Plain Text: ','Vigenere Cipher','Enter Plain Text to be Encoded: Enter Pass Phrase (no spaces allowed): Encoded Text: ','Enter Encoded Text to be Decoded: Enter Pass Phrase (no spaces allowed): Decoded Plain Text: ']
  fillerText = ['Enter encryption key: ', 'Enter string to be encrypted: Encrypted string: ', 'Enter string to be decrypted: Decrypted string: ']
  inputText = []
  outputText = []

  #TODO: Modify this text: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1========================

  outputText.append(['*!<!<!>!<<!*!<','meet me'])
  outputText.append(['<!<<!<><>><<<!<><>><<<!<><>>!<<<!>>!<><>>!<>>!<><>><<<!<<<>>','civic racecar'])
  outputText.append(['<><>><<!<<!<<!*!<<<!<><>><<!<<','meet me'])
  outputText.append(['>>!>>>!>>>!<!*!>>>>>>>>>>>>><','no cd'])
  outputText.append(['<<<><<!<><>><<<!<><!<<<>!<<!<<<!<><>><!<<<!<<<><!<><>>!<<<><','ttt   '])

  inputText.append(['meet me', 'meet me','*!<!<!>!<<!*!<'])
  inputText.append(['the quick brown fox jumps over the lazy dog', 'Hello World','<<<>!<><!>><!<><!<<<>!<<<!<>>!<<<><<!<<<>!<<!<<<>!<<<><<!<>>'])
  inputText.append(['the quick brown fox jumps over the lazy dog', 'meet me','<><>><<!<<!<<!*!<<<!<><>><<!<<'])
  inputText.append(['abcdefghijklm zyxwvutsrqpno', 'CDd ay','>>>>>>>>>>>>><<<<<<<<<<<!>>>>>>>>>>>>><<<<<<<<<<<>!<!>>!>>>'])
  inputText.append(['the quick brown fox jumps over the lazy dog', 'Alice N BOB','*!*!*!<<<!<<<!<<<'])

  if not (fileToGrade == '' and late != -1):
    correctFormatting = True
    count = 0
    for (inText,outText) in zip(inputText,outputText):
      try:
        process = subprocess.Popen(['python3',fileToGrade], **pipes)
        out = process.communicate(bytes('\n'.join(inText), 'UTF-8'))[0]
        answers = list(filter(None, str(out)[2:-1].split('\\n')))
      except KeyboardInterrupt:
        print(' passed ^C')

      #there's probably a way to loop through this jazz but meh
      correctAnswers = []
      correctAnswers.append(fillerText[0])
      correctAnswers.append(fillerText[1] + outText[0])
      correctAnswers.append(fillerText[2] + outText[1])

      for (theirs, ours) in zip(answers,correctAnswers):
        if correctFormatting:
          if theirs.strip() != ours.strip():
            correctFormatting = False
            grade -= 5
            comments.append('Incorrect Formatting (-5) YOURS:' + theirs +' OURS:'+ours)
            print('\tIncorrect Formatting')
            print('\tTheirs\n\t'+theirs)
            print('\tOurs\n\t'+ours)
          else:
            print('Passed Test ' + str(count + 1))
        if not correctFormatting:
          t = theirs.split(':')[-1].strip() 
          o = ours.split(':')[-1].strip()
          if t != o: 
            comments.append('  || Failed Test '+ str(count+1))
            comments.append(': ' + inText[(count%3)] + ' with key: ' + inText[0])
            comments.append(' YOURS:' + theirs +' OURS:'+ours)
            print('Failed Test '+ str(count+1))
            print(inText[(count%3)] + ' with key: ' + inText[0])
            print('\tTheirs\n\t'+theirs)
            print('\tOurs\n\t'+ours)
            grade -= 7
          else:
            print('Passed Test ' + str(count+1))
        count += 1
  if grade == 70:
    print('Perfection =D')
  elif grade < 0:
    grade = 0
    print('Grade: ' + str(grade)+'/70')
  else:
    print('Grade: ' + str(grade)+'/70')

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