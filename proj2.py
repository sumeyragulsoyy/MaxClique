#import sys 
import random
from operator import itemgetter
import matplotlib.pyplot as plt
class Node:
    def __init__(self,id,weight,neighbour):
        self.id=id
        self.weight=weight
        self.neighbour=neighbour
    def create(self,filename):   
        Nodelist=[]
        fname=filename      
        with open(fname) as f:
            content = f.readlines()
        content = [x.strip() for x in content] #remove \n 
        for m in range(len(content)):
            content[m]=content[m].replace(',','.') #replace , to .
        for i in range(len(content)):
            content[i] = [float(n) for n in content[i].split()]
        nodeNum=int(content[0][0]) #node number in Graph
        for j in range(2,1002): #2-1002 arası node -weight
           Nodelist.append(Node(content[j][0],content[j][1],[])) #node ,weight ,neihbour empty list initialized
        for s in range(1002,len(content)):
            for g in range(len(Nodelist)):
                if content[s][0] == Nodelist[g].id:                
                    if not (content[s][1] in Nodelist[g].neighbour): 
                        Nodelist[g].neighbour.append(content[s][1]) # X. node un neighbouruna Y eklendi
                if content[s][1]==Nodelist[g].id:
                    if not (content[s][0] in Nodelist[g].neighbour):
                        Nodelist[g].neighbour.append(content[s][0])
                        
        return Nodelist,nodeNum     #komşuları ,weight ve id ile graph geliyor
    
    
    def population(self,nodeNumber,populationsize):
        population = [[random.uniform(0,1) for x in range(nodeNumber)] for y in range(populationsize)] 
        for i in range(populationsize):
            for j in range(0,nodeNumber):
                if population[i][j]<0.5:
                   population[i][j]=0
                else:
                   population[i][j]=1

        return population  
   
    def repair(self,population,Nodelist): 
        #hiç birbiriyle bağlantısı olmayan nodelar gelebilir
        #sadece 1 tane bağlantısı olan gelebilir
        for i in range(len(population)):
            #string=population[i] #ilk string alındı
            boolean =False
            completeTest=[]
            while(not boolean): #check 
                for j in range(len(population[0])):
                    if population[i][j]==1: # existed node in the subset added to the completeTestlist
                        completeTest.append([j,Nodelist[j].weight,0]) #subset from graph nodes
                for m in range(len(completeTest)):
                    for n in range(m+1,len(completeTest)):
                        if completeTest[n][0] in Nodelist[completeTest[m][0]].neighbour:
                           completeTest[m][2] +=1
                           completeTest[n][2] +=1
                bool1=True #to check completeness with neighbour number 
                bool2=True #to check independent nodes
                for a in range(1,len(completeTest)):
                    if completeTest[a-1][2] != completeTest[a][2]:
                        bool1=False
                
                if bool1==True:  # string is complete go on next string
                    break
                
                for b in range(len(completeTest)):
                    if completeTest[b][2]!=0:
                        bool2=False
                if bool2==True: #create new string
                    population[i]=[random.uniform(0,1) for x in range(len(population[i]))]
                if bool2==False: #not full independent 
                    lessNeighbour=sorted(completeTest,key=itemgetter(2)) #sort according to neighbour num in subset
                    if lessNeighbour[0][2]!=lessNeighbour[1][2]:
                       index=lessNeighbour[0][0] # of id to remove complete list
                       population[i][index]=0 # flip the node in the string
                       del(completeTest[0]) # node is removed from subset
                    else:
                        sameNeighbourNum=lessNeighbour[0][2]
                        list=[]
                        for h in range(len(completeTest)):
                            if lessNeighbour[h][2]==sameNeighbourNum:
                                list.append([lessNeighbour[h][0],lessNeighbour[h][1]]) #get index and weight
                        willdeleted=sorted(list,key=itemgetter(1))
                        index=willdeleted[0][0]
                        population[i][index]=0 # flip the node in the string
                        index_del=0
                        for t in range(len(completeTest)):
                            if completeTest[t][0]==index:
                                index_del=t
                        del(completeTest[index_del])        
                    
        return population        
    
    def matingpool(self,population,Nodelist):
        sum=0
        globalsum=0
        fitness=[]
        for i in range(len(population)):
            for j in range(len(population[0])):
                if population[i][j]==1: 
                    sum += Nodelist[j].weight
            fitness.append(sum) #her stringin fitness değeri
            globalsum +=sum
            sum=0
        
        averagefitnessOfPopulation= globalsum/len(population)
            
        for j in range(len(fitness)): 
            fitness[j] =fitness[j]/globalsum #her fitness değer için olasılık değeri
        
        
        for x in range(1,len(fitness)):
            fitness[x]=fitness[x]+fitness[x-1]
        
        parentlist=[]
        for a in range(len(fitness)):  #roulet method for parent selection
            rand=random.uniform(0,1)
            for b in range(len(fitness)):
                if b==0:
                    if rand < fitness[b]:
                        parentlist.append(population[b])
                else:
                    if rand >= fitness[b-1] and rand < fitness[b]:
                        parentlist.append(population[b])
                     
        return parentlist,averagefitnessOfPopulation
    
    
    def crossover(self,parentlist,prob):
        random.shuffle(parentlist) #shuffle mating pool
        crossoverlist=[]
        for i in range (1,len(parentlist),2):
            rand=random.uniform(0,1)
            if rand >prob :
                l1=[]
                l2=[]
                newl1=[]
                newl2=[]
                randpoint= int(random.uniform(1,1000)) #random index to cross
                #for string 1
                l1.append(parentlist[i-1][0:randpoint])
                l1.append(parentlist[i][randpoint:])
                for x in l1:
                    for y in x:
                        newl1.append(y) #new l1
                #for string 2
                l2.append(parentlist[i][0:randpoint])
                l2.append(parentlist[i-1][randpoint:])
                for x1 in l2:
                    for y1 in x1:
                        newl2.append(y1) #newl2
                crossoverlist.append(newl1)
                crossoverlist.append(newl2)
            else:
                crossoverlist.append(parentlist[i-1])
                crossoverlist.append(parentlist[i])
            
        return crossoverlist    
         
         
    def mutation(self,crossoverlist,prob) :
        for i in range (len(crossoverlist)):
            rand=random.uniform(0,1) #probability for mutation  for every row -string
            if rand>prob:
                randindexes=[]
                for t in range(10):
                    randindexes.append(random.randint(0 ,1001)) #10 random index to flip for mutation
                for c in range(10): #to flip operation
                    if crossoverlist[i][randindexes[c]]== 0: #if 0
                        crossoverlist[i][randindexes[c]]=1
                    else: #if 1
                        crossoverlist[i][randindexes[c]]=0
                        
        return crossoverlist #this list after mutation operation
    
    def averageFitnessOfPopulation(self,RepairedPopulation,Nodelist):
        #generationFitnessValue=[] #every generation fitness value
        sum=0
        globalsum=0
        NodenumInSubset=0
        Details=[]
        for i in range(len(RepairedPopulation)):
            for j in range(len(RepairedPopulation[0])):
                if RepairedPopulation[i][j]==1: 
                    sum += Nodelist[j].weight
                    NodenumInSubset +=1
                globalsum +=sum
                Details.append([sum,NodenumInSubset]) #each string in final population of generation sum and Nodenum 
            sum=0
            NodenumInSubset=0
        averagefitnessOfPopulationFinal= globalsum/len(RepairedPopulation)
        #generationFitnessValue.append(averagefitnessOfPopulationFinal
        sortDetail=sorted(Details,key=itemgetter(0)) #sort according to sum
        maxClique=sortDetail[-1][0] #max clique
        maxNodeNum=[]
        for a1 in range(len(sortDetail)):
            if sortDetail[a1][0]==maxClique:
                maxNodeNum.append(sortDetail[a1][1]) #get nodeNumbers of maxClique
        maxNodeNumberofMaxSum=max(maxNodeNum)
                
        
        return averagefitnessOfPopulationFinal,maxClique,maxNodeNumberofMaxSum
    
    def main(self,filename,generationNumber,populationsize,crossoverProb,mutationProb):
        Nodelist,NodeNumber=Node.create(self,filename)
        populationPool=Node.population(self,NodeNumber,populationsize)
        RepairedPopulation=Node.repair(self,populationPool,Nodelist)
        generationFitnessValue=[] #every generation fitness value
        for x in range(generationNumber): #╚loop for generate number
            parentlist,averagefitnessOfPopulation=Node.matingpool(self,RepairedPopulation,Nodelist)
            crossoverList=Node.crossover(self,parentlist,crossoverProb)
            MutatedList=Node.mutation(self,crossoverList,mutationProb)
            OneGenerationEndPopulation=Node.repair(self,MutatedList,Nodelist)
            averagefitnessOfPopulationFinal,maxClique,maxNodeNumberofMaxSum=Node.averageFitnessOfPopulation(self,OneGenerationEndPopulation,Nodelist)
            generationFitnessValue.append(averagefitnessOfPopulationFinal) # to plot graph
            RepairedPopulation=OneGenerationEndPopulation
        
        generations=list(range(1,generationNumber+1))
        plt.plot(generations, generationFitnessValue, 'ro')
        print(maxClique) 
        print(maxNodeNumberofMaxSum)
     
rootNode=Node(-1,-1,[])        
Node.main(rootNode,'003.txt', 400 , 200, 0.3, 0.4) 
       
        
        
        
        
       
        
