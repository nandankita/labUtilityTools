'''
Created on Aug 9, 2018

@author: nanda
'''
'''
Created on Aug 7, 2018

@author: nanda
python ~/aTools/utilities/binScaffold1kbPart2.py
'''
constRequiredRangeValue=1000


class Node :
    def __init__( self, data, clusterNo,strand ) :
        self.data = data
        self.cluster = clusterNo
        self.strand = strand
        self.next = None
        self.prev = None
        
class LinkedList :
    def __init__( self ) :
        self.head = None
        self.tail = None
        self.size = 0        

    def add( self, data, clusterNo, strand, count ) :
        node = Node( data, clusterNo, strand )
        self.size+=1
        if self.head == None :    
            self.head = node
            if(count==0):
                self.tail = node
        else :
            node.next = self.head
            node.next.prev = node                        
            self.head = node            
    
    def reverse(self):
        node=self.tail
        while node != None:
            p=node.prev
            n=node.next
            node.prev=n
            node.next=p
            node = p
        t=self.tail
        h=self.head
        self.head=t
        self.tail=h

def getNodeTotalDifference(currentNode):
    currentNodeDetailsList=currentNode.data.split("__")
    currentNodeStartValue=int(currentNodeDetailsList[1])
    currentNodeEndValue=int(currentNodeDetailsList[2])
    currentNodeTotalDifference=(currentNodeEndValue-currentNodeStartValue)+1
    return(currentNodeTotalDifference)
        
#Region for same scaffold       
def doPlusAndPlusForSameScaffold(currentNode,isAnyFunctionProcessed,isNodeFinish):
    if(not isAnyFunctionProcessed):
        nextNode=currentNode.next
        currentNodeDetailsList=currentNode.data.split("__")
        nextNodeDetailsList=nextNode.data.split("__")
        
        #Checking whether current node and next node are plus. Also, where currentnode and nextnode are in scaffold or not. Finally, 
        #checking whether in continuum in ascending
        if((currentNode.strand=="plus" and nextNode.strand=="plus") and (currentNodeDetailsList[0]==nextNodeDetailsList[0]) and ((int(currentNodeDetailsList[2])+1)==int(nextNodeDetailsList[1]))):
            currentNodeTotalDifference=getNodeTotalDifference(currentNode)
            remainingToAdd=constRequiredRangeValue-currentNodeTotalDifference
            nextNodeTotalDifference=getNodeTotalDifference(nextNode)
            if(nextNodeTotalDifference>=remainingToAdd):
                currentNodeDetailsList[2]=(int(currentNodeDetailsList[2])) + remainingToAdd
                #Here first we are checking where the next node range difference is greater than the remainingToAdd value of currentNode. 
                #If it is equal, it means there is no remaining value in the nextnode range and we should discard the nextnode.
                if(nextNodeTotalDifference>remainingToAdd):
                    nextNodeDetailsList[1]=str((int(nextNodeDetailsList[1])) + remainingToAdd)
                    currentNode.next.data="__".join(nextNodeDetailsList)
                else:
                    currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.
                isNodeFinish=True
            else:
                currentNodeDetailsList[2]=nextNodeDetailsList[2]
                currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.
            
            currentNode.data="__".join(currentNodeDetailsList)
            
        return (True,isNodeFinish)
    return(False,isNodeFinish)
    
def doPlusAndMinusForSameScaffold(currentNode,isAnyFunctionProcessed,isNodeFinish):
    if(not isAnyFunctionProcessed):
        nextNode=currentNode.next
        currentNodeDetailsList=currentNode.data.split("__")
        nextNodeDetailsList=nextNode.data.split("__")
        if((currentNode.strand=="plus" and nextNode.strand=="minus") and (currentNodeDetailsList[0]==nextNodeDetailsList[0]) and ((int(currentNodeDetailsList[2])+1)==int(nextNodeDetailsList[1]))):
            
        return True
        

def doMinusAndPlusForSameScaffold(currentNode,isAnyFunctionProcessed,isNodeFinish):
    if(not isAnyFunctionProcessed):
        nextNode=currentNode.next
        if(currentNode.strand=="minus" and nextNode.strand=="plus"):
        return True
    
def doMinusAndMinusForSameScaffold(currentNode,isAnyFunctionProcessed,isNodeFinish):
    if(not isAnyFunctionProcessed):
        nextNode=currentNode.next
        currentNodeDetailsList=currentNode.data.split("__")
        nextNodeDetailsList=nextNode.data.split("__")
        #Checking whether current node and next node are minus. Also, whether currentnode and nextnode are in scaffold or not. Finally, 
        #checking whether in continuum in descending
        if((currentNode.strand=="minus" and nextNode.strand=="minus") and (currentNodeDetailsList[0]==nextNodeDetailsList[0]) and ((int(currentNodeDetailsList[1])-1)==int(nextNodeDetailsList[2]))):
            currentNodeTotalDifference=getNodeTotalDifference(currentNode)
            remainingToSubtract=constRequiredRangeValue-currentNodeTotalDifference
            nextNodeTotalDifference=getNodeTotalDifference(nextNode)
            if(nextNodeTotalDifference>=remainingToSubtract):
                currentNodeDetailsList[1]=str((int(currentNodeDetailsList[1])) - remainingToSubtract)
                #Here first we are checking where the next node range difference is greater than the remainingToAdd value of currentNode. 
                #If it is equal, it means there is no remaining value in the nextnode range and we should discard the nextnode.
                if(nextNodeTotalDifference>remainingToSubtract):
                    nextNodeDetailsList[2]=str((int(nextNodeDetailsList[2])) - remainingToSubtract)
                    currentNode.next.data="__".join(nextNodeDetailsList)
                else:
                    currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.
                isNodeFinish=True
            else:
                currentNodeDetailsList[1]=nextNodeDetailsList[1]
                currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.
            
            currentNode.data="__".join(currentNodeDetailsList)
            
        return (True,isNodeFinish)
    return(False,isNodeFinish)
    
    
    
    
    
    
    
#Region for different scaffold        
def doPlusAndPlusForDifferentScaffold(currentNode,isAnyFunctionProcessed,isNodeFinish):
    if(not isAnyFunctionProcessed):
        nextNode=currentNode.next
    #     currentNodeDetailsList=currentNode.data.split("__")
    #     nextNodeDEtailsList=nextNode.data.split("__")
        if(currentNode.strand=="plus" and nextNode.strand=="plus"):
        return True
    
def doPlusAndMinusForDifferentScaffold(currentNode,isAnyFunctionProcessed,isNodeFinish):
    if(not isAnyFunctionProcessed):
        nextNode=currentNode.next
        if(currentNode.strand=="plus" and nextNode.strand=="minus"):
        return True

def doMinusAndPlusForDifferentScaffold(currentNode,isAnyFunctionProcessed,isNodeFinish):
    if(not isAnyFunctionProcessed):
        nextNode=currentNode.next
        if(currentNode.strand=="minus" and nextNode.strand=="plus"):
        return True
        
def doMinusAndMinusForDifferentScaffold(currentNode,isAnyFunctionProcessed,isNodeFinish):
    if(not isAnyFunctionProcessed):
        nextNode=currentNode.next
        if(currentNode.strand=="minus" and nextNode.strand=="minus"):
        return True    
    
    



with open("scaffold1kb") as SCPLIST, open("Finalscaffold1kb", "w") as OUT:

#with open("tmp") as SCPLIST, open("Finalscaffold1kb", "w") as OUT:
    l = LinkedList()
    count=0
    for line in SCPLIST:
        line=line.rstrip("\n")
        v=line.split("\t")
        l.add( v[0], v[1], v[2],count)
        count+=1
    l.reverse()
    
    print("Linked List Ready, processing1..")
    
    node = l.head
    while node != None:
        nLin=""
        #print(node.data, node.strand)
#         if(node.next == None):
#             OUT.write(node.data+"\t"+node.cluster+"\t"+node.strand+"\t"+nLin+"\n")
#             node = node.next
#             continue
        
        
        #Abhi
        isNodeFinish=False
        isAnyFunctionProcessed=False
        #nextNode=node.next
        #while(!isNodeFinish and NextNode!=None):
        while(!isNodeFinish and node.next != None):
            currentNodeTotalDifference=getCurrentNodeTotalDifference(node)
            if(currentNodeTotalDifference<constRequiredRangeValue):
                #either of this function will get called
                
                #Same Scaffold
                isAnyFunctionProcessed,isNodeFinish=doPlusAndPlusForSameScaffold(node,isAnyFunctionProcessed,isNodeFinish)
                isAnyFunctionProcessed,isNodeFinish=doPlusAndMinusForSameScaffold(node,isAnyFunctionProcessed,isNodeFinish)  
                isAnyFunctionProcessed,isNodeFinish=doMinusAndPlusForSameScaffold(node,isAnyFunctionProcessed,isNodeFinish) 
                isAnyFunctionProcessed,isNodeFinish=doMinusAndMinusForSameScaffold(node,isAnyFunctionProcessed,isNodeFinish)
 
                #Different Scaffold
                isAnyFunctionProcessed,isNodeFinish=doPlusAndPlusForDifferentScaffold(node,isAnyFunctionProcessed,isNodeFinish)
                isAnyFunctionProcessed,isNodeFinish=doPlusAndMinusForDifferentScaffold(node,isAnyFunctionProcessed,isNodeFinish)
                isAnyFunctionProcessed,isNodeFinish=doMinusAndPlusForDifferentScaffold(node,isAnyFunctionProcessed,isNodeFinish)
                isAnyFunctionProcessed,isNodeFinish=doMinusAndMinusForDifferentScaffold(node,isAnyFunctionProcessed,isNodeFinish)
                #1.Same Scaffold
                     #a. Plus
                     #b. Minus
                #2.Different Scaffold
                     #a. Plus
                     #b. Minus
            else:
                isNodeFinish=True
                
                
        OUT.write(node.data+"\t"+node.cluster+"\t"+node.strand+"\t"+nLin+"\n")#Todo: Value is not correct. It will change after completing while loop coding
        node=node.next
        
        
        
        
        
        
        
        
        
        
        
        
        scCurrent=node.data.split("__")
        diffr=int(scCurrent[2])-int(scCurrent[1]) +1
        
        nxt=node.next
        scNxt=nxt.data.split("__")
        more=0
        
        if(node.cluster==nxt.cluster):
            if(diffr!=1000):
                more=1000-diffr
                
                if (node.strand=="plus") and (scCurrent[0]==scNxt[0]):
                    scNxt[1]#startpositon
                    
                    if((scNxt[1]+more-1)<=scNxt[2]):
                        scNxt[1]+more-1 #endposition
                    else:
                        
                        scNxt[2] #endposition and call the next node for completing the current node. This process will recursive until it finish
                    
                
                
                if (nxt.strand=="plus") and (scCurrent[0]!=scNxt[0]):
                    
                    print(scCurrent,scNxt,more,diffr)
                    
                    scNxtstart = int(scNxt[1])+more
                    nLin=(scNxt[0]+"__"+scNxt[1]+"__"+str(scNxtstart)+"\t"+nxt.cluster+"\t"+nxt.strand)
                    
                    d=scNxt[0]+"__"+str(scNxtstart+1)+"__"+scNxt[2]
                    nxt.data=d
                    
                
                elif (nxt.strand=="minus") and (scCurrent[0]!=scNxt[0]):
                    
                    scNxtStart = int(scNxt[2])-more
                    nLin=(scNxt[0]+"__"+str(scNxtStart)+"__"+scNxt[2]+"\t"+nxt.cluster+"\t"+nxt.strand)
                    
                    d=scNxt[0]+"__"+scNxt[1]+"__"+str(scNxtStart-1)
                    
                    nxt.data=d
                
                elif (node.strand=="plus") and (scCurrent[0]==scNxt[0]):
                    currentEn=int(scCurrent[1])+999
                    cData=scCurrent[0]+"__"+scCurrent[1]+"__"+str(currentEn)
                    node.data=cData
                    if(currentEn+1<int(scNxt[2])):
                        d=scNxt[0]+"__"+str(currentEn+1)+"__"+scNxt[2]
                        nxt.data=d
                    
                
                elif (node.strand=="minus") and (scCurrent[0]==scNxt[0]):
                    currentSt=int(scCurrent[2])-999
                    cData=scCurrent[0]+"__"+str(currentSt)+"__"+scCurrent[2]
                    node.data=cData
                    if(currentSt-1<int(scNxt[1])):
                        d=scNxt[0]+"__"+scNxt[1]+"__"+str(currentSt-1)
                        nxt.data=d
                    
                
                else:
                    print("Error")
                
        OUT.write(node.data+"\t"+node.cluster+"\t"+node.strand+","+nLin+"\n")
        
        node = node.next

