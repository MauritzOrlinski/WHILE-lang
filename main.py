import re
import sys

prgm = ""
if len(sys.argv) < 2:
    raise Exception("No file given")
elif re.match(r"[\/a-zA-Z0-9\_\-]*\.while", sys.argv[1]) is None:
    raise Exception("Not a .while program file")
with open(sys.argv[1], "r") as f:
    prgm = f.read().lower()
prgm = re.sub(r"(\(\*[\s\n\<\>\*\=a-z\_0-9A-Z]*\*\))|\s|\n", "", prgm)
prgm = re.sub(r"\!=0do|==0then", ";", prgm)
ps = prgm.replace("else", "else;").replace("end", "end;").split(";")
state = {}
stack = []


def check_var(var, line):
    if var not in state:
        raise Exception(f"Error: {var} not defined in statement {line}")


def check_while(var, line):
    check_var(var, line)
    return state[var] != 0


pc = 0
i = ""
while pc < len(ps):
    i = ps[pc]

    # Next line is an assignment
    if re.match(r"[a-z][a-z\_0-9]*\=-?([1-9][0-9]*|0)", i) is not None:
        exp = i.split("=")
        state[exp[0]] = int(exp[1])
    # Next line is an assignment with operation
    elif (
        re.match(r"[a-z][a-z\_0-9]*\=[a-z][a-z\_0-9]*[\+\*\\\-\%][a-z][a-z\_0-9]*", i)
        is not None
    ):
        exp = i.split("=")
        m = re.match(r"([a-z][a-z\_0-9]*)([\+\*\\\-\%])([a-z][a-z\_0-9]*)", exp[1])
        if m:
            var1, op, var2 = m.groups()
            check_var(var1, pc)
            check_var(var2, pc)
            a = state[var1]
            b = state[var2]
            if op == "/":
                state[exp[0]] = a / b
            elif op == "%":
                state[exp[0]] = a % b
            elif op == "-":
                state[exp[0]] = a - b
            elif op == "+":
                state[exp[0]] = a + b
            elif op == "*":
                state[exp[0]] = a * b
        else:
            raise Exception("Syntax Error: No valid Operation")
    # Next line is a while loop
    elif re.match(r"while[a-z][a-z\_0-9]*", i) is not None:
        var = i.replace("while", "")
        if check_while(var, pc):
            stack.append((var, pc))
        else:
            indent = 0
            pc += 1
            while i != "end" or indent > 0:
                if re.match("while", i) is not None or re.match("if", i) is not None:
                    indent += 1
                if i == "end":
                    indent -= 1
                pc += 1
                i = ps[pc]
    # Next line is a if statement
    elif re.match(r"if[a-z][a-z\_0-9]*", i):
        stack.append("if")
        var = i.replace("if", "")
        check_var(var, pc)
        if state[var] != 0:
            prev_pc = pc
            pc += 1
            d = 1
            while pc < len(ps) and d > 0:
                if re.match(r"if[a-z][a-z\_0-9]*", ps[pc]) is not None:
                    d += 1
                elif ps[pc] == "else":
                    d -= 1
                pc += 1
            if pc == len(ps):
                raise Exception(
                    f"Syntax Error: The if ... then in statement {prev_pc} is missing an else"
                )
            continue
        else:
            pass
    # Next line is a print statement
    elif re.match(r"\>[a-z][a-z\_0-9]*\<", i) is not None:
        payload = i.replace(">", "").replace("<", "")
        check_var(payload, pc)
        print(state[payload])
    # Next line is end of a previous statement
    elif i == "end":
        if stack[len(stack) - 1] != "if" and check_while(stack[len(stack) - 1][0], pc):
            pc = stack[len(stack) - 1][1]
        else:
            stack.pop()
    # Next line is an else
    elif i == "else":
        prev_pc = pc
        pc += 1
        while pc < len(ps) and ps[pc] != "end":
            pc += 1
        stack.pop()
        if pc == len(ps):
            raise Exception(
                f"Syntax Error: The else in statement {prev_pc} is missing an end"
            )
    # We allow empty lines
    elif i == "":
        pass
    else:
        raise Exception(f"unsuported op: {i}")
    pc += 1
