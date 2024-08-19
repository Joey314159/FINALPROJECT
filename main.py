import re

state = dict()#Creates an empty dictionary set as a global variable

def varmap(targetVar, state):#varmap function takes in 2 arguments, the variable name, and the dictionary representing the values it holds
    if targetVar in state:#Checking to see if the variable exists in the state dictionary
        return state[targetVar]#If it does exist, then we return it
    else:
        raise ValueError("Error: Var not found")#If it doesn't exist this is what we return

def executeProgram(program):#Takes in our program
    linesInProgram = program.splitlines()#Need to know how many lines are in my program
    linesInProgram = list(linesInProgram)
    for linenum, line in enumerate(linesInProgram):#Splitting our program into separate lines, which are operations

        instruction, expression = line.split(maxsplit=1)#Splitting the operations/lines into 2 parts, instruction and expression
        
        if instruction == "♒":#ASSIGN Checking to see what instruction we gave it
            setValue(expression)
        elif instruction == "✍️":#PRINT, allows us to display to the terminal
            try:
                outputValue(expression)#that will be placed inside of val, which is then printed
            except:
                print("Error: Val not found")
        elif instruction == "🤓": #COMPUTE, this emoji allows us to do arithmatic
            try:
                var,eq1 = expression.split('=')#EX: A = B + C, "A" will be split up from "B+C"
                val = mathFunc(eq1)             #Returning the value when we do B+C
                state[var] = val                #Now we set "A" with that value
                print(var + ' = '+ str(state[var]))               #Displaying the value
            except:
                print("Not possible")
        elif instruction == "🤷‍♂️":#COMPARE, 🤷‍♂️
            try:
                x = compare(expression)
                if(x == True):
                    print("👍")
                elif(x == False):
                    print("👎")
            except:
                print("Comparison not available")
        elif instruction == "👉:":#FOR-LOOP
            try:
                endOfFor = 0
                var, myRange = expression.split("=")# Splitting the expression up in pieces
                start_val, stop_val = myRange.split(",")#Holds teh range of the for-loop
                state[var] = start_val#Setting our variable with our starting value
                for i in range(linenum+1, len(linesInProgram)):
                    scanLine = linesInProgram[i]
                    if "⏭️" in scanLine:#NEXT
                        endOfFor = i#Holds the first occurence of the end of the body
                        break
                for x in range(int(start_val), int(stop_val)+1):
                    state[var] = x
                    for_body = linesInProgram[linenum+1:endOfFor]#This holds your for-loop body as an array
                    newProgram = ";".join(for_body)#newProgram joins all of your loop body in a string
                                                   #This is needed since our executeProgram takes in a string
                    if(len(for_body) > 1):
                        for statement in for_body:
                            statement = statement.replace(";","")
                            executeProgram(statement)
                    else:
                        newProgram = newProgram.replace(";","")#We remove the ";" for an empty space
                        executeProgram(newProgram)
            except:
                print("Error! Instruction not found")
        elif instruction == "⏭️":
            continue
        elif instruction == "👈:":
            continue  # ELSE is handled directly after an IF, do nothing if encountered separately
        elif instruction == "WHILE":
            try:
                y = compare(expression)#This returns a boolean, which y holds
                while True:
                    whileLoop(expression, linesInProgram)#An array containing the complete program
                    if y == False:
                        break
            except:
                print("Loop does not exist")
        elif instruction == "👌":
            try:
                condition, action = expression.split(':')
                valid = compare(condition)
                if valid:
                    executeProgram(action.strip())  # Execute inner program if condition is true
                else:
                    # Search for an ELSE following directly after this IF
                    for j in range(linenum + 1, len(linesInProgram)):
                        if linesInProgram[j].strip().startswith("👈:"):
                            else_line = linesInProgram[j].strip()
                            _, else_action = else_line.split(maxsplit=1)
                            executeProgram(else_action.strip())
                            linenum = j  # Skip the ELSE line in the main loop JUMP
                            break  # Exit the loop once ELSE is found
            except:
                print("Condition not applicable")
        else:
            print("Error! Instruction not found")#If the Instruction does not exit in our grammar than we throw this error message

def setValue(expression):
    var, val = expression.split('=')
    state[var] = val
    
def outputValue(expression):
    try:
        if "'" in expression:
            printed_string = expression.replace("'","")
            print(printed_string)
        else:
            val = varmap(expression, state)
            print(val)
    except:
        print("Error: Val not found")

def mathFunc(equation):#Takes in our equation equation as an argument
    symbols = {'+': 'add', '-':'sub', '*':'mult', '/': 'div', '%':'mod'}#Creating a list of operations that can be made

    for operator in symbols.keys():
        if operator in equation:#Checking to see if the operator exists in our equation
            leftHand, rightHand = equation.split(operator)#If it does exist, then we split up both sides

            match operator:#Matching the operator once more to see what operation is to be performed
                case '+':
                    return mathFunc(leftHand) + mathFunc(rightHand)
                case '-':
                    return mathFunc(leftHand) - mathFunc(rightHand)
                case '*':
                    return mathFunc(leftHand) * mathFunc(rightHand)
                case '/':
                    return mathFunc(leftHand) / mathFunc(rightHand)
                case '%':
                    return mathFunc(leftHand) % mathFunc(rightHand)

    result = 0#Making the result start off with 0
    try:
        result = int(equation)
    except:#If we get a variable, then we need to search up it's value
        equation = varmap(equation,state)#We hold the value in our equation
        result = int(equation) + result#We add that value to our result
    finally:
        return result#Lastly we return the result

def whileLoop(statement, someProgram):
    iterator, end = statement.split('<')
    loopVar = varmap(iterator, state)

    bodyOfLoop = ""
    linesInProgram = len(someProgram)-1
    for i in range(linesInProgram):
        currentLine = someProgram[i]
        nextLine = someProgram[i+1]    

def compare(conditionalStatement):
    compOperations = {'<':'lessThan', '>':'greaterThan', '==':'equalTo'}

    for compSymbol in compOperations.keys():
        if compSymbol in conditionalStatement:
            leftHand, rightHand = conditionalStatement.split(compSymbol)

            size = len(leftHand)
            if leftHand.isdigit():#Takes care of 3<4, or b<5, or b*3<90, or b*b<90
                leftHand = leftHand
            else:
                leftHand = varmap(leftHand, state) if size == 1 else mathFunc(leftHand)#Grabbing the value of our variable
            
            rightHand = rightHand if rightHand.isdigit() else varmap(rightHand, state)#Takes care of the right hand being a digit or a variable

            match compSymbol:
                case '<':
                    return int(leftHand) < int(rightHand)
                case '>':
                    return int(leftHand) > int(rightHand)
                case '==':
                    return int(leftHand) == int(rightHand)

    
sampleProgram = """♒ 😪=90
♒ 🐣=20
👉: 🐔=1,5
✍️ 🐔
🤓 🎈=😪-🐣 
✍️ 😪
✍️ 🐣
✍️ 🎈
⏭️ 🐔
♒ 💎=30
✍️ 💎
"""

executeProgram(sampleProgram)