import pandas as pd
Keyword=['','if','for','while','int','float']
Operators=['','+','-','*','/','<','>','<=','>=','=']
Delimiters=['','(',')','{','}',';']
Symbol=['',]
lineno=[]
Lexemes=[]
Token=[]
TokenValue=[]
l=0
file=open('compilersrc.txt','r')
content=file.readlines()
count=len(content)
for line in content:
   l+=1
   line=line.rstrip()
   data=line.split(' ')
   try:
     for i in range (0,count):
       Lexemes.append(data[i])
       if data[i].isalpha():
          if data[i] in Keyword:
            lineno.append(l)
            Token.append('Keyword')
            indk=Keyword.index(data[i])
            TokenValue.append(indk)
          elif data[i] not in Symbol:
            lineno.append(l)
            Symbol.append(data[i])
            Token.append('Identifier')
            inds=Symbol.index(data[i])
            TokenValue.append(inds)
          elif data[i] in Symbol:
             lineno.append(l)
             Token.append('Identifier')
             inds=Symbol.index(data[i])
             TokenValue.append(inds)
       elif data[i] in Delimiters:
           lineno.append(l)
           Token.append('Delimiter')
           indd=Delimiters.index(data[i])
           TokenValue.append(indd)
       elif data[i] in Operators:
           lineno.append(l)
           Token.append('Operator')
           indo=Operators.index(data[i])
           TokenValue.append(indo)
   except:
        pass
TAB={'Line no':lineno,
     'Lexemes':Lexemes,
     'Token':Token,
     'TokenValue':TokenValue}

df = pd.DataFrame(TAB, columns = ['Line no','Lexemes','Token','TokenValue'])
print(df)
