import re
from ortools.sat.python import cp_model
import time
import sys
start = time.time()



class Instance:
    def __init__(self):
        self.users = 0
        self.steps = 0
        self.constraints = 0
        self.authorisations = []
        self.binding=[]
        self.seperation=[]
        self.atmost=[]
        self.oneteam=[]
        self.u=[]
        self.s=[]
        self.new_s=[]
        self.flatten_s=[]
        self.new_u=[]
        self.flatten_u=[]
        self.binds=[]
        self.sep=[]
        self.new_binds=[]
        self.new_seperation=[]
        self.full_auth=[]
        self.atmostk=[]
        self.atmostk_new=[]
        self.flatten_atmost=[]
        self.oneteam_new=[]
        
        
        
        #reads from file input
    def write(self, filename):
        with open(filename, 'w') as f:
            f.write(f'#Steps: {self.steps}\n')
            f.write(f'#Users: {self.users}\n')
            f.write(f'#Constraints: {self.constraints}\n')
    
def read_file(filename):
    def read_attribute(name):
        line = f.readline()
        match = re.match(f'{name}:\\s*(\\d+)$', line)

        if match:
            return int(match.group(1))
        else:
            raise Exception("Could not parse line")

    instance = Instance()
    with open(filename) as f:
        instance.steps = read_attribute("#Steps")
        instance.users = read_attribute("#Users")
        instance.constraints = read_attribute("#Constraints")
        
        
        #reads the constraints
        for a in range(instance.constraints):
            line = f.readline()
            
            if line.startswith('Auth'):
                instance.authorisations.append(a)
                instance.u.append(line[15:20])

                for i in instance.u:
                    temp = re.findall(r'\d+', i)
                    i = list(map(int, temp))
                    if i not in instance.new_u:
                        instance.new_u.append(i)
                    for i in range(1,instance.users+1):
                        if i not in instance.new_u:
                            instance.flatten_u.append(i)
                        
                for subl in instance.new_u:
                    for item in subl:
                        if item not in instance.new_u:
                            instance.flatten_u.append(item)
                            instance.flatten_u = list(set(instance.flatten_u))                

                instance.s.append(line[20:])
                        
                for i in instance.s:
                    temp = re.findall(r'\d+', i)
                    i = list(map(int, temp))
                instance.new_s.append(i)
                for subl in instance.new_s:
                    for item in subl:
                        instance.flatten_s.append(item)
                        instance.flatten_s = list(set(instance.flatten_s))




            if line.startswith('Binding-of-duty'):
                instance.binding.append(a)
                instance.binds.append(line[16:])
                for i in instance.binds:
                    temp = re.findall(r'\d+', i)
                    i = list(map(int, temp))
                    if i not in instance.new_binds:
                        instance.new_binds.append(i)
                        


            if line.startswith('Separation'):
                instance.seperation.append(a)
                
                instance.sep.append(line[19:])
                
                for i in instance.sep:
                    temp = re.findall(r'\d+', i)
                    i = list(map(int, temp))
                    if i not in instance.new_seperation:
                        instance.new_seperation.append(i)
              
                    
              
                
            if line.startswith('At-most-k'):
                instance.atmost.append(a)
                instance.atmostk.append(line[11:])
                
                for i in instance.atmostk:
                    temp = re.findall(r'\d+', i)
                    i = list(map(int, temp))
                    if i not in instance.atmostk_new:
                        instance.atmostk_new.append(i)
                    
                
            if line.startswith('One-team'):
                instance.oneteam.append(a)
                instance.oneteam.append(line[10:])
                
               # for i in instance.oneteam:
                #    temp = re.findall(r'\d+', i)
                 #   i = list(map(int, temp))
                  #  if i not in instance.oneteam_new:
                   #     instance.oneteam_new.append(i)
                    
                
                
                #users not on list, fully authorised
        if len(instance.new_s)<instance.users:

            for i in range(1,instance.steps+1):
                if i not in instance.new_u:
                    instance.full_auth.append(i)
            instance.new_s.append(instance.full_auth)

        while True:
            l = f.readline()
            if l == "":
                break;
                
    return instance


def solve(instance):
    
    #List of steps flattened
    flat_steps = [item for sublist in instance.new_s for item in sublist]
    flat_steps = list(dict.fromkeys(flat_steps))
    if 0 in flat_steps:
        flat_steps.remove(0)

    #creates model
    model = cp_model.CpModel()


    #variables used( some not always used)
    users=instance.users
    steps=instance.steps
    cons=instance.constraints
    auth=instance.authorisations
    bind=instance.binding
    sep=instance.seperation   
    atmost=instance.atmost
    oneteam=instance.oneteam
    #u=instance.new_u
    #flat_u=instance.flatten_u
    s=sorted(flat_steps)
    binds=instance.new_binds
    sep=instance.new_seperation
    instance.new_s=sorted(instance.new_s)
    
    
    
    
    #This block shows details read from txt files
    print("Steps:",steps)
    print("Users:",users)
    print("Constraints:",cons)
    if len(auth)>0:
        print("Authorisations:",(len(auth)))
    
    if len(bind)>0:
        print("Bindings:",(len(bind)))
    if len(sep)>0:
        print("Seperations:",(len(sep)))
    if len(atmost)>0:
        print("At most: ",(len(atmost)))
    if len(oneteam)>0:
        print("OneTeam: ", (len(oneteam)))
    print("")
    
    #Uncommenting this next block shows additional details
    """
    print("Users Authorised:",flat_u)
    print("Steps users are authorised to cover:",s)
    print("User to steps:",instance.new_s)
    
    
    if len(binds)>0:
        print("Bindings:",binds)
    if len(sep)>0:
        print("Seperations:",sep)
    if len(atmost)>0:
         print("Atmosts:",instance.atmostk_new)
    if len(oneteam)>0:
        print("Oneteams:",instance.oneteam_new)
    """
    
    

        

    #BOD function
    def bindingCheck(l1, l2):
    # here l1 and l2 must be lists
        count = 0
        num_Bindings_Met=0
        for i in l1:
            for j in l2:

                for a in i:
                    if a in j:                        
                        count=count+1
                        if count>=len(i):
                            num_Bindings_Met=num_Bindings_Met+1
                            
                        if len(l1)<=num_Bindings_Met:
                            print("All bindings met")
                            return True
                        
    #SOD function
    def seperationCheck(l1,l2):
        non=[]
        seps_met=0
        for i in l1:
            for j in i:
                for k in l2:
                    if j  in k:
                        non.append(j)
            if len(non)>=2:
                    seps_met=seps_met+1
                        
        if seps_met>=len(l1):
            print("All seperations met")
            
            return True
        else:
            
            return False
            
        
    # Add the Constraints

    #Authorisations met or not
    if len(s)==steps:
        print("All authorisations met")
    else:
       print("Authorisations unable to be met")
       
       
    #Authorisations constraint   
    model.Add(len(s)==steps)
   
   #Binding of duty constraint
    if len(binds)!=0:
        model.Add(bindingCheck(binds,instance.new_s)==True)
    
    #Seperation of duty constraint
    if len(sep) !=0:
        model.Add(seperationCheck(sep,instance.new_s)==True)
    
    
    
    # Create a solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    end = time.time()

    if solver.StatusName(status)=="OPTIMAL":
        print("Sat")
        
        #Solution representation- Not working
        """
        print('User = %i' % solver.Value(instance.flatten_u[i]))
        print('Step = %i' % solver.Value(instance.steps))        
        """
    else:
        print("Unsat")
    
    print("Time taken:",end-start,"sec")



#Main that takes argument passed
if __name__ == '__main__':
    inst = read_file(sys.argv[1])
    solve(inst)