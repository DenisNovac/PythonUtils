# bruteforces private keys from superkey

q=1357
g=10
A=419
B=34
K=33
#print(pow(g,2))
print(pow(65537,-1))
a=0
b=0
found=False
for a in range(1,1000):
    print(str(a))
    answer=0
    for b in range(1,1000):
        if pow(B,a)%q == K and pow(A,b)%q == K:
            found=True
            break
        #this one is really long
        #answer=pow(g,a*b)%q
        #if (answer==g_ab) and (pow(g,a)%q==A) and (pow(g,b)%q==B):
            #print(pow(g,a)%q)
            #print(pow(g,a*b)%q)
            #found=True
            #break
    if found: break
print()
print("Bruteforced!")
print(str(a)+" "+str(b))
