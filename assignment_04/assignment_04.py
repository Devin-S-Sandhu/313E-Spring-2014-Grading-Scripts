from os.path import os, exists
from datetime import datetime, timedelta
from functools import *
import math
import subprocess
import sys
import re
import difflib
import time

from poker_func import *

pipes = {'stdout':subprocess.PIPE, 'stdin':subprocess.PIPE, 'stderr':subprocess.PIPE}

outputFilename = 'assignment_04.txt'
filename = "Poker.py"
dateString = "2-8-2013 23:00:00"

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
      assign04(csid, True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign04(csid, False)
  outputFile.close()

def assign04(csid, writeToFile) :
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
  output format = 5 pts
  duplicate = 5 pts
  sorting = 5 pts
  11 test runs (5 pts each) = 55 points
  '''
  inputText = [2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 6]
  outputList = []
  formatted = True
  hasDuplicate = False
  isSorted = True
  notSorted = []
  hasDupl = []

  if not (fileToGrade == '' and late != -1):
    for numPlayers in inputText:
      try:
        process = subprocess.Popen(['python3', fileToGrade], **pipes)
        out = process.communicate(bytes(str(numPlayers), 'UTF-8'))[0]
        outputGame = str(out)[2:-1].split('\\n')

        indType = numPlayers + 2
        indSoln = numPlayers + indType + 1

        # check output format of all 12 tests
        if outputGame[0].find('Enter the number of hands to play: ') < 0:
          formatted = False
        if formatted:
          for i in range(1, numPlayers + 1):
            if i >= len(outputGame):
              formatted = False
            elif outputGame[i].find('Hand ' + str(i) + ': ') < 0:
              formatted = False
            if not formatted: break
        if formatted:
          for i in range(indType, numPlayers + indType):
            if i >= len(outputGame):
              formatted = False
            elif outputGame[i].find('Hand ' + str(i - indType + 1) + ': ') < 0:
              formatted = False
            if not formatted: break
        if formatted:
          for i in range(indSoln, len(outputGame)):
            if (outputGame[i] != '') and (outputGame[i].find('Hand ') < 0) and (outputGame[i].find('.') < 0):
              formatted = False

        outputList.append(list(filter(None, outputGame)))
      except KeyboardInterrupt:
        print(' passed ^C')

  grade = 0

  # run tests
  for count in range(len(outputList)):
    output = outputList[count]
    numPlayers = inputText[count]
    hands = []
    for test in output:
      hand = []
      for token in test.split():
        if isCard(token):
          hand.append(card(token))
      if len(hand) == 5:
        hands.append(hand)
    if len(hands) != numPlayers:
      comments.append('failed test ' + str(count + 1) + ' (-5) [Wrong Number of Hands]')
      print('Failed Test ' + str(count + 1) + ':')
      print('\tWrong Number of Hands')
    else:
      values = []
      failed = False

      if not hasDuplicate:
        hasDuplicate, hand = checkDuplicate(hands)
        if hasDuplicate:
            hasDupl.append(hand)

      for i in range(len(hands)):
        hand = hands[i]
        sortedHand1 = sorted(hand, reverse=True)
        h1, sortedHand2 = is10(sortedHand1)
        h2, sortedHand3 = isStraight(sortedHand1)

        if isSorted:
          isSorted = sameHand(hand, sortedHand1) or sameHand(hand, sortedHand2) or sameHand(hand, sortedHand3)
          if not isSorted:
            notSorted.append(printHand(hand))

        if not failed:
          offset = 1
          if output[numPlayers + offset].find('1') < 0:
            offset = 0

          for j in range(numPlayers + offset, len(output)):
            line = output[j].rstrip()
            pos = line.find(str(i + 1))

            if pos >= 0:
              for p in range(pos, len(line)):
                if 'a' <= line[p].lower() <= 'z':
                  pos = p
                  break
              line = line[pos:].lower()

              v = -1
              if line in mapping:
                v = mapping[line]

              if (v != h1) and (v != h2):
                strList = map(lambda x: printHand(x), hands)
                comm = 'Hand = ' + printHand(hand) + '; Output = ' + line
                comments.append('failed test ' + str(count + 1) + ' (-5) ' + comm)
                print('Failed Test ' + str(count + 1) + ':')
                print('\tHand: ' + printHand(hand))
                print('\tType: ' + line)
                failed = True

              if not failed:
                if v == h1:
                  values.append(computeScore(h1, sortedHand2))
                else:
                  values.append(computeScore(h2, sortedHand3))

              break

            if failed:
              break

      if len(values) != 0:
        maxScore = max(values)

      winners = [i + 1 for i in range(len(values)) if values[i] >= maxScore][::-1]

      if len(winners) == 1:
        if output[-1].find(str(winners[0])) < 0:
          strList = map(lambda x: printHand(x), hands)
          comm = 'Hands = [' + ', '.join(strList) + ']; Winner = ' + str(winners[0]) + '; Output = ' + output[-1]
          comments.append('failed test ' + str(count + 1) + ' (-5) ' + comm)
          print('Failed Test ' + str(count + 1) + ':')
          print('\tCorrect: ' + str(winners[0]))
          print('\tOutput: ' + output[-1])
          failed = True

      else:
        pos = -1
        for w in winners:
          if output[pos].find(str(w)) < 0:
            strList = map(lambda x: printHand(x), hands)
            comm = 'Hands = [' + ', '.join(strList) + ']; Winner = ' + str(w) + '; Output = ' + output[pos]
            comments.append('failed test ' + str(count + 1) + ' (-5) ' + comm)
            print('Failed Test ' + str(count + 1) + ':')
            print('\tCorrect: ' + str(w))
            print('\tOutput: ' + output[pos])
            failed = True
            break

      if not failed:
        grade += 5

  if formatted:
    grade += 5
  else:
    comments.append('wrong output format (-5)')

  if isSorted:
    grade += 5
  else:
    comm = '[' + ', '.join(notSorted) + ']'
    comments.append('spotted incorrectly sorted hand (-5) ' + comm)

  if not hasDuplicate:
    grade += 5
  else:
    comm = 'Hands = [' + ', '.join(hasDupl) + ']'
    comments.append('spotted duplicate cards (-5)')

  if grade == 70:
    print('Perfection =D')
  else:
    print('Grade: ' + str(grade)+'/70')

  #checking for header and style
  input("Hit Enter to cat")
  print(subprocess.getoutput('cat ' + fileToGrade))
  headerInput = input("Header(y/n, hit enter for y): ")
  if headerInput == 'y' or headerInput == '':
    header = True
  else:
    header = False
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
