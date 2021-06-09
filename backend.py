import csv
import time

#file bertipe FileStorage
def fileStorageToText(file):

    rawText = file.read()
    retText = rawText.decode('utf-8')
    
    return retText
    

def parser(text):
    retArray = []
    tempArray = []
    tempString = ""
    for char in text:
        if (char==','):
            tempArray += [tempString]
            tempString = ""     #reset
        elif (char=='\r' or char=='|'):
            tempArray += [tempString]
            retArray += [tempArray]
            tempArray = []      #reset
            tempString = ""
        elif (char=='\n'):
            tempString          #doNothing
        else:
            tempString += char
    tempArray += [tempString]
    retArray += [tempArray]
    
    return retArray

def arrayToText(arrayOfCSV):
    retText = ""
    for i in range (len(arrayOfCSV)):
        for j in range (len(arrayOfCSV[i])):
            
            retText += arrayOfCSV[i][j]
            if (j != len(arrayOfCSV[i]) - 1):
                retText += ','
        if (i != len(arrayOfCSV) - 1):
            retText+='|'
    
    return retText        

#Fungsi yang mensort array dengan algoritma selection menjadi terurut sesuai order dan berdasarkan kolom column_specifier
def sort_selection(array,column_specifier,order):
    
    start_time = time.clock()
    if (column_specifier>len(array[0])):
        return None         #error
    else:
        if (order=="asc"):
            for i in range (1,len(array)):
                min = (array[i],i)            #tuple untuk menyimpan nilai dan posisi dari minimum value
                for j in range (i+1,len(array)):
                    if (array[j][column_specifier] < min[0][column_specifier]):
                        min = (array[j],j)
                
                tempVal = array[i]
                array[i] = min[0]
                array[min[1]] = tempVal

        elif (order=="desc"):
            for i in range (1,len(array)):
                max = (array[i],i)            #tuple untuk menyimpan nilai dan posisi dari minimum value
                for j in range (i+1,len(array)):
                    if (array[j][column_specifier] > max[0][column_specifier]):
                        max = (array[j],j)
                
                tempVal = array[i]
                array[i] =  max[0]
                array[max[1]] = tempVal

        retTime = time.clock() - start_time
        
        return (array, "%.7f" % retTime)

#Fungsi yang mensort array dengan algoritma mergesort menjadi terurut sesuai order dan berdasarkan kolom column_specifier        
def sort_merge(array,column_specifier,order):
    start_time = time.clock()
    if (column_specifier>=len(array[0])):
        return None         #error
    
    else:
        retTime = time.clock() - start_time
        return ([array[0]] + merge(array[1:len(array)],column_specifier,order), "%.7f" % retTime)

def merge(array,column_specifier,order):
    if (len(array)==1):
        return [array[0]]
    else:
        n = len(array)
        half = n//2 - 1

        leftArray = merge(array[0:(half+1)],column_specifier,order)
        rightArray = merge(array[(half+1):len(array)],column_specifier,order)

        retArray = []
        i = 0
        j = 0
        if (order=="asc"):
            while (i!=len(leftArray) or j!=len(rightArray)):
                if (j==len(rightArray) ):
                    retArray += [leftArray[i]]
                    i+=1
                elif (i==len(leftArray)):
                    retArray += [rightArray[j]]
                    j+=1
                elif (leftArray[i][column_specifier] <= rightArray[j][column_specifier]):
                    retArray += [leftArray[i]]
                    i+=1
                elif (leftArray[i][column_specifier] > rightArray[j][column_specifier]):
                    retArray += [rightArray[j]]
                    j+=1
        elif (order=="desc"):
            while (i!=len(leftArray) or j!=len(rightArray)):
                if (j==len(rightArray) ):
                    retArray += [leftArray[i]]
                    i+=1
                elif (i==len(leftArray)):
                    retArray += [rightArray[j]]
                    j+=1
                elif (leftArray[i][column_specifier] >= rightArray[j][column_specifier]):
                    retArray += [leftArray[i]]
                    i+=1
                elif (leftArray[i][column_specifier] < rightArray[j][column_specifier]):
                    retArray += [rightArray[j]]
                    j+=1
        
        return retArray

#fungsi yang membersihkan table dari data-data tidak valid
def preprocessTable(rawTable):
    #asumsi row pertama dari rawTable typenya pasti benar
    columnTypeNumeric = [ord(rawTable[1][0][0])<58, ord(rawTable[1][1][0])<58, ord(rawTable[1][2][0])<58]

    #dibuat array sementara untuk menyimpan index mana saja yang akan dihapus
    indexWillBeDeleted = []

    for i in range(1,len(rawTable)):
        for j in range(len(rawTable[i])):
            if (ord(rawTable[i][j][0]) < 58 and not columnTypeNumeric[j]):      #nilai cell numeric padahal column bertipe text
                indexWillBeDeleted += [i]
            elif (ord(rawTable[i][j][0]) > 58 and columnTypeNumeric[j]):        #nilai cell text padahal column bertipe numeric
                indexWillBeDeleted += [i]

    for i in range (len(indexWillBeDeleted)):
        del rawTable[indexWillBeDeleted[i]]
        for j in range (i+1,len(indexWillBeDeleted)):
            indexWillBeDeleted[j] -= 1

