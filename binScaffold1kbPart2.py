'''
Created on Aug 7, 2018

@author: nanda
python ~/aTools/utilities/binScaffold1kbPart2.py
'''

#####################################################################
constRequiredRangeValue=10000

#####################################################################
class Node :
    def __init__( self, data, clusterNo,strand ) :
        self.data = data
        self.cluster = clusterNo
        self.strand = strand
        self.anotherScaffoldList = []
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

#####################################################################

def getScaffoldMadeInsideCurrentNodeDifference(scaffoldNode):
    scaffold=scaffoldNode.split("\t")[0].split("__")
    endPositionValue=int(scaffold[2])
    startPositionValue=int(scaffold[1])
    return (endPositionValue-startPositionValue)+1

#####################################################################
def getNodeTotalDifference(currentNode):
    currentNodeTotalDifference=0
    if(len(currentNode.anotherScaffoldList)>0):
        for scaffold in currentNode.anotherScaffoldList:
            currentNodeTotalDifference+=getScaffoldMadeInsideCurrentNodeDifference(scaffold)
        

    currentNodeDetailsList=currentNode.data.split("__")
    currentNodeStartValue=int(currentNodeDetailsList[1])
    currentNodeEndValue=int(currentNodeDetailsList[2])
    currentNodeTotalDifference+=(currentNodeEndValue-currentNodeStartValue)+1
    
    return(currentNodeTotalDifference)


#####################################################################   
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
                currentNodeDetailsList[2]=str((int(currentNodeDetailsList[2])) + remainingToAdd)
                #Here first we are checking where the next node range difference is greater than the remainingToAdd value of currentNode. 
                #If it is equal, it means there is no remaining value in the nextnode range and we should discard the nextnode.
                if(nextNodeTotalDifference>remainingToAdd):
                    nextNodeDetailsList[1]=str((int(nextNodeDetailsList[1])) + remainingToAdd)
                    nextNode.data="__".join(nextNodeDetailsList)
                else:
                    currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.
                isNodeFinish=True
            else:
                currentNodeDetailsList[2]=nextNodeDetailsList[2]
                currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.
                
            currentNode.data="__".join(currentNodeDetailsList)
            
            return (True,isNodeFinish)
    return(isAnyFunctionProcessed,isNodeFinish)


#####################################################################
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
                    nextNode.data="__".join(nextNodeDetailsList)
                else:
                    currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.
                isNodeFinish=True
            else:
                currentNodeDetailsList[1]=nextNodeDetailsList[1]
                currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.

            currentNode.data="__".join(currentNodeDetailsList)
            
            return (True,isNodeFinish)
    return(isAnyFunctionProcessed,isNodeFinish)


#####################################################################   
#Region for different scaffold        
def doPlusAndPlusForDifferentScaffold(currentNode,isAnyFunctionProcessed,isNodeFinish):
    if(not isAnyFunctionProcessed):
        
        nextNode=currentNode.next
        currentNodeDetailsList=currentNode.data.split("__")
        nextNodeDetailsList=nextNode.data.split("__")
        if((currentNode.strand=="plus" and nextNode.strand=="plus") and (currentNodeDetailsList[0]!=nextNodeDetailsList[0])) or ((currentNode.strand=="plus" and nextNode.strand=="plus") and ((int(currentNodeDetailsList[2])+1)!=int(nextNodeDetailsList[1]))):
            
            currentNodeTotalDifference=getNodeTotalDifference(currentNode)
            remainingToAdd=constRequiredRangeValue-currentNodeTotalDifference
            nextNodeTotalDifference=getNodeTotalDifference(nextNode)
            if(nextNodeTotalDifference>=remainingToAdd):
                
                #Here first we are checking where the next node range difference is greater than the remainingToAdd value of currentNode. 
                #If it is equal, it means there is no remaining value in the nextnode range and we should discard the nextnode.
                if(nextNodeTotalDifference>remainingToAdd):
                    
                    addedNewLineListData=[nextNodeDetailsList[0],nextNodeDetailsList[1],str(int(nextNodeDetailsList[1]) + remainingToAdd-1)]
                    addedNewLineList="__".join(addedNewLineListData)
                    currentNode.anotherScaffoldList.append(addedNewLineList+"\t"+nextNode.cluster+"\t"+nextNode.strand)
                    nextNodeDetailsList[1]=str((int(nextNodeDetailsList[1])) + remainingToAdd)
                    nextNode.data="__".join(nextNodeDetailsList)
                else:
                    
                    currentNode.anotherScaffoldList.append(nextNode.data+"\t"+nextNode.cluster+"\t"+nextNode.strand)
                    currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.
                isNodeFinish=True
            else:
                
                currentNode.anotherScaffoldList.append(nextNode.data+"\t"+nextNode.cluster+"\t"+nextNode.strand)
                currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.

            return (True,isNodeFinish)
    return(isAnyFunctionProcessed,isNodeFinish)

#####################################################################

def doMinusAndMinusForDifferentScaffold(currentNode,isAnyFunctionProcessed,isNodeFinish):
    if(not isAnyFunctionProcessed):
        
        nextNode=currentNode.next
        currentNodeDetailsList=currentNode.data.split("__")
        nextNodeDetailsList=nextNode.data.split("__")
        if(((currentNode.strand=="minus" and nextNode.strand=="minus") and (currentNodeDetailsList[0]!=nextNodeDetailsList[0])) or  ((currentNode.strand=="minus" and nextNode.strand=="minus") and ((int(currentNodeDetailsList[1])-1)!=int(nextNodeDetailsList[2])))):
            currentNodeTotalDifference=getNodeTotalDifference(currentNode)
            remainingToSubtract=constRequiredRangeValue-currentNodeTotalDifference
            nextNodeTotalDifference=getNodeTotalDifference(nextNode)
            if(nextNodeTotalDifference>=remainingToSubtract):
                #Here first we are checking where the next node range difference is greater than the remainingToAdd value of currentNode. 
                #If it is equal, it means there is no remaining value in the nextnode range and we should discard the nextnode.
                if(nextNodeTotalDifference>remainingToSubtract):
                    addedNewLineListData=[nextNodeDetailsList[0],str(int(nextNodeDetailsList[2])- remainingToSubtract+1),nextNodeDetailsList[2]]
                    addedNewLineList="__".join(addedNewLineListData)
                    currentNode.anotherScaffoldList.append(addedNewLineList+"\t"+nextNode.cluster+"\t"+nextNode.strand)
                    nextNodeDetailsList[2]=str((int(nextNodeDetailsList[2])) - remainingToSubtract)
                    nextNode.data="__".join(nextNodeDetailsList)
                else:
                    currentNode.anotherScaffoldList.append(nextNode.data+"\t"+nextNode.cluster+"\t"+nextNode.strand)
                    currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.
                isNodeFinish=True
            else:
                currentNode.anotherScaffoldList.append(nextNode.data+"\t"+nextNode.cluster+"\t"+nextNode.strand)
                currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.
                       
            return (True,isNodeFinish)
    return(isAnyFunctionProcessed,isNodeFinish)
    
    
#####################################################################
def doPlusAndMinusForDifferentScaffold(currentNode,isAnyFunctionProcessed,isNodeFinish):
    if(not isAnyFunctionProcessed):
        
        nextNode=currentNode.next
        currentNodeDetailsList=currentNode.data.split("__")
        nextNodeDetailsList=nextNode.data.split("__")
        ##If it is plus minus considered as different scaffold, no need to check continuum
        #print("From",currentNode.strand,nextNode.strand)
        if(((currentNode.strand=="plus" and nextNode.strand=="minus") and (currentNodeDetailsList[0]!=nextNodeDetailsList[0])) or  ((currentNode.strand=="plus" and nextNode.strand=="minus") and ((int(currentNodeDetailsList[1])-1)!=int(nextNodeDetailsList[2])))):
            currentNodeTotalDifference=getNodeTotalDifference(currentNode)
            remainingToSubtract=constRequiredRangeValue-currentNodeTotalDifference
            nextNodeTotalDifference=getNodeTotalDifference(nextNode)
            if(nextNodeTotalDifference>=remainingToSubtract):
                #Here first we are checking where the next node range difference is greater than the remainingToAdd value of currentNode. 
                #If it is equal, it means there is no remaining value in the nextnode range and we should discard the nextnode.
                if(nextNodeTotalDifference>remainingToSubtract):
                    addedNewLineListData=[nextNodeDetailsList[0],str(int(nextNodeDetailsList[2])- remainingToSubtract+1),nextNodeDetailsList[2]]
                    addedNewLineList="__".join(addedNewLineListData)
                    currentNode.anotherScaffoldList.append(addedNewLineList+"\t"+nextNode.cluster+"\t"+nextNode.strand)
                    nextNodeDetailsList[2]=str((int(nextNodeDetailsList[2])) - remainingToSubtract)
                    nextNode.data="__".join(nextNodeDetailsList)
                else:
                    currentNode.anotherScaffoldList.append(nextNode.data+"\t"+nextNode.cluster+"\t"+nextNode.strand)
                    currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.
                isNodeFinish=True
            else:
                currentNode.anotherScaffoldList.append(nextNode.data+"\t"+nextNode.cluster+"\t"+nextNode.strand)

                currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.
            
            return (True,isNodeFinish)
    return(isAnyFunctionProcessed,isNodeFinish)


#####################################################################
def doMinusAndPlusForDifferentScaffold(currentNode,isAnyFunctionProcessed,isNodeFinish):
    if(not isAnyFunctionProcessed):
        
        nextNode=currentNode.next
        currentNodeDetailsList = currentNode.data.split("__")
        nextNodeDetailsList=nextNode.data.split("__")
        if(((currentNode.strand=="minus" and nextNode.strand=="plus") and (currentNodeDetailsList[0]!=nextNodeDetailsList[0])) or  ((currentNode.strand=="minus" and nextNode.strand=="plus") and ((int(currentNodeDetailsList[2])-1)!=int(nextNodeDetailsList[1])))):
            currentNodeTotalDifference=getNodeTotalDifference(currentNode)
            remainingToAdd=constRequiredRangeValue-currentNodeTotalDifference
            nextNodeTotalDifference=getNodeTotalDifference(nextNode)
            if(nextNodeTotalDifference>=remainingToAdd):
                #Here first we are checking where the next node range difference is greater than the remainingToAdd value of currentNode. 
                #If it is equal, it means there is no remaining value in the nextnode range and we should discard the nextnode.
                if(nextNodeTotalDifference>remainingToAdd):
                    addedNewLineListData=[nextNodeDetailsList[0],nextNodeDetailsList[1],str(int(nextNodeDetailsList[1])+ remainingToAdd-1)]
                    addedNewLineList="__".join(addedNewLineListData)
                    currentNode.anotherScaffoldList.append(addedNewLineList+"\t"+nextNode.cluster+"\t"+nextNode.strand)
                    nextNodeDetailsList[1]=str((int(nextNodeDetailsList[1])) + remainingToAdd)
                    nextNode.data="__".join(nextNodeDetailsList)
                else:
                    currentNode.anotherScaffoldList.append(nextNode.data+"\t"+nextNode.cluster+"\t"+nextNode.strand)
                    currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.
                isNodeFinish=True
            else:
                currentNode.anotherScaffoldList.append(nextNode.data+"\t"+nextNode.cluster+"\t"+nextNode.strand)
                currentNode.next=nextNode.next#it means there is no remaining value in the nextnode range and we should discard the nextnode.
            
            
            return (True,isNodeFinish)
    return(isAnyFunctionProcessed,isNodeFinish)
    
#####################################################################

def processScaffolds():
    with open("sortedMissingScaffolds") as SCPLIST, open("binnedScaffoldList", "w") as OUT:
    
        l = LinkedList()
        count=0
        for line in SCPLIST:
            line=line.rstrip("\n")
            v=line.split("\t")
            l.add( v[0], v[1], v[2],count)
            count+=1
        l.reverse()
        
        print("Linked List Ready, processing..")
        
        node = l.head
        while node != None:

            #Abhi
            #if(node.next != None):
            isNodeFinish=False
            
            #nextNode=node.next
            #while(!isNodeFinish and NextNode!=None):
            while( not isNodeFinish and node.next != None and node.cluster == node.next.cluster):
                isAnyFunctionProcessed=False
                currentNodeTotalDifference=getNodeTotalDifference(node)
                #print("currentNodeTotalDifference",currentNodeTotalDifference,node.data,node.strand,node.next.data,node.next.strand)
                if(currentNodeTotalDifference<constRequiredRangeValue):
                    #either of this function will get called
                    
                    #Same Scaffold
                    isAnyFunctionProcessed,isNodeFinish=doPlusAndPlusForSameScaffold(node,isAnyFunctionProcessed,isNodeFinish)
                    #isAnyFunctionProcessed,isNodeFinish=doMinusAndMinusForSameScaffold(node,isAnyFunctionProcessed,isNodeFinish)
                    
                    #Different Scaffold
                    isAnyFunctionProcessed,isNodeFinish=doPlusAndPlusForDifferentScaffold(node,isAnyFunctionProcessed,isNodeFinish)
                
                    #isAnyFunctionProcessed,isNodeFinish=doMinusAndMinusForDifferentScaffold(node,isAnyFunctionProcessed,isNodeFinish)
                    
                    #isAnyFunctionProcessed,isNodeFinish=doPlusAndMinusForDifferentScaffold(node,isAnyFunctionProcessed,isNodeFinish)
                    
                    #isAnyFunctionProcessed,isNodeFinish=doMinusAndPlusForDifferentScaffold(node,isAnyFunctionProcessed,isNodeFinish)
                    
                    
                    #1.Same Scaffold
                        #a. Plus
                        #b. Minus
                    #2.Different Scaffold
                        #a. Plus
                        #b. Minus
                        
                        
                if(currentNodeTotalDifference>constRequiredRangeValue):
                    
                else:
                    isNodeFinish=True
                    
            if(len(node.anotherScaffoldList)>0):
                OUT.write(node.data+"\t"+node.cluster+"\t"+node.strand+","+",".join(node.anotherScaffoldList)+"\n")#Todo: Value is not correct. It will change after completing while loop coding
            
            else:
                OUT.write(node.data+"\t"+node.cluster+"\t"+node.strand+"\n")
       
            node=node.next
            
            

#####################################################################

def main():
    processScaffolds()


#####################################################################
if __name__ == '__main__':
    main()


