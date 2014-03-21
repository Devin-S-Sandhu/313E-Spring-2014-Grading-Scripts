#looks for ghosts.tsv
# returns all ghosts with eids
def findGhosts():
  f = open('ghosts.tsv', 'r')
  ghosts = []
  skipFirst = True

  for line in f:
    if skipFirst:
      skipFirst = False
      continue
    line = line.split('\t')
    if line[0]:
      ghosts.append(line[0])

  f.close()
  return ghosts
#looks for tobust.tsv
#outputs busted.tsv
def bustGhosts(ghosts):
  f1 = open('tobust.tsv','r')
  f2 = open('busted.tsv','w')
  for line in f1:
    if line.split()[0] not in ghosts:
      f2.write(line)
  f1.close()
  f2.close()
  
def main():
  ghosts = findGhosts()
  bustGhosts(ghosts)
main()