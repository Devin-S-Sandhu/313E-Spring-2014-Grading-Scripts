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

outputFilename = 'assignment_15.txt'
filename = "Graph.py"
dateString = "5-5-2014 23:59:59"

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
      assign15(csid, True)
  #singleton mode
  else:
    csid = sys.argv[1]
    os.system('clear')
    print('======================')
    print(csid)
    print('======================')
    assign15(csid, False)
  outputFile.close()

def assign15(csid, writeToFile) :
  fileToGrade = ""
  late = 0
  grade = 0
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
  5 files, 2 cases (toposort/mst, djikstras)
  10 cases total
  7 points per case
  '''

  if not (fileToGrade == '' and late != -1):
    correctFormatting = True
    count = 0
    for run in range(1,6):
      try:
        print("\n=====File %d====="%run)
        testFile = 'graph%d.txt'%run
        correctFile = '../correct%d.txt'%run
        os.system('cp ../'+ testFile +' graph.txt')
        out = subprocess.getoutput('python3 ' + fileToGrade).split('\n')
        points,c = getPoints(run,out)
        grade += points
        comments += c
        print(str(points) + '/14')
        if c != []:
          print('\n'.join(c))

      except KeyboardInterrupt:
        print(' passed on run',run)
  
  grade = 0 if grade < 0 else grade
  if grade == 70:
    print('Perfection =D')
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
  if late in [-1,2,3]:
    if writeToFile: outputFile.write('0\t More than 1 day1 late')
    print('Late more than 1 day')
  elif late == 1:
    comments.append("1 day late (-10)")
    grade -= 10
    print('1 day late (-10)')

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

#Graph class because why work with 2 files =P
class Stack (object):
  def __init__ (self):
    self.stack = []

  # add an item to the top of the stack
  def push (self, item):
    self.stack.append ( item )

  # remove an item from the top of the stack
  def pop (self):
    return self.stack.pop()

  # check what item is on top of the stack without removing it
  def peek (self):
    return self.stack[len(self.stack) - 1]

  # check if a stack is empty
  def isEmpty (self):
    return (len(self.stack) == 0)

  # return the number of elements in the stack
  def size (self):
    return (len(self.stack))

class Queue (object):
  def __init__ (self):
    self.queue = []

  def enqueue (self, item):
    self.queue.append (item)

  def dequeue (self):
    return (self.queue.pop(0))

  def isEmpty (self):
    return (len (self.queue) == 0)

  def size (self):
    return len (self.queue)

class Vertex (object):
  def __init__ (self, label):
    self.label = label
    self.visited = False

  # determine if vertex was visited
  def wasVisited (self):
    return self.visited 

  # determine the label of the vertex
  def getLabel (self):
    return self.label

  # string representation of the label
  def __str__(self):
    return str (self.label)

'''
class Edge (object):
  def __init__ (self, fromVertex, toVertex, weight):
    self.u = fromVertex
    self.v = toVertex
    self.weight = weight

  # comparison operators
  def __lt__ (self, other):

  def __le__ (self, other):

  def __gt__ (self, other):

  def __ge__ (self, other):

  def __eq__ (self, other):

  def __ne__ (self, other):
'''
  
class Graph (object):
  def __init__ (self):
    self.Vertices = []
    self.adjMat = []

  # checks if a vertex label already exists
  def hasVertex (self, label):
    nVert = len (self.Vertices)
    for i in range (nVert):
      if (label == (self.Vertices[i]).label):
        return True
    return False

  # add a vertex with given label
  def addVertex (self, label):
    if not self.hasVertex (label):
      self.Vertices.append (Vertex (label))

      # add a new column in the adjacency matrix for new Vertex
      nVert = len (self.Vertices)
      for i in range (nVert - 1):
        (self.adjMat[i]).append (0)
    
      # add a new row for the new Vertex in the adjacency matrix
      newRow = []
      for i in range (nVert):
        newRow.append (0)
      self.adjMat.append (newRow)

  # add weighted directed edge to graph
  def addDirectedEdge (self, start, finish, weight = 1):
    self.adjMat[start][finish] = weight

  # add weighted undirected edge to graph
  def addUndirectedEdge (self, start, finish, weight = 1):
    self.adjMat[start][finish] = weight
    self.adjMat[finish][start] = weight

  # return an unvisited vertex adjacent to v
  def getAdjUnvisitedVertex (self, v):
    nVert = len (self.Vertices)
    for i in range (nVert):
      if (self.adjMat[v][i] > 0) and (not (self.Vertices[i]).wasVisited()):
        return i
    return -1

  # does a depth first search in a graph
  def dfs (self, v):
    # create a stack
    theStack = Stack()

    # mark the vertex as visited and push on the stack
    (self.Vertices[v]).visited = True
    print (self.Vertices[v])
    theStack.push (v)

    while (not theStack.isEmpty()):
      # get an adjacent unvisited vertex
      u = self.getAdjUnvisitedVertex (theStack.peek())
      if (u == -1):
        u = theStack.pop() 
      else:
        (self.Vertices[u]).visited = True
        print (self.Vertices[u])
        theStack.push(u)

    self.resetFlags()

  # does a breadth first search in a graph
  def bfs (self, v):
    # create a queue
    theQueue = Queue ()

    # mark the vertex as visited and enqueue
    (self.Vertices[v]).visited = True
    print (self.Vertices[v])
    theQueue.enqueue (v)

    while (not theQueue.isEmpty()):
      # get the vertex at the front
      v1 = theQueue.dequeue()
      # get an adjacent unvisited vertex
      v2 = self.getAdjUnvisitedVertex (v1)
      while (v2 != -1):
        (self.Vertices[v2]).visited = True
        print (self.Vertices[v2])
        theQueue.enqueue (v2)
        v2 = self.getAdjUnvisitedVertex (v1)

    self.resetFlags()

  # get index from vertex label
  def getIndex (self, label):
    for i in range(len(self.Vertices)):
      if self.Vertices[i].label == label:
        return i
    return None

  # get edge weight between two vertices
  # return -1 if edge does not exist
  def getEdgeWeight (self, fromVertexLabel, toVertexLabel):
    fromIndex = self.getIndex(fromVertexLabel)
    toIndex = self.getIndex(toVertexLabel)
    val = self.adjMat[fromIndex][toIndex]
    return -1 if val == 0 else val

  # get a list of neighbors that you can go to from a vertex
  # return empty list if there are none
  def getNeighbors (self, vertexLabel):
    neighbors = []
    row = self.adjMat[self.getIndex(vertexLabel)]
    for i in range(len(row)):
      if row[i] != 0:
        neighbors.append(self.Vertices[i])
    return neighbors

  # get a copy of the list of vertices
  def getVertices (self):
    return self.Vertices[:]

  # determine if the graph has a cycle
  def hasCycle (self):
    # create a stack
    theStack = Stack()
    hasCycle = False

    v = 0
    # mark the vertex as visited and push on the stack
    (self.Vertices[v]).visited = True
    theStack.push (v)

    while (not theStack.isEmpty()):
      # get an adjacent unvisited vertex
      u = self.getAdjUnvisitedVertex (theStack.peek())
      if u != -1:
        neighbors = self.getNeighbors(self.Vertices[u].label)
        neighborVertices = [self.getIndex(x.label) for x in neighbors]
        for n in neighborVertices:
          if n in theStack.stack:
            hasCycle = True
            break
      if (u == -1):
        u = theStack.pop() 
      else:
        (self.Vertices[u]).visited = True
        theStack.push(u)
    self.resetFlags()
    return hasCycle

  #reset the flags
  def resetFlags(self):
    for i in range (len (self.Vertices)):
      (self.Vertices[i]).visited = False

  # return a list of vertices after a topological sort
  def toposort (self):
    tempGraph = Graph()
    tempGraph.adjMat = [row[:] for row in self.adjMat]
    tempGraph.Vertices = self.Vertices[:]

    endPoint = set()
    noIncoming = []
    for v in tempGraph.Vertices:
      for x in tempGraph.getNeighbors(v.label):
        endPoint.add(x)
    noIncoming = list(set(tempGraph.Vertices) - endPoint)

    topological = []
    while noIncoming != []:
      vertex = noIncoming.pop()
      topological.append(vertex)
      for v in tempGraph.getNeighbors(vertex.label):
        tempGraph.deleteEdge(vertex.label,v.label)
        #if col of v is 0 then i has no other incoming edges
        col = []
        vIndex = tempGraph.getIndex(v.label)
        for row in tempGraph.adjMat:
          col.append(row[vIndex])
        if all(x == 0 for x in col):
          noIncoming.append(v)
    return topological

  # prints a list of edges for a minimum cost spanning tree
  # list is in the form [v1 - v2, v2 - v3, ..., vm - vn]
  def spanTree (self,startIndex):
    tree = []
    treeVertices = []

    currentVertex = self.Vertices[startIndex]
    currentVertex.visited = True
    treeVertices.append(currentVertex)
    neighborWeights =[]
    while len(treeVertices) != len(self.Vertices):
      neighbors = self.getNeighbors(currentVertex.label)
      neighborWeights += [(self.getEdgeWeight(currentVertex.label,x.label),x,currentVertex) for x in neighbors]
      minVal = (sys.maxsize,None,None)

      for x in neighborWeights:
        if x[1].visited == False and minVal[0] > x[0]:
          minVal = x
      if minVal == (sys.maxsize,None,None):
        currentVertex = treeVertices[treeVertices.index(currentVertex) - 1]
      else:
        neighborWeights.remove(minVal)
        currentVertex = minVal[1]
        oldVertex = minVal[2]

      currentVertex.visited = True
      if currentVertex not in treeVertices:
        treeVertices.append(currentVertex)
        tree.append(str(oldVertex) + ' - ' + str(currentVertex))

    self.resetFlags()
    return tree

  # determine shortest path from a single vertex
  # djikstras
  def shortestPath (self, fromVertexLabel,printing=True):
    index = self.getIndex(fromVertexLabel)
    distance = [None] * len(self.Vertices)
    distance[index] = 0

    while not all([x.visited for x in self.Vertices]):
      currentVertex = None
      minDist = sys.maxsize
      for i in range(len(distance)):
        if distance[i] != None and minDist > distance[i] and not self.Vertices[i].visited:
          minDist = distance[i]
          currentVertex = self.Vertices[i]
      if minDist == sys.maxsize:
        break
      currentVertex.visited = True

      currentIndex = self.getIndex(currentVertex.label)
      for n in self.getNeighbors(currentVertex.label):
        nIndex = self.getIndex(n.label)
        alt = distance[currentIndex] + self.getEdgeWeight(currentVertex.label,n.label)
        if distance[nIndex] == None or alt < distance[nIndex]:
          distance[nIndex] = alt

    self.resetFlags()

    if printing:
      for v,dist in zip(self.Vertices, distance):
        print(v,'-',dist if dist != None else 'unreachable')
    else:
      listy = []
      for v,dist in zip(self.Vertices, distance):
        listy.append(' '.join(map(str, (v,'-',dist if dist != None else 'unreachable'))))
      return listy

  # delete an edge from the adjacency matrix
  def deleteEdge (self, fromVertexLabel, toVertexLabel):
    fromIndex = self.getIndex(fromVertexLabel)
    toIndex = self.getIndex(toVertexLabel)
    self.adjMat[fromIndex][toIndex] = 0

  # Why have multiple returns when they lose points?
  # let's just raise exceptions!!!
  def checkToposort(self,topoSorted,fileNum):
    try:
      if len(topoSorted) != len(self.Vertices):
        raise Exception
      for index in range(1,len(topoSorted)):
        sliced = topoSorted[index:]
        for n in self.getNeighbors(topoSorted[index]):
          if n.label not in sliced:
            raise Exception
      return 7,''
    except:
      return 0,'failed topological sort on file %d (-7)'%fileNum



  def checkSpanTree(self,theirs,fileNum):
    try:
      weights = {1:11,3:7,4:39}
      weight = 0
      for edge in theirs:
        v1,v2 = tuple(edge.split(' - '))
        weight += self.getEdgeWeight(v1,v2)
      if weight != weights[fileNum]:
        raise Exception
      return 7,''
    except:
      return 0,'failed minimum span tree on file %d (-7)'%fileNum


def getPoints(fileNum,lines):
  # Create Graph object
  graph = Graph()

  # Open file for reading
  inFile = open ("./graph.txt", "r")

  # Read the vertices
  numVertices = int ((inFile.readline()).strip())

  for i in range (numVertices):
    city = (inFile.readline()).strip()
    graph.addVertex (city)

  # Read the edges
  numEdges = int ((inFile.readline()).strip())

  for i in range (numEdges):
    edge = (inFile.readline()).strip()
    edge = edge.split()
    start = int (edge[0])
    finish = int (edge[1])
    weight = int (edge[2])
    graph.addDirectedEdge (start, finish, weight)

  # Read the starting vertex for dfs, bfs, and shortest path
  startVertex = (inFile.readline()).strip()

  # Close file
  inFile.close()

  #grab the output
  linesCopy = lines[:]
  try:
    dfs = lines[:lines.index('')]
    lines = lines[lines.index('') + 1:]
    bfs = lines[:lines.index('')]
    lines = lines[lines.index('') + 1:]
    foo = lines[:lines.index('')]
    lines = lines[lines.index('') + 1:]
    djik = lines[:]
  except:
    print('parse error dumping their output')
    print('\n'.join(linesCopy))
    return 0,['error parsing output on file %d (-14)'%fileNum]

  comments = []
  if fileNum in [2,5]:
    points,c = graph.checkToposort(foo[1:],fileNum)
  else:
    points,c = graph.checkSpanTree(foo[1:],fileNum)
  if c != '':
    comments.append(c)

  djikCorrect = graph.shortestPath(startVertex,False)
  if djik[1:] != djikCorrect:
    p,c = 0,'failed on shortestPath on file %d (-7)'%fileNum
  else:
    p,c = 7,''
  if c != '':
    comments.append(c)

  if (point + p) == 0:
    print('dumping their output')
    print('\n'.join(linesCopy))

  return(points + p,comments)

main()
