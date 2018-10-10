#for i in range(1,984):
    #with open("bin") as f:
        #key=i
        #name="file"+str(key)+"-"
        #with open(name)
            #for line in f:
                #for c in line:
                    #key=key+1
                    #добавить в result число (ord(c) + (ord(c) % key))

# actually this code is bad:
# it uses only english alphabet, which codes are 65-90, 97-122 and
# special symbols 32-64
# but for A, B:
# if B>A then A mod B = A
# so here: ord(c) + ord(c) % key
# its just doubles

#from numbersGenerator import numGen

with open("bin") as f:
    for line in f:
        print(line)



for i in range(1,985):
    key = i
    name = "file"#+str(key)
    num=""

    with open("bin") as input, open(name,"w") as output:
        lineout=""
        for line in input:
            print("key is:"+str(key))
            for ch in line:
                if ch==' ':
                    # logic start

                    cyp=int(num)
                    #mes=numGen(cyp,key)
                    print(str(mes)+"   ",end='')
                    #if mes is None: continue
                    #print(mes)
                    #lineout+=chr(mes)
                    # logic end
                    num=""
                    continue
                num+=ch
            print()
        print(lineout)
