# генератор рассматривает все возможные числа N, для которых деление с
# остатком на D дает остаток R

# каждый символ файла - это X = (c + c % key)
# X может быть любым, т.к. шифрован, но c - это буквы латиницы или кириллицы
# python работает с UTF-8

# латиница 65-90, 97-122
# кириллица 1042-1103
# служебка 32-64

#c+c%key = 423

numGen(144,1)

def numGen(cypheredChar,key):
    answer=None
    X=cypheredChar
    counter=0

    for i in range(32,64):
        check=i+i%key
        if check==X:
            answer=i
            print(answer)
            counter+=1

    for i in range(65,122):
        check=i+i%key
        if check==X:
            answer=i
            print(answer)
            counter+=1

    for i in range(1042,1103):
        check=i+i%key
        if check==X:
            answer=i
            print(answer)
            counter+=1

    for i in range(32,64):
        check=i+i%key
        if check==X:
            answer=i
            print(answer)
            counter+=1
    return counter
