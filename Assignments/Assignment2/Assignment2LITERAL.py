#MnemonicTable mnemonic:opcode,type,size
MnemonicTable={'MOVER':['01','IS',2],
               'ADD':['02','IS',2],
               'LTORG':['01','AD','#R1'],
               'ORG':['02','AD','#R2'],
               'START':['03','AD','#R3'],
               'BC':['03','IS',3],
               'DC':['2','DL',1],
               'DS':['3','DL'],
               'END':['04','AD','#R4'],
               'MOV':['04','IS',2],
               'MOVEM':['05','IS',2],
               'JZ':['06','IS',2],
               'READ':['07','IS',2],
               'SUB':['08','IS',2],
               'INC':['09','IS',1]}
RegisterTable={'AREG':[1],
               'BREG':[2],
               'CREG':[3]}
SymbolTable={}
LitTable={}
Pooltable=[]
lc=0
IC=[]
addds=0

def process(string):
    global l
    flist=[]
    word=string.split("\t")
    n=len(word)
    #print(word)
    #print(word[0])
    if ' ' in word[0]:
       flist.append("")
       word.remove(word[0])
    elif word[0] in MnemonicTable.keys():
        flist.append("")
        flist.append(word[0])
        word.remove(word[0])
    elif ':' in word[0]:
         if ':' in word[0]:  #checking Label
             flist.append(word[0][:len(word[0])-1])
             word.remove(word[0])
    else:
        flist.append(word[0])
        word.remove(word[0])
    if word[0] in MnemonicTable.keys(): #checking Mnemonic
        flist.append(word[0])
        word.remove(word[0])
    else:
        print('Error:Mnemonic not present in the Mnemonic Table')
        exit(0)
            
    if n>0:
        try:
            if ',' in word[0]:
                op=word[0].split(',')
                flist.append(op[0])
                word.remove(word[0])
                #flist.append(op[1])
                if '=' in op[1]:
                    l=op[1]
                    flist.append(l[1])
                    #print(l)
                    #word.remove(l[1])
                    
                else:
                    flist.append(op[1])
                    word.remove(word[0])
            else:
                flist.append(word[0])
                word.remove(word[0])
        except:
            pass
    else:
        flist.append("")
        flist.append("")
    print(flist)
    return flist
  
    

def classgen(string):
    #print(string[0])
    #print(string[1])
    if len(string[2])!=0:
        if string[2].isalpha():
            try:
                if(string[3].isdigit()):
                    IC.append(string[2]+',')
                    IC.append(('L',string[3]))
            
                elif(string[3] in SymbolTable.keys()):
                    IC.append(('S', list(SymbolTable.keys()).index(string[3])))
                elif(string[0] not in SymbolTable.keys()):
                    IC.append((string[2]+','))
                else:
                    IC.append((string[2],string[3]))
            except:
                pass
            
        elif string[2].isdigit():
            IC.append(('C',string[2]))
        else:
            IC.append((string[2]))
    return(IC)
my_file=open("SP.txt","r")
line=my_file.readlines()
icfile=open("IC.txt","a")

#print(line)
for i in line:
    #print(i)
    #i=i.rstrip()
    string=process(i.rstrip())
   
    if(string[1] in MnemonicTable.keys()):
        if(MnemonicTable[string[1]][1] == 'AD'):
            if(string[1] == 'START'):
                print('LC value:',lc)
                IC.append((MnemonicTable[string[1]][1],MnemonicTable[string[1]][0]))
                IC.append(('C',string[2]))
                IC.append(lc)
                lc=int(string[2])
            elif(string[1] == 'END'):
                lc+=addds
                IC.append((lc))
                IC.append((MnemonicTable[string[1]][1],MnemonicTable[string[1]][0]))
                #print(IC)
                print('Final lc value:',lc)
                LitTable[l]=lc
                Pooltable.append(list(LitTable.keys()).index(l))
            elif (string[1]== 'LTORG'):
                lc+=1
                print('LC value:',lc)
                IC.append((MnemonicTable[string[1]][1], MnemonicTable[string[1]][0]))
                LitTable[l]=lc
                Pooltable.append(list(LitTable.keys()).index(l))
                    
        elif(MnemonicTable[string[1]][1] == 'IS'):
            if(string[1] == 'MOVER'):
                lc+=2
                IC.append(lc)
                IC.append((MnemonicTable[string[1]][1],MnemonicTable[string[1]][0]))
                classgen(string)
                print('LC value:',lc)
            elif(string[1] == 'ADD' or 'BC' or 'INC' or 'SUB' or 'JZ' or 'READ'):
                lc += int(MnemonicTable[string[1]][2])
                print('LC value:',lc)
                IC.append(lc)
                IC.append((MnemonicTable[string[1]][1],MnemonicTable[string[1]][0]))
                classgen(string)
                
        elif(MnemonicTable[string[1]][1] == 'DL'):
            if string[1]=='DC':
                lc+=int(MnemonicTable[string[1]][2])
                print('LC value:',lc)
                IC.append(lc)
                IC.append((MnemonicTable[string[1]][1],MnemonicTable[string[1]][0]))
                classgen(string)
                
            elif string[1]=='DS':
                lc+=2
                addds=int(string[2])
                print('LC value:',lc)
                IC.append(lc)
                IC.append((MnemonicTable[string[1]][1],MnemonicTable[string[1]][0]))
                classgen(string)
                
    if len(string[0])!=0:
        SymbolTable[string[0]] = lc
        print("Symbol Table :")
        IC.append(('S', list(SymbolTable.keys()).index(string[0])))
        print(SymbolTable)
    
print(LitTable)
print(Pooltable)
print(SymbolTable)


for i in IC:
    j=str(i)
    #print(j)
    if 'AD' in j or 'IS' in j or 'DL' in j:
        icfile.write('\n'+j)
    else:
        icfile.write(j)
icfile.close()


#ic.append((AD , 05) AREG,4)
    #print(string[0])   

#for i in ic:
    #print(i)
