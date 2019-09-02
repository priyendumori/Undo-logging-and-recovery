import sys

variables_disk = {}
logs = []
start_ckpt_line_no = -1
end_ckpt_line_no = -1

def undo_all():
    global logs
    l = logs[::-1]
    commited = []
    for line in l:
        if line[0]=='T':
            s = line.replace(" ","").split(",")
            # print s,commited
            if s[0] not in commited:
                # print "making ",s[1],s[2],"by",s[0]
                variables_disk[s[1]] = int(s[2])
        elif line.split(" ")[0]=="COMMIT":
            commited.append(line.split(" ")[1])

def undo_only_start_present():
    global logs
    l = logs[start_ckpt_line_no]
    ts = l[l.find("(")+1:l.find(")")].replace(" ","").replace(","," ")
    trans_active_at_ckpt = ts.split(" ")
    
    commited = []
    lg = logs[::-1]
    for line in lg :
        if len(trans_active_at_ckpt)==0:
            break
        if line[0]=='T':
            s = line.replace(" ","").split(",")
            # print s,commited
            if s[0] not in commited:
                # print "making ",s[1],s[2],"by",s[0]
                variables_disk[s[1]] = int(s[2])
        elif line.split(" ")[0]=="COMMIT":
            commited.append(line.split(" ")[1])
        elif line.split(" ")[0]=="START":
            ls = line.split(" ")
            if ls[1]!="CKPT":
                if ls[1] in trans_active_at_ckpt:
                    trans_active_at_ckpt.remove(ls[1])

def undo_end_present():
    global logs
    l = logs[start_ckpt_line_no+1:]
    l = l[::-1]

    commited = []
    for line in l:
        if line[0]=='T':
            s = line.replace(" ","").split(",")
            # print s,commited
            if s[0] not in commited:
                # print "making ",s[1],s[2],"by",s[0]
                variables_disk[s[1]] = int(s[2])
        elif line.split(" ")[0]=="COMMIT":
            commited.append(line.split(" ")[1])

def do_recovery():
    global start_ckpt_line_no
    global end_ckpt_line_no

    if start_ckpt_line_no > end_ckpt_line_no:
        end_ckpt_line_no = -1

    if start_ckpt_line_no==-1 and end_ckpt_line_no==-1:
        # print "no ckpt"
        undo_all()
    elif start_ckpt_line_no!=-1 and end_ckpt_line_no==-1:
        # print "start ckpt"
        undo_only_start_present()
    elif start_ckpt_line_no==-1 and end_ckpt_line_no!=-1:
        print "end ckpt found without start ckpt"
    elif start_ckpt_line_no!=-1 and end_ckpt_line_no!=-1:
        # print "both "
        undo_end_present()

def read_file(input_file):
    global start_ckpt_line_no
    global end_ckpt_line_no
    line_no = 1
    transaction_no = None
    for line in open(input_file):
        if line_no == 1:
            variables = line.split()
            for i in xrange(len(variables)):
                if i%2==0:
                    variables_disk[variables[i]] = int(variables[i+1])
        else:
            if line.strip():
                logs.append(line[1:-2])
                # print line
                if line.find("START")!=-1 and line.find("CKPT")!=-1:
                    start_ckpt_line_no = line_no - 3

                if line.find("END")!=-1 and line.find("CKPT")!=-1:
                    end_ckpt_line_no = line_no - 3
        line_no+=1

    # print variables_disk
    # print logs
    # print start_ckpt_line_no, end_ckpt_line_no

def write_output():
    s = ""
    for i in sorted(variables_disk):
        s+=i+" "+str(variables_disk[i])+" "
    s=s[:-1]
    output_file.write(s+"\n")

input_file = sys.argv[1]
read_file(input_file)
do_recovery()

output_file = open("2018201103_2.txt","w")
write_output()
output_file.close()