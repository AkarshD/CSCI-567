from Queue import PriorityQueue
from collections import OrderedDict
import copy
import time

class Applicant:

    def __init__(self):
        self.Gender=''
        self.Age=0
        self.Pets=''
        self.MCondition=''
        self.Car=''
        self.DL=''
        self.Totaldays=0
        self.week=[0]*7

class ReversePriorityQueue(PriorityQueue):

    def put(self, tup):
        newtup = tup[0] * -1, tup[1]
        PriorityQueue.put(self, newtup)

    def get(self):
        tup = PriorityQueue.get(self)
        newtup = tup[0] * -1, tup[1]
        return newtup

def addToDict(detail,Dict):
    applicantObj= Applicant()
    applicantID=''
    applicantID=detail[0:5]
    applicantObj.Gender=detail[5]
    applicantObj.Age=int(detail[6:9])
    applicantObj.Pets=detail[9]
    applicantObj.MCondition=detail[10]
    applicantObj.Car=detail[11]
    applicantObj.DL=detail[12]
    k=0
    for i in range(13,20):
        applicantObj.week[k]=int(detail[i])
        k+=1
        if(detail[i]=='1'):
            applicantObj.Totaldays+=1

    Dict[applicantID]=applicantObj
    pass


f=open("input.txt","r")
start = time.time()
shelterBeds=0
parkingSpace=0
LAHSAbyfar=0
SPLAbyfar=0
ChosenbyLAHSA=[]
ChosenbySPLA=[]
ApplicantsDict={}
ApplicantsAvail={}
AvailRAHSA={}
AvailSPLA={}
AvailBoth={}
totalApplicants=0

linecount = 0
a=[]

for l in f:
    a.append(l.rstrip())


for x in a:
    linecount += 1
    if (linecount == 1):
        shelterBeds=int(x)
    elif (linecount == 2):
        parkingSpace=int(x)
    elif (linecount == 3):
        LAHSAbyfar=int(x)
    elif (linecount>=4 and linecount<=(3+LAHSAbyfar)):
        ChosenbyLAHSA.append(x)
    elif (linecount == (4+LAHSAbyfar)):
        SPLAbyfar=int(x)
    elif (linecount>(4+LAHSAbyfar) and linecount <= (4+LAHSAbyfar+SPLAbyfar)):
        ChosenbySPLA.append(x)
    elif (linecount == 5+LAHSAbyfar+SPLAbyfar):
        totalApplicants=int(x)
    elif (linecount> (5+LAHSAbyfar+SPLAbyfar) and linecount <= (5+LAHSAbyfar+SPLAbyfar+totalApplicants)):
        addToDict(x,ApplicantsDict)

ApplicantsAvail.update(ApplicantsDict)
for i in ChosenbyLAHSA:
    ApplicantsAvail.pop(i)
for i in ChosenbySPLA:
    ApplicantsAvail.pop(i)

for k,v in ApplicantsAvail.iteritems():
    LAHSA = (v.Gender=='F' and v.Age>17 and v.Pets=='N' and v.Age<=100)
    SPLA = (v.Car=='Y' and v.DL=='Y' and v.MCondition=='N' and v.Age<=100)
    if (LAHSA):
        AvailRAHSA[k]=v
    if (SPLA):
        AvailSPLA[k]=v
    if (LAHSA and SPLA):
        AvailBoth[k]=v

PQ = ReversePriorityQueue()
PQ1 = ReversePriorityQueue()
PQ2= ReversePriorityQueue()
PQ3= ReversePriorityQueue()
SPLAspace=parkingSpace*7
LAHSAspace=shelterBeds*7
spaceMatrix ={}
bedMatrix ={}
parent='00000'
fixedLevel=0
ans=SPLAspace
listSPLA = OrderedDict()
listLAHSA = OrderedDict()


def maxLAHSA(k, listSPLA, listLAHSA, S, L, p, level):
    global ans
    global parent
    global fixedLevel

    if time.time() - start > 170:
        f = open("output.txt", "w")
        f.write(parent)
        exit()

    requestedWeek = ApplicantsDict[k].week
    for i in range(7):
        if requestedWeek[i] == 1 and bedMatrix[i] == 0:
            return

    for i in range(7):
        if requestedWeek[i] == 1:
            bedMatrix[i] -= 1

    L -= ApplicantsDict[k].Totaldays
    l1 = listSPLA.copy()
    l2 = listLAHSA.copy()
    l2.pop(k)
    if k in l1:
        l1.pop(k)

    if not l1 or level >fixedLevel or LAHSAspace==0 or SPLAspace==0:
        if S<=ans:
            if S==ans:
                if level==2:
                    if p<parent:
                        parent=p
                else:
                    if p in AvailBoth and parent in AvailBoth:
                        if (ApplicantsDict[p].Totaldays>ApplicantsDict[parent].Totaldays) :
                                parent=p
                        elif (ApplicantsDict[p].Totaldays==ApplicantsDict[parent].Totaldays):
                            if (p<parent):
                                parent=p
                    elif p in AvailBoth:
                        parent=p
            else:
                ans=S
                parent=p

        for i in range(7):
            if requestedWeek[i] == 1:
                bedMatrix[i] += 1
        return
    else:
        if S<=ans:
            if S==ans:
                if level==1:
                    if p<parent:
                        parent=p
                else:
                    if p in AvailBoth and parent in AvailBoth:
                        if (ApplicantsDict[p].Totaldays>ApplicantsDict[parent].Totaldays) :
                                parent=p
                        elif (ApplicantsDict[p].Totaldays==ApplicantsDict[parent].Totaldays):
                            if (p<parent):
                                parent=p
                    elif p in AvailBoth:
                        parent=p
            else:
                ans=S
                parent=p
        for m,n in l1.iteritems():
            maxSPLA(m,l1,l2,S,L,p,level+1)

    for i in range(7):
        if requestedWeek[i] == 1:
            bedMatrix[i] += 1

    pass


def maxSPLA(k, listSPLA, listLAHSA, S, L, p, level):

    global parent
    global ans
    global spaceMatrix
    global ApplicantsDict
    global fixedLevel

    if time.time() - start > 170:
        f = open("output.txt", "w")
        f.write(parent)
        exit()

    requestedWeek=ApplicantsDict[k].week

    for i in range(7):
        if requestedWeek[i]==1 and spaceMatrix[i]==0:
            return

    for i in range(7):
        if requestedWeek[i] == 1:
            spaceMatrix[i] -= 1

    S-=ApplicantsDict[k].Totaldays
    l1=listSPLA.copy()
    l2=listLAHSA.copy()
    l1.pop(k)
    if k in l2:
        l2.pop(k)
    if not l1 or level >fixedLevel or LAHSAspace==0 or SPLAspace==0:
        if S<=ans:
            if S==ans:
                if level==1:
                    if p<parent:
                        parent=p
                else:
                    if p in AvailBoth and parent in AvailBoth:
                        if (ApplicantsDict[p].Totaldays>ApplicantsDict[parent].Totaldays) :
                                parent=p
                        elif (ApplicantsDict[p].Totaldays==ApplicantsDict[parent].Totaldays):
                            if (p<parent):
                                parent=p
                    elif p in AvailBoth:
                        parent=p
            else:
                ans=S
                parent=p
        for i in range(7):
            if requestedWeek[i] == 1:
                spaceMatrix[i] += 1
        return
    else:
        if S<=ans:
            if S==ans:
                if level==1:
                    if p<parent:
                        parent=p
                else:
                    if p in AvailBoth and parent in AvailBoth:
                        if (ApplicantsDict[p].Totaldays>ApplicantsDict[parent].Totaldays) :
                                parent=p
                        elif (ApplicantsDict[p].Totaldays==ApplicantsDict[parent].Totaldays):
                            if (p<parent):
                                parent=p
                    elif p in AvailBoth:
                        parent=p
            else:
                ans=S
                parent=p
    if not l2:
        lev=level/2
        space=spaceMatrix.copy()
        for m,n in l1.iteritems():
            flag=False
            r=ApplicantsDict[m].week
            for i in range(7):
                if r[i] == 1 and space[i] ==0:
                    flag=True
                    break
            if flag:
                continue
            else:
                lev+=1
                for i in range(7):
                    if r[i]==1:
                        space[i]-=1
                S-=ApplicantsDict[m].Totaldays
                if lev>fixedLevel/2:
                    break

        if S<=ans:
            if S==ans:
                if level==1:
                    if p<parent:
                        parent=p
                else:
                    if p in AvailBoth and parent in AvailBoth:
                        if (ApplicantsDict[p].Totaldays>ApplicantsDict[parent].Totaldays) :
                                parent=p
                        elif (ApplicantsDict[p].Totaldays==ApplicantsDict[parent].Totaldays):
                            if (p<parent):
                                parent=p
                    elif p in AvailBoth:
                        parent=p
            else:
                ans=S
                parent=p

    else:
        for m,n in l2.iteritems():
            maxLAHSA(m,l1,l2,S,L,p,level+1)

    for i in range(7):
        if requestedWeek[i] == 1:
            spaceMatrix[i] += 1
    pass


if not bool(AvailBoth):
    if not AvailSPLA:
        parent='00000'
    else:
        for k,v in AvailSPLA.iteritems():
            PQ.put((v.Totaldays,k))
        i = PQ.get()
        parent = i[1]
    while not PQ:
        i=PQ.get()
        if ApplicantsDict[i[1]].Totaldays == ApplicantsDict[parent].Totaldays:
            if i[1] < parent:
                parent=i[1]
        else:
            break
    f = open("output.txt", "w")
    f.write(parent)

else:
    for k, v in AvailBoth.iteritems():
        PQ.put((v.Totaldays, k))
        PQ1.put((v.Totaldays, k))

    for k, v in AvailSPLA.iteritems():
        PQ2.put((v.Totaldays, k))

    for k, v in AvailRAHSA.iteritems():
        PQ3.put((v.Totaldays, k))

    while not PQ.empty():
        i = PQ.get()
        listSPLA[i[1]]= ApplicantsDict[i[1]]

    while not PQ2.empty():
        i = PQ2.get()
        listSPLA[i[1]] = ApplicantsDict[i[1]]

    while not PQ1.empty():
        i = PQ1.get()
        listLAHSA[i[1]] = ApplicantsDict[i[1]]

    while not PQ3.empty():
        i = PQ3.get()
        listLAHSA[i[1]] = ApplicantsDict[i[1]]

    for i in range(7):
        spaceMatrix[i]=parkingSpace
        bedMatrix[i]=shelterBeds

    for i in ChosenbyLAHSA:
        LAHSAspace -= ApplicantsDict[i].Totaldays
        req=ApplicantsDict[i].week
        for i in range(7):
            if req[i]==1:
                bedMatrix[i]-=1

    for i in ChosenbySPLA:
        req=ApplicantsDict[i].week
        SPLAspace -= ApplicantsDict[i].Totaldays
        for i in range(7):
            if req[i]==1:
                spaceMatrix[i]-=1

    if len(listSPLA) <=20:
        fixedLevel=10
    elif len(listSPLA) <=40:
        fixedLevel=6
    else:
        fixedLevel=4

    for k,v in listSPLA.iteritems():
        level=0
        maxSPLA(k,listSPLA,listLAHSA,SPLAspace,LAHSAspace,k,level+1)

    f = open("output.txt", "w")
    f.write(parent)