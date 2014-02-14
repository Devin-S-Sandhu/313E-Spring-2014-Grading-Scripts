#run in the same directory as the file you're exploding (Where the grading script was run from)
import sys

if (len(sys.argv) == 2):
  f = open(sys.argv[1], 'r')
else:
  print("Please have the name of the file to explode as a command line arguement")
  exit()


skip_first = True
for line in f:
  #skips the "CSID Grade Comments" line
  if(skip_first):
    skip_first = False
    continue

  vals = line.strip().split('\t')
  #if they're no comments there's no file to write
  if(len(vals) == 3):
    fileName = vals[0] + '/' + sys.argv[1]
    try:
      f2 = open(fileName,'w')
      f2.write('Grade: ' + vals[1] +'\n')
      f2.write('Comments: ' + vals[2].replace(', ','\n'))
      f2.close()
      print('Wrote ' + fileName)
    except:
      print('\tFailed to write '+ fileName)

f.close()
