
#--- IMPORT DEPENDENCIES ------------------------------------------------------+

from __future__ import division
import random
import math
from random import randint
import sys



#--- VECTOR ---------------------------------------------------------------------+
class Vector:
    


    def __init__(self,content=0.0,moisture=0.0,hid=-1,binc=0.0):
        self.x=content
        self.y=moisture
        self.z=binc
        self.limit= sys.float_info.max
        self.H_id=hid

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getZ(self):
        return self.z

    def getH (self):
        return self.H_id

    def setX(self,content):
        self.x=content
    def setY(self,moisture):
        self.y=moisture

    def setZ(self,binc):
        self.z=binc

    def mag(self):
        math.sqrt( self.x*self.x+self.y*self.y )
    def limit(self,h=-1):
        if h==-1:
            m=mag()
            if(m>self.limit):
                ratio=m/limit
                self.x=sel.x/ratio
                self.y=self.y/ratio
        else:
            self.limit=h
            limit()
            
    def normalize(self):
        m=mag()
        if(m>0):
            self.x=self.x/m
            self.y=self.y/m
        
    def set(self,content,moisture,hid,binc):
        self.x=content
        self.y=moisture
        self.z=binc
        self.H_id=hid
    def add(self,Vector):
        self.x=self.x+Vector.getX()
        self.y=self.y+Vector.getY()
    def sub(self,Vector):
        self.x=self.x-Vector.getX()
        self.y=self.y-Vector.getY()
    def mul(self,s):
        self.x=self.x*s
        self.y=self.y*s
    def div(self,s):
        self.x=self.x/s
        self.y=self.y/s



    def clone(self):
        return Vector(self.x,self.y,self.H_id,self.z)


#--- Fitness Function ---------------------------------------------------------------------+
class Function:
    
    def __init__(self):
        g=0
    def HostId_V(self,Vec):
        return (Vec.getX()+Vec.getY())/(2*Vec.getZ())
    

#--- Particle ---------------------------------------------------------------------+
class Particle:

    def __init__(self,a,b,c,d):
        self.position = Vector()
        self.velocity = Vector()
        
        self.setRandomPosition(a,b,c,d)
        self.bestPosition = self.velocity.clone()
        self.bestEval = self.eval()

    def eval(self):
        f=Function()
        p=self.position
        return f.HostId_V(p)

    def setRandomPosition(self,a,b,c,d):
        self.position.set(a,b,c,d)


    def updatePersonalBest(self):
        eva = self.eval()
        if(eva<self.bestEval):
            self.bestPosition = self.position.clone()
            self.bestEval = eva

    def getVelocity (self):
        return self.velocity.clone()

    def getBestPosition(self):
        return self.bestPosition.clone()
    def getPosition (self):
        return self.position.clone()
    def getBestEval (self):
        return self.bestEval

    def updatePosition (self):
        self.position.add(self.velocity)

    def setVelocity (self, vel):
        self.velocity = vel.clone()


#--- Swarm ---------------------------------------------------------------------+
class Swarm:


    def __init__(self):
        self.infinity = float('inf')
        self.ninfinity = float('-inf')
        self.epochs=100
        
        self.bestPosition=Vector(self.infinity, self.infinity, self.ninfinity, self.infinity)
        self.bestEval=float('inf')
        self.DEFAULT_INERTIA = 1.5
        self.DEFAULT_SOCIAL = 1.5

        

    def initialize(self,ls,nv):
        particles=[]
        for i in range(0,len(ls)):
            x=ls[i]
            if(i in nv):
                k=0
                #print "Not Included"
            else:
                particle=Particle(x[0],x[1],x[2],x[3])
                particles.append(particle)
                self.updateGlobalBest(particle)
        return particles

    def updateGlobalBest (self,particle):
        if particle.getBestEval() < self.bestEval:
            self.bestPosition = particle.getBestPosition()
            self.bestEval = particle.getBestEval()
            
        
    def updateVelocity (self,particle):
        oldVelocity = particle.getVelocity()
        pBest = particle.getBestPosition()
        gBest = self.bestPosition.clone()
        pos = particle.getPosition()
        newVelocity = oldVelocity.clone()
        pBest.sub(pos)
        newVelocity.add(pBest)
        gBest.sub(pos)
        newVelocity.add(gBest)
        particle.setVelocity(newVelocity)


    def run(self,ls,nv):
        particles = self.initialize(ls,nv)
        oldEval = self.bestEval
        ct=len(ls)*.8
        #print int(ct)
        for i in range(0,int(ct)):
             if (self.bestEval < oldEval):
                 oldEval = self.bestEval

             for p in particles:
                 p.updatePersonalBest()
                 self.updateGlobalBest(p)
                    
             for p in particles:
                 self.updateVelocity(p)
                 p.updatePosition()
            

        
        return self.bestPosition.getH()




#--- MaxPSO ---------------------------------------------------------------------+
class MaxPSO:


    def __init__(self):
        po=0
        #print "PSO Started"

    def menu(self,ls,nv):
        swarm = Swarm()
        return int(swarm.run(ls,nv))





#--- Test ---------------------------------------------------------------------+

from random import randint

th=3



    # lst.append((containers[i][0]+containers[i][1])/2)
def psofit(containers,containers2,containers_bincount,bc,lt,lst):
    for i in range(0,lt):
        print str(containers[i][0])+" \t "+str(containers[i][1])+"\t"+str((containers[i][0]+containers[i][1])/2)+" - "+str(i)
      #  #print str(containers2[i][0])+" \t "+str(containers2[i][1])+"\t"+str((containers2[i][0]+containers2[i][1])/2)+" - "+str(i)
    containers_nv=[]
    containers_nvm=[]
    pso=MaxPSO()
    t=containers[pso.menu(containers,containers_nv)][2]


    pso=MaxPSO()
    t2=containers2[pso.menu(containers2,containers_nvm)][2]

    print t
    print t2



    stop=0
    vm1=0
    vc1=0
    while(stop==0):
        
        containers_nv = []

        for i in range(0,len(containers)):
            if containers[i][3]<=3:
                containers_nv.append(i)
                containers_nvm.append(i)
                
        pso=MaxPSO()
        t=containers[pso.menu(containers,containers_nv)][2]


        pso=MaxPSO()
        t2=containers2[pso.menu(containers2,containers_nvm)][2]
        containers_bincount[t]=containers_bincount[t]+1
        containers_nvm.append(t)
        if len(containers_nv)<len(containers_bincount)-1  and containers_bincount[t2]>3:
            containers_bincount[t2]=containers_bincount[t2]-1
            
        else:
            print "Allocating Bin - "+str(t)


        if(((containers[t][0]+containers[t][1])/2)/(containers[t][3])>=th):
            containers[t][0]=(containers[t][0]*containers[t][3])/containers_bincount[t]
            containers[t2][0]=(containers[t2][0]*containers[t2][3])/containers_bincount[t2]
            containers[t][1]=(containers[t][1]*containers[t][3])/containers_bincount[t]
            containers[t2][1]=(containers[t2][1]*containers[t2][3])/containers_bincount[t2]

            containers2[t][0]=100-containers[t][0]
            containers2[t2][0]=100-containers[t2][0]
            containers2[t][1]=100-containers[t][1]
            containers2[t2][1]=100-containers[t2][1]
            if(((containers[t][0]+containers[t][1])/2)/(containers[t][3])<th):
                containers_nv.append(t)
            if t2==t:
                print "No Additional Bin Required"
                break

        else :
            print "No Additional Bin Required"

            break




        

    for i in range(0,lt):
        print str(i)+"\t"+str((containers[i][0]+containers[i][1])/2)+"\t"+str(containers_bincount[i])
        lst[i][3]=containers[i][0]
        lst[i][4]=containers[i][1]
        lst[i][5]=containers_bincount[i]


    return lst


