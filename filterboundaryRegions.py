'''
Created on Jun 6, 2020

@author: nanda
'''
class Node :
    def __init__( self, boundaryChr,boundarySt,boundaryEnd):
        self.boundaryChr = boundaryChr
        self.boundarySt = boundarySt
        self.boundaryEnd = boundaryEnd
        
        self.next = None
        self.prev = None


class LinkedList :
    def __init__( self ) :
        self.head = None
        self.tail = None
        self.size = 0        

    def add(self, count,boundaryChr,boundarySt,boundaryEnd):
        node = Node(boundaryChr,boundarySt,boundaryEnd)
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
        
    def get(self, chVal):
        node=self.head
        filterList=[]
        while node != None:
            if(node.boundaryChr==chVal):
                filterList.append(node)
            node=node.next
        return(filterList)
        
with open("../domains", "r") as ORD1, open("Complete_Manually_selected_divergent.csv" , "r") as ORD2, open("boundary" , "w") as ORD3, open("non_boundary" , "w") as ORD4:
    count=0
    l = LinkedList()
    for line in ORD1:
        boundaryLine=line.rstrip("\n")
        values=boundaryLine.split("\t")
        l.add(count,values[0],int(values[1]),int(values[2]))
        count+=1
    l.reverse()
    
    for line in ORD2:
        readsLine = line.rstrip("\n")
        readsvalues = readsLine.split("\t")
        filteredboundaries=l.get(readsvalues[0])
        readst=int(readsvalues[1])
        readend=int(readsvalues[2])
        readRange=range(readst, readend)
        within=False
        for f in filteredboundaries:
            #print(f.boundarySt, f.boundaryEnd,readst,readend)
            boundaryRange=range(f.boundarySt, f.boundaryEnd+1)
            xs = set(readRange)
            inter=xs.intersection(boundaryRange)
            if(len(inter)!=0):
                within=True
#             if((readst in range(f.boundarySt, f.boundaryEnd+1)) or (readend in range(f.boundarySt, f.boundaryEnd+1))):
#                 within=True
#                 
        if(within==False):
            ORD4.write(readsLine+"\n")
            
        else:
            ORD3.write(readsLine+"\n")
        
        
        
        
        
        
        
        
        
        
        
