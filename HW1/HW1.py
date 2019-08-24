from Queue import PriorityQueue

def updateValidity(occupied,activityPointMatrix):
    lastAdded = occupied[-1]
    coordLA = lastAdded.split(',')
    lx,ly = int(coordLA[0]),int(coordLA[1])
    for i in range(size):
        for j in range(size):
            validityMatrix[i][j] = True
    for pos in occupied:
        rc=pos.split(',')
        r,c = int(rc[0]),int(rc[1])
        validityMatrix[r][c] = False
        for i in range(size):
            validityMatrix[r][i] = False
            validityMatrix[i][c] = False
        for i in range(size):
            for j in range(size):
                if abs(i-r) == abs(j-c):
                    validityMatrix[i][j]= False
                if activityPointMatrix[i][j] > activityPointMatrix[lx][ly]:
                    validityMatrix[i][j] = False


def CreateSearchTree(activityPointMatrix,policeoff,size):
    AP = PriorityQueue()
    maxAP = 0
    while not q.empty():
        t = q.get()
        if (t[0] * (-1)) > maxAP:
            maxAP = t[0] * (-1)
            AP.put((t[0] * (-1)))
        if t[2] < maxAP:
            if (t[0] * (-1)) == maxAP:
                AP.get()
                maxAP = (AP.get()) * (-1)
                AP.put(maxAP * (-1))
                continue
        else:
            squaresTaken = t[1].split('-')
            squaresTaken.remove('00')
            countOfSqauresTaken = len(squaresTaken)
            if(policeoff == countOfSqauresTaken):
                solutions.put(t)
                continue
            else:
                updateValidity(squaresTaken,activityPointMatrix)
                flag = 0
                for i in range(size):
                    for j in range(size):
                        if validityMatrix[i][j] == True:
                            flag = 1
                if flag == 0:
                    if (t[0]*(-1)) == maxAP:
                        AP.get()
                        maxAP = (AP.get()) * (-1)
                        AP.put(maxAP * (-1))
                    continue
                else:
                    for i in range(size):
                        for j in range(size):
                            if validityMatrix[i][j] == True:
                                activitypoint = (t[0]*(-1)) + activityPointMatrix[i][j]
                                maxpathcost = (t[0]*(-1)) + ((policeoff-countOfSqauresTaken) * activityPointMatrix[i][j])
                                if policeoff == (countOfSqauresTaken+1):
                                    solutions.put((activitypoint*(-1),t[1]+'-'+str(i)+','+str(j)))
                                else:
                                    q.put((activitypoint*(-1),t[1]+'-'+str(i)+','+str(j),maxpathcost))
    return

f=open("input.txt","r")
linecount = 0
a=[]
policeoff=0
scooter=0
q = PriorityQueue()
solutions = PriorityQueue()
size = 0
for l in f:
    a.append(l.rstrip())
for x in a:
    linecount += 1
    if (linecount == 1):
        size=int(x)
        activityPointMatrix = [[0] * size for i in range(size)]
        validityMatrix= [[0] * size for j in range(size)]
        #print size
    elif (linecount == 2):
        policeoff=int(x)
        #print policeoff
    elif (linecount == 3):
        scooter=int(x)
        #print scooter
    else :
        b=x.split(",")
        i=int(b[0])
        j=int(b[1])
        activityPointMatrix[i][j]+=1
#print activityPointMatrix

for i in range(size):
    for j in range(size):
        v = '00'+ '-' + str(i) + ',' + str(j)
        k = (-1) * activityPointMatrix[i][j]
        maxpathcost = activityPointMatrix[i][j] * policeoff
        q.put((k,v,maxpathcost))

CreateSearchTree(activityPointMatrix,policeoff,size)

goal = solutions.get()
#print goal[1]
#print goal[0]*(-1)
answer = str(goal[0]*(-1))
f=open("output.txt","w")
f.write(answer)