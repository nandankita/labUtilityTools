'''
Created on Dec 4, 2018

@author: nanda
'''
class Node :
    def __init__( self, data, lengt,start,stop) :
        self.data = data
        self.lengt = lengt
        self.start = start
        self.stop = stop
        self.next = None
        self.prev = None
    
        
class LinkedList :
    def __init__( self ) :
        self.head = None
        self.tail = None
        self.size = 0        

    def add( self,  data, lengt,start,stop, count ) :
        node = Node( data,lengt,start,stop)
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
        
####################################################################

with open("missing-scaffoldsPositionFile", 'r') as orderFH, open("chr95Header-rearranged", 'r') as headerFH, open("rearrngedHeader", 'w') as binFH: 
    l = LinkedList()
    count=0
    for line in orderFH:
            line = line.rstrip('\n')
            v=line.split("\t")
            data=line
            lengt=int(v[1])
            ch=v[2].split("__")
            start=int(ch[1])
            stop=int(ch[2])
            l.add( data, lengt,start,stop, count )
            count+=1
    l.reverse()
    print("list created")
    listAdded=[]
    for line in headerFH:
            line = line.rstrip('\n')
            v=line.split("__")
            chSt=int(v[1])
            chEnd=int(v[2])
        
            node = l.head
            while node != None:
                c=0
                if(node.start<=chSt<=node.stop):
                    c+=node.lengt
                    
                    if(node.data not in listAdded):
                        binFH.write(node.data+"\t"+line+"\n")
                        listAdded.append(node.data)
                        while(c<10000 and node != None):
                            node = node.next
                            if(node != None):
                                listAdded.append(node.data)
                                binFH.write(node.data+"\t"+line+"\n")
                                c+=node.lengt
                    break
#                 else: 
#                     print("else",line,node.data)
                node = node.next

    
    
            