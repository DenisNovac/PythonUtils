# bruteforces file of hashes from one letter


import hashlib

alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,_-;{}[]"


with open("hashes.txt") as f:
    for line in f:
        #print(line, end='')
        for c in alphabet:
            s=hashlib.md5()
            s.update(bytes(c,"utf-8"))
            dig=s.hexdigest()
            #print(type(dig))
            #print(c+"]      ["+dig+"]     ["+line)
            if ((dig+"\n")==line): print(c, end='')
print()
