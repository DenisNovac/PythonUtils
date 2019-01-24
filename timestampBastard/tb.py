import sys
from datetime import datetime, timedelta
from filetimes import dt_to_filetime, utc

mode=0 # режим работы утилиты
statistics = [] # массив для накопления статистики

# метод переводит то, что мы считаем временной отметкой
# в собственно дату
def calculateDate(eightBytes):
    global statistics
    # отметки читаются справа-налево, поэтому разворачиваем массив
    copyForReverse=eightBytes.copy()
    copyForReverse.reverse()

    stringOfBytes=""
    for element in copyForReverse:
        element=element[2:]
        if len(element)<2: element="0"+element
        stringOfBytes=stringOfBytes+element
    # массивы прошедшие сюда скорее всего не будут вызывать эксепт
    try:
        us = int(stringOfBytes,16) / 10.
        calculate = datetime(1601,1,1) + timedelta(microseconds=us)
        statistics.append(calculate)
        print(calculate)
    except OverflowError: pass


# основная процедура программы
# идея: побайтово читаем двоичный файл, заполняя массив
# если накопилось восемь байтов в массиве, проверяем, является ли он отметкой
# если да, то полностью начинаем массив заново
# если нет, то сдвигаем его на один элемент вправо
def timestampGatherer():
    global mode
    global statistics
    maxYear=0
    minYear=0
    #maxMonth=0
    #minMonth=0
    maxOffset=-12345
    filepath=""

    # разбираем аргументы исходя из выбранного режима
    if mode==1:
        print("Режим 1: поиск с точностью до года")
        maxYear=int(sys.argv[2])
        maxYear = dt_to_filetime(datetime(int(maxYear), 1, 1, 0, 0, tzinfo=utc))
        minYear=int(sys.argv[3])
        minYear = dt_to_filetime(datetime(int(minYear), 1, 1, 0, 0, tzinfo=utc))
        filepath=sys.argv[4]
        if len(sys.argv)==6: maxOffset=int(sys.argv[5],16)

    if mode==2:
        print("Режим 2: поиск с точностью до месяца")
        maxYear=int(sys.argv[2])
        maxMonth=int(sys.argv[3])
        maxYear = dt_to_filetime(datetime(int(maxYear), int(maxMonth), 1, 0, 0, tzinfo=utc))
        minYear=int(sys.argv[4])
        minMonth=int(sys.argv[5])
        minYear =  dt_to_filetime(datetime(int(minYear), int(minMonth), 1, 0, 0, tzinfo=utc))
        filepath=sys.argv[6]
        if len(sys.argv)==8: maxOffset=int(sys.argv[7],16)

    if maxOffset!=-12345:
        print("Максимальное смещение, в байтах: "+str(maxOffset))
    # В этот момент у нас есть десятичные представления временных отметок
    # Windows. Однако, они слишком большие, для сравнения с ними нужно считать
    # много байт. Обрежем их так, чтобы проверять только три байта за раз
    # отрезаем первые три байта
    maxYear=hex(maxYear)[:7]
    minYear=hex(minYear)[:7]

    # переводим в десятичное число, выходит на несколько порядков меньше,
    # чем оригинальная временная отметка
    maxYear=int(maxYear,16)
    minYear=int(minYear,16)

    offset=-16 # первые 16 байтов на нулевом смещении, а не на 16
    eightBytes = [ ]
    file = open(filepath,"rb")
    for bytes in file:
        for byte in bytes:
            if maxOffset==offset: break
            if len(eightBytes) == 8: # массив забился
                # Последние три байта в обратном порядке отвечают за год
                # и за месяц
                yearBytes=""
                firstByte=eightBytes[7][2:]
                secondByte=eightBytes[6][2:]
                thirdByte=eightBytes[5][2:]
                # Дописываем нули в начало, если не хватает
                if len(firstByte)<2: firstByte="0"+firstByte
                if len(secondByte)<2: secondByte="0"+secondByte
                if len(thirdByte)<2: thirdByte="0"+thirdByte

                yearBytes=firstByte+secondByte+thirdByte
                year=int(yearBytes,16)
                # сравниваем значение последних двух байт с границами
                if year>minYear and year<maxYear:
                    print(hex(offset))
                    calculateDate(eightBytes)
                    eightBytes = [ ] # временные отметки не могут пересекаться
                # иначе не очищаем массив, а сдвигаем и дополняем на один байт
                else: eightBytes.pop(0)
            eightBytes.append(hex(byte))
            offset=offset+1
        if maxOffset==offset: break
    file.close()
    print()
    statisticsToFile()


def statisticsToFile():
    global statistics
    statistics.sort()
    with open ("statistics.csv","w") as outputfile:
        outputfile.write("Год,Месяц,День,Час,Минута\n")
        for entry in statistics:
            print(entry)
            csvstr = datetime.strftime(entry, '%Y, %m, %d, %H, %M')
            outputfile.write(csvstr+"\n")

def printHelp():
    print ("*** TIMESTAMP BASTARD ***")
    print ("Утилита поиска временных отметок в файлах и составления статистики")
    print ("После завершения сбора временных отметок программа автоматически создаст файл statistics.csv, который удобно исследовать")
    print ()
    print ("Использование:")
    print ("python3 tb.py [РЕЖИМ] [КОНЕЧНЫЙ ГОД ПОИСКА] <месяц> [НАЧАЛЬНЫЙ ГОД ПОИСКА] <месяц> [ПУТЬ К ФАЙЛУ] <граница>")
    print ()
    print ("Режимы:")
    print ("1 - Режим с точностью до года (не требует указания месяца)")
    print ("2 - Режим с точностью до месяца (требует указания месяца)")
    print ()
    print ("Граница - если необходимо просматривать не весь файл, а только его часть.")
    print ("Нужно указать шестнадцатеричное число")
    print ()
    print ("Программные требования:")
    print ("Python 3")
    print ("Библиотека filetimes.py (в комплекте)")
    print ()
    print ("Дисклеймер: скорее всего программа найдет больше временных отметок, чем есть на самом деле. Это происходит по причине случайности двоичной информации, из которой состоят шифрованные файлы, сжатые файлы, изображения.")

def main():
    global mode

    if len(sys.argv)<2:
        printHelp()
        exit()
    if sys.argv[1]=="1" and len(sys.argv)<7 and len(sys.argv)>4:
        mode=1
        timestampGatherer()
    else:
        if sys.argv[1]=="2" and len(sys.argv)<9 and len(sys.argv)>6:
            mode=2
            timestampGatherer()
        else:
            printHelp()
            exit()

main()
