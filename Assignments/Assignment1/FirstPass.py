#MnemonicTable mnemonic:opcode,type,size
MnemonicTable={'MOVER':['01','IS',2],
               'ADD':['02','IS',2],
               'LTORG':['01','AD',0],
               'START':['02','AD',0],
               'BC':['03','IS',3],
               'DC':['2','DL',1],
               'DS':['3','DL'],
               'END':['03','AD',0]}
RegTable={'':'',
          'AREG':'1',
          'BREG':'2',
          'CREG':'3',
          'DREG':'4'}
condition={'':'','ANY':'1','EQU':'2','LT':'3','GT':'4','LE':'5','GE':'6'}
SymbolTable={'':''}
lc=0
IC=[]

def process(string):
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
        #return flist
            
    if n>0:
        try:
            if  ',' in word[0]:     #adding operand and removing
                op=word[0].split(',')
                flist.append(op[0])
                word.remove(word[0])
                flist.append(op[1])
            else:
                flist.append(word[0])
                word.remove(word[0])
        except:
            pass
    else:
        flist.append("")
        flist.append("")

    return flist
  
    print(flist)

def classgen(string):
    #print(string[0])
    #print(string[1])
    #if string[3]!=None:
        
    if len(string[2])!=0:
        if string[2].isalpha():
            if(string[2] in RegTable.keys()):
                IC.append('R,{}'.format(list(RegTable.keys()).index(string[2])))
                IC.append(' ')
                if (string[3] in RegTable.keys()): 
                    IC.append('R,{}'.format(list(RegTable.keys()).index(string[3])))
                    IC.append(' ')
                elif string[3].isdigit():
                    IC.append('C,{}'.format(string[3]))
                    IC.append(' ')
            elif (string[2] not in RegTable.keys() and string[3].isdigit):
                IC.append('{},{}'.format(string[2],string[3]))
                IC.append(' ')
        elif string[2].isdigit():
            IC.append('C,{}'.format(string[2]))
            IC.append(' ')
        
    
    for  i in (0,3):
        if(string[i]!='' and string[i] not in SymbolTable.keys() and string[i] not in RegTable.keys()):
            SymbolTable[string[i]] = lc
            IC.append('S,{}'.format(list(SymbolTable.keys()).index(string[i])))
            IC.append(' ')

    return IC
                      
my_file=open("FirstPass.txt","r")
line=my_file.readlines()
icfile=open("FirstPassIC.txt","a")
sym=open("SymbolTable.txt","a")
#print(line)
for i in line:
    string=process(i.rstrip())
    print(string)

    if(len(string[0])!=0):
        #SymbolTable.update(string[0])
        SymbolTable[string[0]] = lc
        #print("Symbol Table :")
        #print(SymbolTable)
        
    
    if(string[1] in MnemonicTable.keys()):
        if(MnemonicTable[string[1]][1] == 'AD'):
            if(string[1] == "START"):
                IC.append(lc)
                IC.append('  ')
                print('LC value:',lc)
                #print('LC value:',lc)
                IC.append('{},{}'.format(MnemonicTable[string[1]][1],MnemonicTable[string[1]][0]))
                IC.append(' ')
                IC.append('C,{}'.format(string[2]))
                IC.append(' ')
                IC.append('\n')
                lc=int(string[2])
            elif(string[1] == "END"):
                IC.append(lc)
                IC.append('  ')
                print('LC value:',lc)
                IC.append('{},{}'.format(MnemonicTable[string[1]][1],MnemonicTable[string[1]][0]))
                IC.append(' ')
                IC.append('\n')
                
                print('Final lc value:',lc)
        elif(MnemonicTable[string[1]][1] == 'IS'):
            if(string[1] == "MOVER"):
                IC.append(lc)
                IC.append('  ')
                print('LC value:',lc)
                IC.append('{},{}'.format(MnemonicTable[string[1]][1],MnemonicTable[string[1]][0]))
                IC.append(' ')
                classgen(string)
                IC.append('\n')
                lc += int(MnemonicTable[string[1]][2])
                #print('LC value:',lc)
            elif(string[1] == "ADD"):
                IC.append(lc)
                IC.append('  ')
                print('LC value:',lc)
                IC.append('{},{}'.format(MnemonicTable[string[1]][1],MnemonicTable[string[1]][0]))
                IC.append(' ')
                classgen(string)
                IC.append('\n')
                lc += int(MnemonicTable[string[1]][2])
            elif(string[1] == "BC"):
                IC.append(lc)
                IC.append('  ')
                print('LC value:',lc)
                IC.append('{},{}'.format(MnemonicTable[string[1]][1],MnemonicTable[string[1]][0]))
                if (string[2] in condition):
                    IC.append(' ')
                    IC.append('D,{}'.format(list(condition.keys()).index(string[2])))
                    IC.append(' ')
                    if(string[3] in SymbolTable.keys()):
                        IC.append('S,{}'.format(list(SymbolTable.keys()).index(string[3])))
                        IC.append(' ')
                else:
                    IC.append(' ')
                    classgen(string)
                    IC.append(' ')
                IC.append('\n')
                lc += int(MnemonicTable[string[1]][2])
        elif(MnemonicTable[string[1]][1] == 'DL'):
            if string[1]=="DC":
                IC.append(lc)
                print('LC value:',lc)
                IC.append('  ')
                IC.append('{},{}'.format(MnemonicTable[string[1]][1],MnemonicTable[string[1]][0]))
                IC.append(' ')
                #classgen(string)
                IC.append('C,{}'.format(string[2]))
                IC.append(' ')
                IC.append('\n')
                lc+=int(MnemonicTable[string[1]][2])
            elif string[1]=="DS":
                IC.append(lc)
                print('LC value:',lc)
                IC.append('  ')
                IC.append('{},{}'.format(MnemonicTable[string[1]][1],MnemonicTable[string[1]][0]))
                IC.append(' ')
                #classgen(string)
                IC.append('C,{}'.format(string[2]))
                IC.append(' ')
                IC.append('\n')
                lc+=int(string[2])
                
for key,value in SymbolTable.items():
    if(key!="" and value!=""):
        print(key, ' ', value)
        sym.write(key+" "+str(value)+"\n")
sym.close()  


for i in IC:
    j=str(i)
    #print(j)
    icfile.write(j)
icfile.close()






