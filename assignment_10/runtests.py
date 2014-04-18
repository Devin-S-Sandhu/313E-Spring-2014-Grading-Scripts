def insertFirst(ll, data):
    newLink = Link(data)
    newLink.next = getFirst(ll)
    putFirst(ll, newLink)

def makeLinkedList(items, addWorks):
    ll = LinkedList()
    for i in list(reversed(items)):
        if addWorks:
            ll.addFirst(i)
        else:
            insertFirst(ll, i)
    return ll

def getFirst(ll):
    try:
        return ll.first
    except:
        try:
            return ll.head
        except:
            return None

def putFirst(ll, link):
    try:
        ll.first = link
    except:
        try:
            ll.head = link
        except:
            pass

def diff(ll, ls):
    cur = getFirst(ll)
    for i in ls:
        if cur.data != i:
            return False
        cur = cur.next
    return cur != None

'''
grade out of 70 pts

test 1 (sample test):
{addInOrder, getNumLinks, find*, delete} = 1 pt (4 pts)
{copyList, reverseList, sortList, isSorted, isEmpty, mergeList, isEqual, removeDuplicates} = 2 pts (16 pts)

test 2:
{find*, delete} = 1 pt
{addInOrder, getNumLinks} = 4 pts
{copyList, reverseList, sortList, isSorted, isEmpty, mergeList, isEqual, removeDuplicates} = 5 pts (40 pts)
'''
def runTests(run, list1, list2, addWorks):
    if run == 1:
        grade = 20
    else:
        grade = 50

    comments = []

    # addInOrder
    try:
        ll = makeLinkedList(list1, addWorks)
        list1.append(13)
        list1.sort()
        ll.addInOrder(13)
        if diff(ll, list1):
            raise
    except:
        cmt = 'failed addInOrder'
        if run == 1:
            grade -= 1
            cmt += ' in test1 (-1)'
        else:
            grade -= 4
            cmt += ' in test2 (-4)'
        comments.append(cmt)

    # getNumLinks
    try:
        ll1 = makeLinkedList(list1, addWorks)
        ll2 = makeLinkedList(list2, addWorks)
        if ll1.getNumLinks() != len(list1) or ll2.getNumLinks() != len(list2):
            raise
    except:
        cmt = 'failed getNumLinks'
        if run == 1:
            grade -= 1
            cmt += ' in test1 (-1)'
        else:
            grade -= 4
            cmt += ' in test2 (-4)'
        comments.append(cmt)

    # find
    try:
        ll = makeLinkedList(list1, addWorks)
        if ll.findUnordered(13) == None:
            raise
        if ll.findUnordered(999) != None:
            raise
        if ll.findOrdered(13) == None:
            raise
        if ll.findOrdered(999) != None:
            raise
    except:
        cmt = 'failed find'
        if run == 1:
            grade -= 1
            cmt += ' in test1 (-1)'
        else:
            grade -= 1
            cmt += ' in test2 (-1)'
        comments.append(cmt)

    # delete
    try:
        ll = makeLinkedList(list1, addWorks)
        list1.remove(13)
        if ll.delete(13) == None or diff(ll, list1):
            raise
        if ll.delete(999) != None or diff(ll, list1):
            raise
    except:
        cmt = 'failed delete'
        if run == 1:
            grade -= 1
            cmt += ' in test1 (-1)'
        else:
            grade -= 1
            cmt += ' in test2 (-1)'
        comments.append(cmt)

    # copyList
    try:
        ll = makeLinkedList(list1, addWorks)
        ll2 = ll.copyList()
        if ll == ll2 or diff(ll2, list1):
            raise
    except:
        cmt = 'failed copyList'
        if run == 1:
            grade -= 2
            cmt += ' in test1 (-2)'
        else:
            grade -= 5
            cmt += ' in test2 (-5)'
        comments.append(cmt)

    # reverseList
    try:
        ll = makeLinkedList(list1, addWorks)
        ll2 = ll.reverseList()
        if ll == ll2 or diff(ll2, list(reversed(list1))):
            raise
    except:
        cmt = 'failed reverseList'
        if run == 1:
            grade -= 2
            cmt += ' in test1 (-2)'
        else:
            grade -= 5
            cmt += ' in test2 (-5)'
        comments.append(cmt)

    # sortList
    try:
        ll = makeLinkedList(list2, addWorks)
        ll2 = ll.sortList()
        if ll == ll2 or diff(ll2, list(sorted(list2))):
            raise
    except:
        cmt = 'failed sortList'
        if run == 1:
            grade -= 2
            cmt += ' in test1 (-2)'
        else:
            grade -= 5
            cmt += ' in test2 (-5)'
        comments.append(cmt)

    # isSorted
    try:
        ll = makeLinkedList(list1, addWorks)
        if not ll.isSorted():
            raise
        ll2 = makeLinkedList(list2, addWorks)
        if ll2.isSorted():
            raise
    except:
        cmt = 'failed isSorted'
        if run == 1:
            grade -= 2
            cmt += ' in test1 (-2)'
        else:
            grade -= 5
            cmt += ' in test2 (-5)'
        comments.append(cmt)

    # isEmpty
    try:
        ll = makeLinkedList(list1, addWorks)
        if ll.isEmpty():
            raise
        ll2 = makeLinkedList(list2, addWorks)
        if ll2.isEmpty():
            raise
        ll3 = LinkedList()
        if not ll3.isEmpty():
            raise
    except:
        cmt = 'failed isEmpty'
        if run == 1:
            grade -= 2
            cmt += ' in test1 (-2)'
        else:
            grade -= 5
            cmt += ' in test2 (-5)'
        comments.append(cmt)

    # mergeList
    try:
        ll = makeLinkedList(list1, addWorks)
        ll2 = makeLinkedList(list2, addWorks)
        ll3 = ll.mergeList(ll2)
        merged = []
        for i in list1:
            merged.append(i)
        for i in list2:
            merged.append(i)
        merged.sort()
        if ll == ll3 or ll2 == ll3 or diff(ll3, merged):
            raise
    except:
        cmt = 'failed mergeList'
        if run == 1:
            grade -= 2
            cmt += ' in test1 (-2)'
        else:
            grade -= 5
            cmt += ' in test2 (-5)'
        comments.append(cmt)

    # isEqual
    try:
        ll = makeLinkedList(list1, addWorks)
        ll2 = makeLinkedList(list2, addWorks)
        ll3 = makeLinkedList(list1, addWorks)
        if ll.isEqual(ll2):
            raise
        if not ll.isEqual(ll3):
            raise
    except:
        cmt = 'failed isEqual'
        if run == 1:
            grade -= 2
            cmt += ' in test1 (-2)'
        else:
            grade -= 5
            cmt += ' in test2 (-5)'
        comments.append(cmt)

    # removeDuplicates
    try:
        list1.extend([13, 14, 13, 13, 13, 14, 17, 17, 17, 18, 2, 2, 5, 5])
        list1.sort()
        ll = makeLinkedList(list1, addWorks)
        noDupl = list(set(list1))
        noDupl.sort()
        ll2 = ll.removeDuplicates()
        if ll == ll2 or diff(ll2, noDupl):
            raise
    except:
        cmt = 'failed removeDuplicates'
        if run == 1:
            grade -= 2
            cmt += ' in test1 (-2)'
        else:
            grade -= 5
            cmt += ' in test2 (-5)'
        comments.append(cmt)

    return grade, comments

print ('\n=TestLinkedList=')

addWorks = True

try:
    test = [1, 3, 5, 7, 9]
    testll = LinkedList()

    for t in test:
        testll.addFirst(t)

    cur = getFirst(testll)
    for t in test:
        if cur.data != t:
            addWorks = False
            break
        cur = cur.next
except:
    addWorks = False

l1 = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
l2 = [19, 15, 13, 11, 17]
grade, comments = runTests(1, l1, l2, addWorks)
l1 = [12, 23, 7, 34, 80, 20, 40, 123, 53, 2, 12, 15, 16, 12, 19, 52, 61, 77, 52]
l2 = [32, 62, 32, 52, 16, 73, 84, 35]
gr, cmt = runTests(2, l1, l2, addWorks)
grade += gr
comments.extend(cmt)

print ('g::' + str(grade))
for l in comments:
    print ('c::' + l)
