from commonFunctions import *
import re
import fileinput

def EQtoSC(line,new):
    if "ObjectIntersectionOf" in line[1]: x = intersectionSplit(line,new)
    else: x = "SubClassOf({} {})\nSubClassOf({} {})".format(line[0],line[1],line[1],line[0])
    #print(x)
    return x

'''
B ≡ A ⊓ ∃S.D

B ≡ A ⊓ X2
X2 ≡ ∃S.D

B ⊑ A
B ⊑ X2
A ⊓ X2 ⊑ B
X2 ⊑ ∃S.D
∃S.D ⊑ X2


A ≡ B ⊓ C ⊓ ∃S.D

A ≡ B ⊓ X1
X1 ≡ C ⊓ X2
X2 ≡ ∃S.D

A ⊑ B
A ⊑ X1
B ⊓ X1 ⊑ A
X1 ⊑ C
X1 ⊑ X2
C ⊓ X2 ⊑ X1
X2 ⊑ ∃S.D
∃S.D ⊑ X2
'''
def intersectionSplit(line,new):
    newLine = [line[0]]
    newLine.extend(line[1][21:-1].split(" ",1))
    x = ""
    if canEasySplit(line[1]):
                
        while separable(newLine[-1]):
            if not "ObjectIntersectionOf" in newLine[-1]:
                rem = newLine[-1]
                newLine.extend(newLine[-1].split(" ",1))
                newLine.remove(rem)
            else:
                pass
        for C in newLine:
            if C in new.keys(): pass
            else: new[C] = "sep:X{:05d}".format(len(new)+1)
        if len(newLine) == 3:
            '''
            B ⊑ A
            B ⊑ X
            A ⊓ X ⊑ B
            X ⊑ ∃S.D
            ∃S.D ⊑ X
            '''
            if isExistential(newLine[-1]):
                x = "SubClassOf({} {})\nSubClassOf({} {})\nSubClassOf(ObjectIntersectionOf({} {}) {})\nSubClassOf({} {})\nSubClassOf({} {})\n".format(newLine[0],newLine[1],newLine[0],new[newLine[-1]],newLine[1],new[newLine[-1]],newLine[0],new[newLine[-1]],newLine[-1],newLine[-1],new[newLine[-1]])
            else:
                raise
        else:
            '''
            A ≡ B ⊓ C ⊓ ∃S.D
            
            A ⊑ B
            A ⊑ X1
            B ⊓ X1 ⊑ A
            X1 ⊑ C
            X1 ⊑ X2
            C ⊓ X2 ⊑ X1
            X2 ⊑ ∃S.D
            ∃S.D ⊑ X2
            '''
            X1 = "ObjectIntersectionOf({} {})".format(newLine[2],newLine[3])
            X1r = "ObjectIntersectionOf({} {})".format(newLine[3],newLine[2])
            
            if X1 in new.keys() or X1r in new.keys(): pass
            else: new[X1] = "sep:X{:05d}".format(len(new)+1)
            
            X2 = newLine[3]
            concept = True
            if isExistential(X2): 
                concept = False
                if X2 in new.keys(): pass
                else: new[X2] = "sep:X{:05d}".format(len(new)+1)
                '''
                X2 ⊑ ∃S.D
                ∃S.D ⊑ X2
                '''
                x = x + "SubClassOf({} {})\n".format(new[X2],newLine[3])
                x = x + "SubClassOf({} {})\n".format(newLine[3],new[X2])                
                
            #
            '''
            A ⊑ B
            A ⊑ X1
            '''
            x = x + "SubClassOf({} {})\n".format(newLine[0],newLine[1])
            x = x + "SubClassOf({} {})\n".format(newLine[0],new[X1])
            '''
            B ⊓ X1 ⊑ A
            C ⊓ X2 ⊑ X1
            '''
            x = x + "SubClassOf(ObjectIntersectionOf({} {}) {})\n".format(newLine[1],new[X1],newLine[0])
            x = x + "SubClassOf(ObjectIntersectionOf({} {}) {})\n".format(newLine[2],X2 if concept else new[X2],new[X1])            
            '''
            X1 ⊑ C
            X1 ⊑ X2
            '''
            x = x + "SubClassOf({} {})\n".format(new[X1],newLine[2])
            x = x + "SubClassOf({} {})\n".format(new[X1],X2 if concept else new[X2])
            #print(newLine)#print(x,"\n")
    else:
        if newLine[2][0] != 'O':
            '''
            A ≡ B ⊓ C ⊓ ∃R.D ⊓ ∃S.E
            
            A ⊑ B
            A ⊑ X1
            B ⊓ X1 ⊑ A
            X1 ⊑ C
            X1 ⊑ X2
            C ⊓ X2 ⊑ X1
            X2 ⊑ X3
            X2 ⊑ X4
            X3 ⊓ X4 ⊑ X2
            X3 ⊑ ∃R.D
            ∃R.D ⊑ X3
            X4 ⊑ ∃S.E
            ∃S.E ⊑ X4
            '''
            y = newLine[2].split(" ",1)
            z = y[1].split(" ",2)[-1]
            y[1] = " ".join(y[1].split(" ",2)[:2])
            y.append(z)
            del newLine[2]
            newLine.extend(y)
     
            #print(newLine)       
            X3 = newLine[3]
            if X3 in new.keys(): pass
            else: new[X3] = "sep:X{:05d}".format(len(new)+1)
            
            X4 = newLine[4]
            if X4 in new.keys(): pass
            else: new[X4] = "sep:X{:05d}".format(len(new)+1)
            
            X2 = "ObjectIntersectionOf({} {})".format(newLine[3],newLine[4])
            X2r = "ObjectIntersectionOf({} {})".format(newLine[4],newLine[3])
            
            if X2 in new.keys() or X2r in new.keys(): pass
            else: new[X2] = "sep:X{:05d}".format(len(new)+1)

            X1 = "ObjectIntersectionOf({} {})".format(newLine[2],X2)
            X12 = "ObjectIntersectionOf({} {})".format(newLine[2],X2r)
            X1r = "ObjectIntersectionOf({} {})".format(X2,newLine[2])
            X12r = "ObjectIntersectionOf({} {})".format(X2r,newLine[2])
            
            if X1 in new.keys() or X1r in new.keys() or X12 in new.keys() or X12r in new.keys(): pass
            else: new[X1] = "sep:X{:05d}".format(len(new)+1)            
            
            '''
            A ⊑ B
            A ⊑ X1
            X1 ⊑ C
            X1 ⊑ X2
            X2 ⊑ X3
            X2 ⊑ X4
            '''
            x = x + "SubClassOf({} {})\n".format(newLine[0],newLine[1])
            x = x + "SubClassOf({} {})\n".format(newLine[0],new[X1])
            x = x + "SubClassOf({} {})\n".format(new[X1],newLine[2])
            x = x + "SubClassOf({} {})\n".format(new[X1],new[X2])
            x = x + "SubClassOf({} {})\n".format(new[X2],new[X3])
            x = x + "SubClassOf({} {})\n".format(new[X2],new[X4])            
            '''
            B ⊓ X1 ⊑ A
            C ⊓ X2 ⊑ X1
            X3 ⊓ X4 ⊑ X2
            '''
            x = x + "SubClassOf(ObjectIntersectionOf({} {}) {})\n".format(newLine[1],new[X1],newLine[0])
            x = x + "SubClassOf(ObjectIntersectionOf({} {}) {})\n".format(newLine[2],new[X2],new[X1])
            x = x + "SubClassOf(ObjectIntersectionOf({} {}) {})\n".format(new[X3],new[X4],new[X2])
            '''
            X3 ⊑ ∃R.D
            ∃R.D ⊑ X3
            '''
            x = x + "SubClassOf({} {})\n".format(new[X3],newLine[3])
            x = x + "SubClassOf({} {})\n".format(newLine[3],new[X3])  
            '''
            X4 ⊑ ∃S.E
            ∃S.E ⊑ X4
            '''
            x = x + "SubClassOf({} {})\n".format(new[X4],newLine[4])
            x = x + "SubClassOf({} {})\n".format(newLine[4],new[X4])
            
            #print(newLine)
        else:
            
            while stillSplittable(newLine[-1]):
                #print(newLine)
                y = newLine[-1][21:-1].split(" ",1)
                #print(y)
                newLine.pop(-1)
                newLine.append(y[0])
                newLine.append(y[1])
                #            
            
            if newLine[-1].count(' ') > 1:
                y = newLine[-1][21:-1].split(" ",1)
                newLine.pop(-1)
                newLine.append(y[0])
                newLine.append(y[1])
                
            #print(newLine)
            
            last = newLine[-1]
            if last in new.keys(): pass
            else: new[last] = "sep:X{:05d}".format(len(new)+1)
            
            '''
            last ⊑ ∃R.C
            ∃R.C ⊑ last
            '''
            x = x + "SubClassOf({} {})\n".format(new[last],newLine[-1])
            x = x + "SubClassOf({} {})\n".format(newLine[-1],new[last])
            
            newLine[-1] = new[last]
            
            #print(newLine)
            
            while len(newLine) > 2:
                if len(newLine[-2]) > 7:
                    Y = "ObjectIntersectionOf({} {})".format(newLine[-2],newLine[-1])
                    Yr = "ObjectIntersectionOf({} {})".format(newLine[-1],newLine[-2])
                    
                    if Y in new.keys() or Yr in new.keys(): pass
                    else: 
                        new[Y] = "sep:X{:05d}".format(len(new)+1) 
                        '''
                        Y ⊑ B
                        Y ⊑ X
                        B ⊓ X ⊑ Y
                        '''
                        x = x + "SubClassOf({} {})\n".format(new[Y],newLine[-1])
                        x = x + "SubClassOf({} {})\n".format(new[Y],newLine[-2])
                        x = x + "SubClassOf(ObjectIntersectionOf({} {}) {})\n".format(newLine[-2],newLine[-1],new[Y])
                    
                    newLine.pop(-1)
                    newLine[-1] = new[Y]
                    
                    #print(newLine)
                else:
                    last = "ObjectSomeValuesFrom({} {})".format(newLine[-2],newLine[-1])
                    if last in new.keys(): pass
                    else: 
                        new[last] = "sep:X{:05d}".format(len(new)+1)
                        '''
                        last ⊑ ∃R.C
                        ∃R.C ⊑ last
                        '''
                        x = x + "SubClassOf({} {})\n".format(new[last],last)
                        x = x + "SubClassOf({} {})\n".format(last,new[last])
                    #print(x)
                    newLine.pop(-1)
                    newLine[-1] = new[last]
                    
                    #print(newLine)
            
            x = x + "SubClassOf({} {})\nSubClassOf({} {})\n".format(newLine[0],newLine[1],newLine[1],newLine[0])#"EquivalentClasses({} {})".format(line[0],line[1])
    
    return x


def stillSplittable(string):
    #print(string)
    pattern1 = re.compile("^.*(ObjectIntersectionOf)+.*$")
    pattern2 = re.compile("^.*(ObjectSomeValuesFrom){2,}.*$")
    val = pattern1.match(string) != None or pattern2.match(string) != None   
    return val

def isExistential(string):
    return "ObjectSomeValuesFrom" in string

def separable(string):
    pattern = re.compile("^[a-z]{3}:[A-Z]{1}[0-9]{5}\s")
    return pattern.match(string) != None

def canEasySplit(line):
    if not "ObjectSomeValuesFrom" in line: return True
    if line.count("ObjectSomeValuesFrom") == 1:
        return line.rfind("ObjectSomeValuesFrom") > line.rfind("ObjectIntersectionOf")
    #print(line)
    return False

def normalizeFS(inf,outf):
    pattern = re.compile("EquivalentClasses+")
    
    file = open(inf,"r")
    file2 = open(outf,"w")
    
    new = {}
    
    for line in file:
        if pattern.match(line) != None: file2.write(EQtoSC(line[18:-2].split(" ",1),new))
        else: file2.write(line)
    
    file.close()
    file2.close()
    
    newData = ["Declaration(Class(sep:X{:05d}))\n".format(x) for x in range(1,len(new)+1)]
    
    file3 = open(outf,"r")    
    data = file3.readlines()
    file3.close()
    
    for line in fileinput.FileInput(outf,inplace=1):
        if "Declaration(Class(sep:fauxP19550))" in line:
            line = line.replace(line,line+"".join(newData))
        print (line,end='')
    
    return outf

def fsOWLReader(filename):
    file = open(filename,'r')
    
    line = file.readline()
    while "Declaration" not in line:
        line = file.readline()
    
    classes = 0
    classDict = {}
    labelDict = {}
    roles = 0
    roleDict = {}
    CType1=[]
    CType2=[]
    CType3=[]
    CType4=[]
    roleSubs=[]
    roleChains=[]
    
    
    while "Declaration" in line:
        if "Class" in line: 
            classes = classes + 1
            classDict[line[18:-3]] = classes
        elif 'Object' in line: 
            roles = roles + 1
            roleDict[line[27:-3]] = roles
        line = file.readline()
        
    
    while line:
        if line[0] == '#': pass
        elif 'AnnotationAssertion(rdfs:label' in line:
            line = line[31:-2].split(' ',1)
            labelDict[line[0]] = line[1][1:-1]
        elif 'SubObjectPropertyOf(' in line:
            #print(line)
            line = line[20:-2]            
            if 'ObjectPropertyChain(' in line:
                first = (" ".join(line.split(" ",2)[:2]))[20:-1].split()
                last = line.split(" ",2)[2]
                rs = RoleStatement(len(roleSubs),True,RoleChain(0,Role(roleDict[first[0]],[0,1]),Role(roleDict[first[1]],[1,2])),Role(roleDict[last],[0,2]))
                rs.complete('⊑')
                roleChains.append(rs)
            else: 
                line = line.split()
                #print(line)
                rs = RoleStatement(len(roleChains),True,Role(roleDict[line[0]],[0,1]),Role(roleDict[line[1]],[0,1]))
                rs.complete('⊑')
                roleSubs.append(rs)
        elif 'TransitiveObjectProperty(' in line:
            '''SubObjectPropertyOf( ObjectPropertyChain( OPE OPE ) OPE )'''
            role = line[25:-2]
            rs = RoleStatement(len(roleChains),True,RoleChain(0,Role(roleDict[role],[0,1]),Role(roleDict[role],[1,2])),Role(roleDict[role],[0,2]))
            rs.complete('⊑')
            roleChains.append(rs) 
        elif 'SubClassOf(' in line:
            line = line[11:-2]
            inter = False     
            test = 'ObjectSomeValuesFrom(' in line or 'ObjectIntersectionOf(' in line
            first = line.split(" ")[0] if not test or line[0] != 'O' else " ".join(line.split(" ",2)[:2])
            last = line.split(" ",1)[1] if not test  or line[0] != 'O' else line.split(" ",2)[2]
            
            if test and 'ObjectIntersectionOf(' in first:
                thiss = first[21:-1].split()
                inter = True
            elif test and 'ObjectSomeValuesFrom(' in first:
                thiss = first[21:-1].split()
            elif test and 'ObjectSomeValuesFrom(' in last:
                thiss = last[21:-1].split()
            else:
                thiss = None
            
            if len(first) <= 14 and len(last) <= 14:
                cs = ConceptStatement(len(CType1),True,Concept(classDict[first],[0]),Concept(classDict[last],[0]))
                cs.complete('⊑')
                CType1.append(cs)
            elif len(first) >= 20 and inter:
                cs1 = ConceptStatement(1,False,Concept(classDict[thiss[0]],[0]),Concept(classDict[thiss[1]],[0]))
                cs1.complete('⊓')
                cs = ConceptStatement(len(CType2),True,cs1,Concept(classDict[last],[0]))
                cs.complete('⊑')
                CType2.append(cs)
            elif len(first) >= 20:
                cs = ConceptStatement(len(CType3),True,ConceptRole('e',Role(roleDict[thiss[0]],[0,1]),Concept(classDict[thiss[1]],[1])),Concept(classDict[last],[0]))
                cs.complete('⊑')
                CType4.append(cs)
            elif len(last) >= 20:
                cs = ConceptStatement(len(CType4),True,Concept(classDict[first],[0]),ConceptRole('e',Role(roleDict[thiss[0]],[0,1]),Concept(classDict[thiss[1]],[1]))) 
                cs.complete('⊑')
                CType3.append(cs)
            else:
                print("nooooooooo")
            
        else:pass
        line = file.readline()
    
    random.shuffle(CType1)
    random.shuffle(CType2)
    random.shuffle(CType3)
    random.shuffle(CType4)
    random.shuffle(roleSubs)
    random.shuffle(roleChains)
    
    info = [['c',classes,classDict],['r',roles,roleDict],['cs',len(CType1),len(CType2),len(CType3),len(CType4)],['rs',len(roleSubs),len(roleChains)],['l',labelDict]]
    
    return [CType1,CType2,CType3,CType4],[roleSubs,roleChains],info

def makeKBFromSamples(concepts,roles,info,easy):
       
    start = 0
    allowedCNames = []
    allowedRNames = []
    
    while isinstance(start,int):
        start = random.randint(1,info[0][1])
        #print(start)
        for intersection in concepts[1]:
            if intersection.antecedent.antecedent.name == start or intersection.antecedent.consequent.name == start or intersection.consequent.name == start:
                start = intersection
                allowedCNames.append(intersection.antecedent.antecedent.name) 
                allowedCNames.append(intersection.antecedent.consequent.name)
                allowedCNames.append(intersection.consequent.name)
                break
    
    #4 2 8 2
    #2 2
    
    numCType1 = 4 if easy else 10
    numCType2 = 2 if easy else 10
    numCType3 = 8 if easy else 10
    numCType4 = 2 if easy else 10
    numRoleSubs = 2 if easy else 4
    numRoleChains = 2 if easy else 4
    
    CTypeNull = []
    CType1 = []
    CType2 = [start]
    CType3 = []
    CType4 = []
    roleSubs = []
    roleChains = []   
    allType3Names = []
    allType4Names = []
    allRSubNames = []
    allRChainNames = []
    
    for restriction in concepts[2]:
        allType3Names.append(restriction.consequent.concept.name)
        allType3Names.append(restriction.antecedent.name)
    allType3Names = list(dict.fromkeys(allType3Names))
    for restriction in concepts[3]:
        allType4Names.append(restriction.antecedent.concept.name)
        allType4Names.append(restriction.consequent.name) 
    allType4Names = list(dict.fromkeys(allType4Names))
    for restriction in roles[0]:
        allRSubNames.append(restriction.antecedent.name)
        allRSubNames.append(restriction.consequent.name)     
    allRSubNames = list(dict.fromkeys(allRSubNames))
    for restriction in roles[1]:
        allRChainNames.append(restriction.antecedent.roles[0].name)
        allRChainNames.append(restriction.antecedent.roles[1].name)
        allRChainNames.append(restriction.consequent.name)     
    allRChainNames = list(dict.fromkeys(allRChainNames))    
    
    while len(CType1) < numCType1:
        usedBefore = False
        inclusion = random.choice(concepts[0])
        for other in CType1: 
            if other.antecedent.name == inclusion.antecedent.name and other.consequent.name==inclusion.consequent.name:
                usedBefore = True
                break
        if not usedBefore and (inclusion.antecedent.name in allowedCNames or inclusion.consequent.name in allowedCNames):
            CType1.append(inclusion)
            allowedCNames.append(inclusion.antecedent.name)
            allowedCNames.append(inclusion.consequent.name)
            no1InC = False
            
    allowedCNames = list(dict.fromkeys(allowedCNames))
    
    while len(CType2) < numCType2:
        usedBefore = False
        intersection = random.choice(concepts[1])
        for other in CType2: 
            if intersection.antecedent.antecedent.name == other.antecedent.antecedent.name and intersection.antecedent.consequent.name==other.antecedent.consequent.name and other.consequent.name==inclusion.consequent.name:
                usedBefore = True
                break
        if not usedBefore and (intersection.antecedent.antecedent.name in allowedCNames or intersection.antecedent.consequent.name in allowedCNames or intersection.consequent.name in allowedCNames):
            CType2.append(intersection)
            allowedCNames.append(intersection.antecedent.antecedent.name) 
            allowedCNames.append(intersection.antecedent.consequent.name)
            allowedCNames.append(intersection.consequent.name)
            
    allowedCNames = list(dict.fromkeys(allowedCNames))
    no3InC = bool(set(allowedCNames) & set(allType3Names))
    
    while len(CType3) < numCType3:
            usedBefore = False
            restriction = random.choice(concepts[2])
            for other in CType3: 
                if restriction.consequent.concept.name == other.consequent.concept.name and restriction.consequent.role.name==other.consequent.role.name and other.antecedent.name==restriction.antecedent.name:
                    usedBefore = True
                    break
            if not usedBefore and (no3InC or restriction.consequent.concept.name in allowedCNames or restriction.antecedent.name in allowedCNames):
                CType3.append(restriction)
                allowedCNames.append(restriction.consequent.concept.name)
                allowedRNames.append(restriction.consequent.role.name)
                allowedCNames.append(restriction.antecedent.name)
                no3InC = False
            
    allowedCNames = list(dict.fromkeys(allowedCNames))
    allowedRNames = list(dict.fromkeys(allowedRNames))          
    no4InC = bool(set(allowedCNames) & set(allType4Names))
    
    while len(CType4) < numCType4:
            usedBefore = False
            restriction = random.choice(concepts[3])
            for other in CType4: 
                if restriction.antecedent.concept.name == other.antecedent.concept.name and restriction.antecedent.role.name==other.antecedent.role.name and other.consequent.name==restriction.consequent.name:
                    usedBefore = True
                    break
            if not usedBefore and (no4InC or restriction.antecedent.concept.name in allowedCNames or restriction.consequent.name in allowedCNames):
                    CType4.append(restriction)
                    allowedCNames.append(restriction.antecedent.concept.name)
                    allowedRNames.append(restriction.antecedent.role.name)
                    allowedCNames.append(restriction.consequent.name)
                    no4InC = False
    
    allowedCNames = list(dict.fromkeys(allowedCNames))
    allowedCNames.sort(key=lambda x: (x))
    allowedRNames = list(dict.fromkeys(allowedRNames))
    random.shuffle(allowedRNames)
    noChain = bool(set(allowedRNames) & set(allRChainNames))
   
    iterations = 0
    while len(roleChains) < numRoleChains:
        iterations = iterations + 1 
        noChain = True if iterations > 1000 else noChain      
        restriction = random.choice(roles[1])
        if restriction in roleChains: iterations = iterations + 1 ; noChain = iterations > 1000 ; continue
        elif noChain or restriction.antecedent.roles[0].name in allowedRNames or restriction.antecedent.roles[1].name in allowedRNames or restriction.consequent.name in allowedRNames:
            roleChains.append(restriction)
            allowedRNames.append(restriction.antecedent.roles[0].name)
            allowedRNames.append(restriction.antecedent.roles[1].name)
            allowedRNames.append(restriction.consequent.name)
            noChain = False
            iterations = 0
    noSub = bool(set(allowedRNames) & set(allRSubNames))
    iterations = 0
    while len(roleSubs) < numRoleSubs:
        iterations = iterations + 1 
        noSub = True if iterations > 1000 else noSub
        restriction = random.choice(roles[0])
        if restriction in roleSubs: continue
        elif noSub or restriction.antecedent.name in allowedRNames or restriction.consequent.name in allowedRNames:
            roleSubs.append(restriction)
            allowedRNames.append(restriction.antecedent.name)
            allowedRNames.append(restriction.consequent.name)
            noSub = False
            iterations = 0
            
    allowedRNames = list(dict.fromkeys(allowedRNames))
    allowedRNames.sort(key=lambda x: (x))
    
    if len(allowedCNames) > conceptSpace:
        raise
    
    if len(allowedRNames) > roleSpace:
        raise 
        
    for item in range(1,22):
        cs = ConceptStatement(item,True,Concept(item,[0]),Concept(item,[0]))
        cs.complete('⊑')
        CTypeNull.append(cs) 
    
    CTypeNull,CType1,CType2,CType3,CType4,roleSubs,roleChains = copyAllStatements(CTypeNull,CType1,CType2,CType3,CType4,roleSubs,roleChains)
    mapping,CTypeNull,CType1,CType2,CType3,CType4,roleSubs,roleChains,allowedCNames,allowedRNames = shiftNames(CTypeNull,CType1,CType2,CType3,CType4,roleSubs,roleChains,allowedCNames,allowedRNames)
    
    generator = HardGenERator2(rGenerator=GenERator(conceptNamespace=conceptSpace,roleNamespace=roleSpace,CTypeNull=CTypeNull,CType1=CType1,CType2=CType2,CType3=CType3,CType4=CType4,roleSubs=roleSubs,roleChains=roleChains),difficulty=0)
    
    generator.hasRun = True
    
    generator.genERate()
    
    return mapping,generator

def copyAllStatements(oldCTypeNull,oldCType1,oldCType2,oldCType3,oldCType4,oldroleSubs,oldroleChains):
    CTypeNull=[]
    CType1=[]
    CType2=[]
    CType3=[]
    CType4=[]
    roleSubs=[]
    roleChains=[]		
    for i in range(0,len(oldCTypeNull)):
        cs = ConceptStatement(len(CTypeNull),True,Concept(oldCTypeNull[i].antecedent.name,[0]),Concept(oldCTypeNull[i].consequent.name,[0]))
        cs.complete('⊑')
        CTypeNull.append(cs)

    for i in range(0,len(oldCType1)):
        cs = ConceptStatement(len(CType1),True,Concept(oldCType1[i].antecedent.name,[0]),Concept(oldCType1[i].consequent.name,[0]))
        cs.complete('⊑')
        CType1.append(cs)

    for i in range(0,len(oldCType2)):
        cs1 = ConceptStatement(1,True,Concept(oldCType2[i].antecedent.antecedent.name,[0]),Concept(oldCType2[i].antecedent.consequent.name,[0]))
        cs1.complete('⊓')
        cs = ConceptStatement(len(CType2),True,cs1,Concept(oldCType2[i].consequent.name,[0]))
        cs.complete('⊑')
        CType2.append(cs)

    for i in range(0,len(oldCType3)):
        cs = ConceptStatement(len(CType3),True,Concept(oldCType3[i].antecedent.name,[0]),ConceptRole('e',Role(oldCType3[i].consequent.role.name,[0,1]),Concept(oldCType3[i].consequent.concept.name,[1])))
        cs.complete('⊑')
        CType3.append(cs)

    for i in range(0,len(oldCType4)):
        cs = ConceptStatement(len(CType4),True,ConceptRole('e',Role(oldCType4[i].antecedent.role.name,[0,1]),Concept(oldCType4[i].antecedent.concept.name,[1])),Concept(oldCType4[i].consequent.name,[0]))
        cs.complete('⊑')
        CType4.append(cs)	

    for i in range(0,len(oldroleSubs)):
        rs = RoleStatement(len(roleSubs),True,Role(oldroleSubs[i].antecedent.name,[0,1]),Role(oldroleSubs[i].consequent.name,[0,1]))
        rs.complete('⊑')
        roleSubs.append(rs)

    for i in range(0,len(oldroleChains)):
        rs = RoleStatement(len(roleChains),True,RoleChain(0,Role(oldroleChains[i].antecedent.roles[0].name,[0,1]),Role(oldroleChains[i].antecedent.roles[1].name,[1,2])),Role(oldroleChains[i].consequent.name,[0,2]))
        rs.complete('⊑')
        roleChains.append(rs)
    
    return CTypeNull,CType1,CType2,CType3,CType4,roleSubs,roleChains
    
    
def shiftNames(CTypeNull,CType1,CType2,CType3,CType4,roleSubs,roleChains,allowedCNames,allowedRNames):
    newVal = 1
    mapping = {}
    for name in allowedCNames:
        mapping[name] = newVal
        for statement in CTypeNull:
            if statement.antecedent.name == name:
                statement.antecedent.name = mapping[name]
                statement.consequent.name = mapping[name]
        for statement in CType1:
            if statement.antecedent.name == name:
                statement.antecedent.name = mapping[name]
            if statement.consequent.name == name:
                statement.consequent.name = mapping[name]
        for statement in CType2:
            if statement.antecedent.antecedent.name == name:
                statement.antecedent.antecedent.name = mapping[name]
            if statement.antecedent.consequent.name == name:
                statement.antecedent.consequent.name = mapping[name]
            if statement.consequent.name == name:
                statement.consequent.name = mapping[name]
        for statement in CType3:
            if statement.antecedent.name == name:
                statement.antecedent.name = mapping[name]
            if statement.consequent.concept.name == name:
                statement.consequent.concept.name = mapping[name]
        for statement in CType4:
            if statement.antecedent.concept.name == name:
                statement.antecedent.concept.name = mapping[name]
            if statement.consequent.name == name:
                statement.consequent.name = mapping[name]
        newVal = newVal + 1
    
    newVal = 1    
    for name in allowedRNames:
        mapping[-name] = newVal
        for statement in CType3:
            if statement.consequent.role.name == name:
                statement.consequent.role.name = mapping[-name]
        for statement in CType4:
            if statement.antecedent.role.name == name:
                statement.antecedent.role.name = mapping[-name]
        for statement in roleSubs:
            if statement.antecedent.name == name:
                statement.antecedent.name = mapping[-name]
            if statement.consequent.name == name:
                statement.consequent.name = mapping[-name] 
        for statement in roleChains:
            if statement.antecedent.roles[0].name == name:
                statement.antecedent.roles[0].name = mapping[-name]
            if statement.antecedent.roles[1].name == name:
                statement.antecedent.roles[1].name = mapping[-name]
            if statement.consequent.name == name:
                statement.consequent.name = mapping[-name] 
        newVal = newVal + 1
    
    return mapping,CTypeNull,CType1,CType2,CType3,CType4,roleSubs,roleChains,allowedCNames,allowedRNames
    
def sampleDataHardGenerator2Format(trials,easy,x):
    concepts,roles,info = x   
    seq_in = numpy.empty(trials,dtype=numpy.ndarray)
    seq_out = numpy.empty(trials,dtype=numpy.ndarray)
    kbs = numpy.empty([trials,80 if easy else 588],dtype=numpy.float32)
    if not os.path.isdir("snoutput"): os.mkdir("snoutput")
    i = 0

    while i < trials:

        print(i)

        localmap,generator = makeKBFromSamples(concepts,roles,info,easy)
        
        kbs[i] = array(generator.toVector())

        reasoner = ReasonER(generator,showSteps=True)

        reasoner.ERason()
        
        if len(reasoner.KBaLog) > 4 or len(reasoner.KBaLog) < 2:
            continue

        dependencies = DependencyReducer(generator.getAllExpressions(),reasoner.sequenceLog,reasoner.KBsLog,reasoner.KBaLog)

        seq_in[i],seq_out[i] = dependencies.toVector(generator.conceptNamespace,generator.roleNamespace)

        if not os.path.isdir("snoutput/Dataset/{}".format(i)): os.mkdir("snoutput/Dataset/{}".format(i))
        if len(reasoner.KBaLog) > 0 and not os.path.isdir("snoutput/Dataset/{}/Reasoner Steps".format(i)): os.mkdir("snoutput/Dataset/{}/KB after sequence".format(i))
        generator.toStringFile("snoutput/Dataset/{}/completedKB.txt".format(i))
        reasoner.toStringFile("snoutput/Dataset/{}/completedKB.txt".format(i))
        for j in range(0,len(dependencies.donelogs[2])):
            if len(reasoner.KBaLog[j]) > 0: writeFile("snoutput/Dataset/{}/Reasoner Steps/reasonerStep{}.txt".format(i,j+len(reasoner.sequenceLog)),dependencies.toString(dependencies.donelogs[2][j]))
            
        i = i + 1


    numpy.savez("ssaves/dataEasy" if easy else 'ssaves/data', kbs,seq_in,seq_out)

    return kbs,seq_in,seq_out    
    

def shallowSystem(n_epochs0,learning_rate0):
    log.write("Testing Stepwise Trained LSTM\n\nMapping KB to Reasoner Justifications\n\n")
    print("")
    
    train_size0 = KBs_train.shape[0]
    n_neurons0 = X_train.shape[2]
    n_layers0 = 1
    
    X0 = tf.placeholder(tf.float32, shape=[None,KBs_train.shape[1],KBs_train.shape[2]])
    y0 = tf.placeholder(tf.float32, shape=[None,X_train.shape[1],X_train.shape[2]])
    
    basic_cell0 = tf.contrib.rnn.LSTMBlockCell(num_units=n_neurons0)
    multi_layer_cell0 = tf.contrib.rnn.MultiRNNCell([basic_cell0] * n_layers0)
    outputs0, states0 = tf.nn.dynamic_rnn(multi_layer_cell0, X0, dtype=tf.float32)
    
    loss0 = tf.losses.mean_squared_error(y0,outputs0)
    optimizer0 = tf.train.AdamOptimizer(learning_rate=learning_rate0)
    training_op0 = optimizer0.minimize(loss0)
    
    init0 = tf.global_variables_initializer()
    
    saver = tf.train.Saver()
    
    with tf.Session() as sess:
        init0.run()
        mse0 = 0
        mseL = 0
        for epoch in range(n_epochs0):  
            print("Piecewise System\tEpoch: {}".format(epoch))
            ynew,a = sess.run([outputs0,training_op0],feed_dict={X0: KBs_train,y0: X_train})
            mse = loss0.eval(feed_dict={outputs0: ynew, y0: X_train})
            if epoch == 0: mse0 = mse
            if epoch == n_epochs0 - 1: mseL = mse
            log.write("Epoch: {}\tMean Squared Error:\t{}\n".format(epoch,mse))
            if mse < 0.0001:
                mseL = mse
                break
        
        y_pred = sess.run(outputs0,feed_dict={X0: KBs_test,y0: X_test}) 
        mseNew = loss0.eval(feed_dict={outputs0: y_pred, y0: X_test})
        newPreds,newStatements = vecToStatements(y_pred,conceptSpace,roleSpace)
        
        log.write("\nTraining Statistics\n\nPrediction\tMean Squared Error:\t{}\nTraining\tLearned Reduction MSE:\t{}\n\t\tIncrease MSE on New:\t{}\n\t\tPercent Change MSE:\t{}\n\n".format(numpy.float32(mseNew),mse0-mseL,numpy.float32(mseNew)-mseL,(mseL - mse0)/mse0*100))
        
        writeVectorFile("snoutput/KBFitEasy.txt" if easy else "snoutput/KBFit.txt",newStatements)
        
        numpy.savez("ssaves/halfwayEasy.npz" if easy else "ssaves/halfway.npz", y_pred)
      
    tf.reset_default_graph()
    
    log.write("\nMapping Reasoner Justifications to KB Completion\n\n")
    
    train_size1 = X_train.shape[0]
    n_neurons1 = y_train.shape[2]
    
    X1 = tf.placeholder(tf.float32, shape=[None,X_train.shape[1],X_train.shape[2]])
    y1 = tf.placeholder(tf.float32, shape=[None,y_train.shape[1],y_train.shape[2]])
    
    basic_cell1 = tf.contrib.rnn.LSTMBlockCell(num_units=n_neurons1)
    multi_layer_cell1 = tf.contrib.rnn.MultiRNNCell([basic_cell1] * n_layers0)
    outputs1, states1 = tf.nn.dynamic_rnn(multi_layer_cell1, X1, dtype=tf.float32)
    
    loss1 = tf.losses.mean_squared_error(y1,outputs1)
    optimizer1 = tf.train.AdamOptimizer(learning_rate=learning_rate0)
    training_op1 = optimizer1.minimize(loss1)
    
    
    init1 = tf.global_variables_initializer()
    
    with tf.Session() as sess:    
        init1.run()
        mse0 = 0
        mseL = 0
        for epoch in range(n_epochs0):  
            print("Piecewise System\tEpoch: {}".format(epoch+n_epochs0))
            ynew,a = sess.run([outputs1,training_op1],feed_dict={X1: X_train,y1: y_train})
            mse = loss1.eval(feed_dict={outputs1: ynew, y1: y_train})
            if epoch == 0: mse0 = mse
            if epoch == n_epochs0 - 1: mseL = mse
            log.write("Epoch: {}\tMean Squared Error:\t{}\n".format(epoch,mse))
            if mse < 0.0001:
                mseL = mse
                break
        
        y_pred = sess.run(outputs1,feed_dict={X1: X_test})  
        mseNew = loss1.eval(feed_dict={outputs1: y_pred, y1: y_test})
        
        log.write("\nTraining Statistics\n\nPrediction\tMean Squared Error:\t{}\nTraining\tLearned Reduction MSE:\t{}\n\t\tIncrease MSE on New:\t{}\n\t\tPercent Change MSE:\t{}\n".format(numpy.float32(mseNew),mse0-mseL,numpy.float32(mseNew)-mseL,(mseL - mse0)/mse0*100))
        
        log.write("\nTESTING HOLDOUT JUSTIFICATION DATA\n\n")    
          
        newPreds,newStatements = vecToStatements(y_pred,conceptSpace,roleSpace)
        distTRan,distRReal = levDistance(newStatements,trueStatements,conceptSpace,roleSpace)
        cdistTRan,cdistRReal = customDistance(newPreds,preds,conceptSpace,roleSpace)   
        
        log.write("Levenshtein Distance From Actual to Random Data:    {}\nLevenshtein Distance From Actual to Predicted Data: {}\n".format(distTRan,distRReal))
        log.write("\nCustom Distance From Actual to Random Data:    {}\nCustom Distance From Actual to Predicted Data: {}\n".format(cdistTRan,cdistRReal))
        
        #log.write("Levenshtein Distance From Actual to Random Data:    {}\nLevenshtein Distance From Predicted to Random Data: {}\nLevenshtein Distance From Actual to Predicted Data: {}\n".format(distTRan,distRRan,distRReal))
        #log.write("\nCustom Distance From Actual to Random Data:    {}\nCustom Distance From Predicted to Random Data: {}\nCustom Distance From Actual to Predicted Data: {}\n".format(cdistTRan,cdistRRan,cdistRReal))
        
        writeVectorFile("snoutput/predictedOutEasy.txt" if easy else "snoutput/predictedOut.txt",newStatements)
        
        data = numpy.load("ssaves/halfwayEasy.npz" if easy else "ssaves/halfway.npz",allow_pickle=True)
        data = data['arr_0'] 
        
        log.write("\nTESTING PIPELINED KB DATA\n\n")
        
        y_pred = sess.run(outputs1,feed_dict={X1: data})
        newPreds,newStatements = vecToStatements(y_pred,conceptSpace,roleSpace)
        distTRan,distRReal = levDistance(newStatements,trueStatements,conceptSpace,roleSpace)
        cdistTRan,cdistRReal = customDistance(newPreds,preds,conceptSpace,roleSpace)
        
        log.write("Levenshtein Distance From Actual to Random Data:    {}\nLevenshtein Distance From Actual to Predicted Data: {}\n".format(distTRan,distRReal))
        
        log.write("\nCustom Distance From Actual to Random Data:    {}\nCustom Distance From Actual to Predicted Data: {}\n\n".format(cdistTRan,cdistRReal))    
        
        writeVectorFile("snoutput/predictedOutPEasy.txt" if easy else "snoutput/predictedOutP.txt",newStatements)
        
def deepSystem(n_epochs2,learning_rate2):
    log.write("Testing Deep LSTM\n\nMapping KB to hidden layer to KB Completion\n\n")
    print("")
    
    train_size2 = X_train.shape[0]
    n_neurons2 = y_train.shape[2]
    n_layers2 = 1
    
    X0 = tf.placeholder(tf.float32, shape=[None,KBs_train.shape[1],KBs_train.shape[2]])
    y1 = tf.placeholder(tf.float32, shape=[None,y_train.shape[1],y_train.shape[2]])
    
    basic_cell1 = [tf.contrib.rnn.LSTMBlockCell(num_units=X_train.shape[2]),tf.contrib.rnn.LSTMBlockCell(num_units=y_train.shape[2])]
    multi_layer_cell2 = tf.contrib.rnn.MultiRNNCell(basic_cell1)
    outputs2, states2 = tf.nn.dynamic_rnn(multi_layer_cell2, X0, dtype=tf.float32)
    
    loss2 = tf.losses.mean_squared_error(y1,outputs2)#tf.reduce_sum(tf.reduce_sum(tf.reduce_sum(tf.math.square(outputs - y))))/(tf.to_float(tf.size(y)))
    optimizer2 = tf.train.AdamOptimizer(learning_rate=learning_rate2)
    training_op2 = optimizer2.minimize(loss2)
    
    init2 = tf.global_variables_initializer()
    
    with tf.Session() as sess:    
        init2.run()
        mse0 = 0
        mseL = 0
        for epoch in range(n_epochs2): 
            print("Deep System\t\tEpoch: {}".format(epoch))
            ynew,a = sess.run([outputs2,training_op2],feed_dict={X0: KBs_train,y1: y_train})
            mse = loss2.eval(feed_dict={outputs2: ynew, y1: y_train})
            if epoch == 0: mse0 = mse
            if epoch == n_epochs2 - 1: mseL = mse
            log.write("Epoch: {}\tMean Squared Error:\t{}\n".format(epoch,mse))
            if mse < 0.0001:
                mseL = mse
                break
        
        y_pred = sess.run(outputs2,feed_dict={X0: KBs_test})  
        mseNew = loss2.eval(feed_dict={outputs2: y_pred, y1: y_test})
        log.write("\nTraining Statistics\n\nPrediction\tMean Squared Error:\t{}\nTraining\tLearned Reduction MSE:\t{}\n\t\tIncrease MSE on New:\t{}\n\t\tPercent Change MSE:\t{}\n".format(numpy.float32(mseNew),mse0-mseL,numpy.float32(mseNew)-mseL,(mseL - mse0)/mse0*100))
        
        log.write("\nTESTING HOULDOUT DATA\n\n")    
          
        newPreds,newStatements = vecToStatements(y_pred,conceptSpace,roleSpace)
        distTRan,distRReal = levDistance(newStatements,trueStatements,conceptSpace,roleSpace)
        cdistTRan,cdistRReal = customDistance(newPreds,preds,conceptSpace,roleSpace)   
        
        log.write("Levenshtein Distance From Actual to Random Data:    {}\nLevenshtein Distance From Actual to Predicted Data: {}\n".format(distTRan,distRReal))
        log.write("\nCustom Distance From Actual to Random Data:    {}\nCustom Distance From Actual to Predicted Data: {}\n".format(cdistTRan,cdistRReal))
        
        writeVectorFile("snoutput/predictedOutDEasy.txt" if easy else "snoutput/predictedOutD.txt",newStatements)    



if __name__ == "__main__":
    if not os.path.isdir("ssaves"): os.mkdir("ssaves")
    if not os.path.isdir("snoutput"): os.mkdir("snoutput")
    if not os.path.isdir("snoutput/Dataset"): os.mkdir("snoutput/Dataset")
    
    easy = True
    conceptSpace = 21 if easy else 106
    roleSpace = 8 if easy else 56  
    
    if len(sys.argv) == 3:
        epochs = int(sys.argv[1])
        learningRate = float(sys.argv[2])
    else:
        epochs = 100000 if easy else 50000
        learningRate = 0.0001 if easy else 0.005        
    
    log = open("slog.txt","w")
    
    KBs,dependencies,output = getDataFromFile('ssaves/dataEasy.npz' if easy else 'ssaves/data.npz',easy)#sampleDataHardGenerator2Format(1000,easy,fsOWLReader(normalizeFS("SNOMED/SNOMED2012fs.owl","SNOMED/SNOrMED2012fs.owl")))#
    
    fileShapes1 = [4,204,52] if easy else [8,2116,324]

    KBs_test,KBs_train = repeatAndSplitKBs(KBs,fileShapes1[0],0.33)
                            
    X_train, X_test, y_train, y_test = splitTensors(dependencies, output, 0.33)
    
    X_train = pad(X_train,maxlen1=fileShapes1[0],maxlen2=fileShapes1[1])
    X_test = pad(X_test,maxlen1=fileShapes1[0],maxlen2=fileShapes1[1])
    
    y_train = pad(y_train,maxlen1=fileShapes1[0],maxlen2=fileShapes1[2])
    y_test = pad(y_test,maxlen1=fileShapes1[0],maxlen2=fileShapes1[2])
    
    print("KBs shape:\t\t{}\nExtended KBs shape:\t{}{}\nDependencies shape:\t{}{}\nOutput shape:\t\t{}{}\n\n".format(KBs.shape,KBs_train.shape,KBs_test.shape,X_train.shape,X_test.shape,y_train.shape,y_test.shape))
    log.write("KBs shape:\t\t{}\nExtended KBs shape:\t{}{}\nDependencies shape:\t{}{}\nOutput shape:\t\t{}{}\n\n".format(KBs.shape,KBs_train.shape,KBs_test.shape,X_train.shape,X_test.shape,y_train.shape,y_test.shape))

    KBvec,KBstr = vecToStatements(KBs_test,conceptSpace,roleSpace)
    preds,trueStatements = vecToStatements(y_test,conceptSpace,roleSpace)
    placeholder,inputs = vecToStatements(X_test,conceptSpace,roleSpace)
    
    writeVectorFile("snoutput/KBsInEasy.txt" if easy else "snoutput/KBsIn.txt",KBstr)
    writeVectorFile("snoutput/dependenciesEasy.txt" if easy else "snoutput/dependencies.txt",inputs)
    writeVectorFile("snoutput/targetOutEasy.txt" if easy else "snoutput/targetOut.txt",trueStatements)
    
    shallowSystem(epochs,learningRate)
    
    tf.reset_default_graph()
    
    deepSystem(epochs*2,learningRate/2)
    
    log.close()
    
    print('\nDone')
 