#MnemonicTable mnemonic:opcode,type,size
MnemonicTable={'STR':['#R1','AD',],
               'MOVER':['01','IS',2],
               'MOVEM':['02','IS',2],
               'MUL':['03','IS',2],
               'SUB':['04','IS',2],
               'RD':['05','IS',2],
               'BC':['03','IS',3], 
               'LTORG':['#R3','AD',],
               'DCON':['#R5','DL',],
               'DSTR':['07','DL'],
               'END':['#R2','AD',],
               'JM':['08','IS',3],
               'INCR':['09','IS',2]}

MCA=[]
s=[]
ulc=0
n=0
dupsym=[]
def process(string):
    global MCA
    global ulc
    global n
    string=line.split(' ')
    
    try:
        word1=string[1].split(',')                  
        if 'AD' in string[1]:               
            if '#R1' in string[1]:
                word1.remove(word1)         
        word0=string[0].split(' ')         
                           
        MCA.append('\n')
        MCA.append(word0[0]+' ')
        MCA.append(word1[1]+' ')
        
        word2=string[2].split(',')                  
        
        MCA.append(word2[1])
        
        if len(string[3])!=0:
            word3=string[3].split(',')
            MCA.append(' '+word3[1])
            if 'S' in string[3]:
                word4=string[3].split(',')
                MCA.append(' ')
                i=1
                n=len(s)
                if int(word4[1])>n:
                    print("Error Symbol used but not defined")
                for i in range (0,n):
                    if str(i) in word4[1]:
                        MCA.append(s[i-1])
                        i+=1
    except:     
        if word1[0]=="DL" and word1[1]=="07" and 'C' in word2[0]:           
                lc=int(word2[1])
                tlc=lc+ulc-1 
                while ulc<tlc:
                 MCA.append('\n'+str(ulc+1))
                 ulc+=1
        pass
    
    
    return(MCA)
   
mcode=open("MachineCode.txt","a")

icfile=open("Pass2IC.txt","r")
lines=icfile.readlines()
sym=open("SymbolTable.txt","r")
sym=sym.readlines()

        

for line in sym:                                
    symbol=line.split(' ')
    if symbol[0] not in dupsym:
        s.append(symbol[1].rstrip())
        dupsym.append(symbol[0])
        n=len(s)
    else:
        print("Error Duplicate symbol in symbol table")
        exit()
        
    
for line in lines:
    string=process(line)

for i in MCA:                           
    j=str(i)
    mcode.write(j)
mcode.close()


