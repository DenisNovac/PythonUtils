# erases all spaces in file (file will be uploaded to RAM)

filename="a"
num=""
with open(filename) as f:
    for line in f:
        for ch in line:
            if ch==' ':
                #o.write(num)
                #num=""
                continue
            num+=ch
with open(filename,"w") as f:
    f.write(num)
