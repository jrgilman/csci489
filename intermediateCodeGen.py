from scanner.parser import Parser
from scanner.scanner import Scanner
from pythonds.basic.stack import Stack

#opens file_name to be read 
with open('file_name', 'r') as fh:
    content = fh.read().strip() 

def interCodeGen(infixexpr):    
    prec = {}               
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Stack()       				#create stack to house operations in
    postfixList = []        
    tokenList = infixexpr.split()       	

    for token in tokenList:             
        if token.isnumeric():           
            postfixList.append(token)   
        elif token == '(':            
            opStack.push(token)         
        elif token == ')':              
            topToken = opStack.pop()    
            while topToken != '(':      
                postfixList.append(topToken)    
                topToken = opStack.pop()    
        else:
        	#while the stack is not empty, and the precedence of the next operator is higher or equal to the precedence of our current token                            
            while (not opStack.isEmpty()) and (prec[opStack.peek()] >= prec[token]):        
            opStack.push(token)        														
                  postfixList.append(opStack.pop())     

    while not opStack.isEmpty():        	#push the remaining operators onto postfixlist
        postfixList.append(opStack.pop())  
    return " ".join(postfixList)            

print(interCodeGen(content))                #print the generated intermediate code 