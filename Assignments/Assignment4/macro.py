kpdt=[] 
sst=[]  
mdt=[] 
ssnt=[]
pnt=[]
evnt=[]
mntl=[]
evt=[]
apdt=[]
pp=0
kp=0
ev=0
cmdtp=25
mdtp=25
kpdtp=10
sstp=5
    
mdtfile=open('MDT.txt','a')


file=open('macrosrc.txt','r')
lines=file.readlines()
if 'STARTMAC' in lines[0]:
       macname=str(lines[0]).split('\t')
       name=macname[2]
for line in lines:
   string=line.split('\t')
   print(mdtp,string)
        
   if len(string[0])!=0:
        if '.' in string[0]:
                ssnt.append(string[0][1:len(string[0])])
                sst.append("{} {}".format(sstp,mdtp))
        if '&' in string[0]:
                if 'SET' in string[1]:
                 if '0' in string[2]:
                  mdt.append("(E,{}) {} {}".format(ev,string[1],string[2]))
                 else:
                  e=string[2].split('+')
                  mdt.append("(E,{}) {} (E,{})+{}".format(ev,string[1],ev,e[1]))

   try:
    if len(string[1])!=0:
         mdtp+=1
         if 'LCL' in string[1]:
                ev+=1
                evnt.append(string[2][1:len(string[2])].strip())
                mdt.append("{} {} (E,{})".format(string[1],ev))
         
         if 'AIF' in string[1]:
                sym=string[2].split('.')
                if sym[1].rstrip() in ssnt:
                       mdt.append(" {} ((E,{} NE (P,{})) (S,{})".format(string[1],ev,pnt.index(pnt[2]),sstp))
         if 'MOVER' in string[1] or 'MOVEM' in string[1]:
                if len(string[2])!=0:
                  if '=' in string[2]:
                   reg=string[2].split('=')
                   if '+' in reg[1]:
                    mdt.append("{} (P,{}),(P,{})+(E,{})".format(string[1],pnt.index('REG'),pnt.index('X'),ev))
                   else:
                     mdt.append("{} (P,{}) {}".format(string[1],pnt.index('REG'),reg[1].rstrip()))
         if 'ENDMAC' in string[1]:
                mdt.append("{}".format(string[1]))
        
         if  ',' in string[3]:
                word=string[3].split(',')
                n=len(word)
                for i in range (0,n):
                 if '=' not in word[i]:
                  pnt.append(word[i][1:len(word[i])])
                  pp+=1
                 if '=' in word[i]:
                  kp+=1
                  val=word[i].split('=')
                  pnt.append(val[0][1:len(val[0])])
                  keyp=kpdtp,val[0][1:len(val[0])]+' '+val[1].rstrip()
                  kpdt.append(keyp)
                  apdt.append(val[1].rstrip())

   except:
         pass
         
        
    
mntl.append("{} {} {} {} {} {} {}".format(name,pp,kp,ev,cmdtp,kpdtp,sstp))
for i in mntl:
    mnt=str(i)
for i in mdt:
    mdts=str(i)
    mdtfile.write(mdts)
mdtfile.close()
print('MNT:'+mnt)
print(mdt)
print('PNTAB:',pnt)
print('KPDTAB:',kpdt)
print('SSNTAB:',ssnt)
print('EVNTAB:',evnt)
print('APDTAB:',apdt)
print('SST:',sst)
