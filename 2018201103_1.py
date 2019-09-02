import sys

transactions = {}
variables_disk = {}
variables_memory = {}
len_of_trans = {}
order_of_trans = []
done_dict = {}
temp_var_map = {}
temp_var = {}

def operate(a, b, op):
    if op=='+':
        return a+b
    if op=='-':
        return a-b
    if op=='*':
        return a*b
    if op=='/':
        return float(a)/float(b)

def print_values_in_memory():
    s = ""
    for i in sorted(variables_memory):
        # print i,variables_memory[i],
        s+=i+" "+str(variables_memory[i])+" "
    # print
    s=s[:-1]
    output_file.write(s+"\n")

def print_values_in_disk():
    s = ""
    for i in sorted(variables_disk):
        # print i,variables_disk[i],
        s+=i+" "+str(variables_disk[i])+" "
    # print
    s=s[:-1]
    output_file.write(s+"\n")

def perform_log(cur_transaction,x,start_from):
    if start_from >= len_of_trans[cur_transaction]:
        done_dict[cur_transaction]=True
        return
    instructions = transactions[cur_transaction]
    instructions = instructions[start_from:start_from+x]
    # print cur_transaction,": ", instructions
    # print
    if start_from==0:
        # print "<START",cur_transaction+">"
        output_file.write("<START "+cur_transaction+">"+"\n")
        print_values_in_memory()
        print_values_in_disk()
    
    for line in instructions:
        line = line.strip()
        line = line.replace(" ","")
        if line.split("(")[0] == "READ":
            # print line
            var = line[line.find("(")+1:line.find(",")]
            value = line[line.find(",")+1:line.find(")")]
            # print var,value
            if var not in temp_var_map.keys():
                temp_var_map[var] = value
                temp_var[value] = variables_disk[var]
                variables_memory[var] = variables_disk[var]
            else:
                temp_var[value] = variables_memory[var]
                temp_var_map[var] = value
        elif line.split("(")[0] == "WRITE":
            # print "write ",line
            var = line[line.find("(")+1:line.find(",")]
            value = line[line.find(",")+1:line.find(")")]
            # print var,value
            # print "before ",variables_memory
            # print "<",cur_transaction,var,variables_memory[var],">"
            output_file.write("<"+cur_transaction+", "+var+", "+str(variables_memory[var])+">"+"\n")
            variables_memory[var] = int(temp_var[value])
            print_values_in_memory()
            print_values_in_disk()
            # print "after ",variables_memory
        elif line.split("(")[0] == "OUTPUT":
            # print "output ", line
            var = line[line.find("(")+1:line.find(")")]
            variables_disk[var]=variables_memory[var]
        else:
            # print "else ", line
            var1 = line[0:line.find(":")]
            op = None
            if '+' in line:
                op='+'
            elif '-' in line:
                op='-'
            elif '*' in line:
                op='*'
            elif '/' in line:
                op='/'

            var2 = line[line.find("=")+1:line.find(op)]
            val = line[line.find(op)+1:]
            # print var1,var2,val
            temp_var[var1] = operate(temp_var[var2],int(val),op)
            # print temp_var[var1]
    if start_from+x >= len_of_trans[cur_transaction]:
        # print "<COMMIT",cur_transaction,">"
        output_file.write("<COMMIT "+cur_transaction+">"+"\n")
        print_values_in_memory()
        print_values_in_disk()
    # print_values_in_memory()
    # print_values_in_disk()

def undo_logs(x):
    i=0
    cur_transaction = order_of_trans[i]
    start_from=0
    while True:
        perform_log(cur_transaction,x,start_from)
        i+=1
        # print cur_transaction,x,start_from,i
        if i%len(transactions) == 0:
            start_from+=x
            i=0
        cur_transaction = order_of_trans[i]

        false_count = 0
        for key,val in done_dict.iteritems():
            if val==False:
                false_count+=1
        if false_count == 0:
            break

def read_file(input_file):
    line_no = 1
    transaction_no = None
    for line in open(input_file):
        if line_no == 1:
            variables = line.split()
            for i in xrange(len(variables)):
                if i%2==0:
                    variables_disk[variables[i]] = int(variables[i+1])
        elif line.split(" ")[0][0] == 'T':
            ls = line.split(" ")
            transaction_no = ls[0]
            order_of_trans.append(transaction_no)
            len_of_trans[transaction_no] = int(ls[1])
            transactions[transaction_no] = list()
        elif line.split("(")[0] == "READ":
            transactions[transaction_no].append(line[:-1])
        elif line.split("(")[0] == "WRITE":
            transactions[transaction_no].append(line[:-1])
        elif line.split("(")[0] == "OUTPUT":
            transactions[transaction_no].append(line[:-1])
        elif not line.strip():
            transaction_no = None
        else:
            transactions[transaction_no].append(line[:-1])
        line_no+=1

    for i in transactions.keys():
        done_dict[i]=False



input_file = sys.argv[1]
x = int(sys.argv[2])

read_file(input_file)

output_file = open("2018201103_1.txt","w") 
undo_logs(x)
output_file.close()