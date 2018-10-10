# bruteforce sha1 hashed password from 8 numbers

import hashlib


#print(m.hexdigest())
hash = "6ddc3c39fbe045ad9712232e48c4c9a6c4053a0a"

for i in range(0,99999999):
    m=hashlib.sha1()
    s=str(i)
    if len(s)<8:
        s="0"*(8-len(s))+s
    if i%1000000==0:
        proc=s
        print(proc[0]+proc[1])
    #print(s)
    m.update(bytes(s))
    hashM = m.hexdigest()
    #print(s+"    "+hashM)
    if hashM==hash:
        print(s+"     "+hash+"     "+hashM)
        break
