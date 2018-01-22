#!/usr/bin/python
#imports
import sys
from sets import Set
import numpy as np

# main con casos de prueba simple
def main():

    morseAPI = MorseAPI()
    #test_string = '1101101100111'+'00000'+'1111110001111111100111111'+'00000'+'11101111111101110111'+'0000'+'11000111111'+'00000000'+'11111100111111'+'00000'+'1100001101111111101110111'+'000000'+'1101110'
    slow = "000000000000011111110000111111000011111000011111110000000000111111111111110000111111111110000011111111110000000011111100000111111111111000011111000111111000000000011111100001111111111111000000000000000000000001111111111000011111111110000000001111100000000011111100000111111111100011111000011111000000000011111000001111100000000000"
    medium = "00000000110110110011100000111111000111111001111110000000111011111111011101110000000110001111110000000001111110011111100000001100000110111111110111011100000011011100000000000"
    fast = "000000101011001100000111100111100111110000101111100110110000010011110000000111100111110001000011011111011010000110100000000000"


    print "Se testean diferentes velocidades para un mismo mensaje..."

    print "-------------- SLOW -----------------"
    morseAPI.testApi(slow)
    print "-------------- MEDIUM -----------------"
    morseAPI.testApi(medium)
    print "-------------- FAST -----------------"
    morseAPI.testApi(fast)
    ## testeo la api con una cadena binaria basica
    #morseAPI.testApi(test_string)


class MorseAPI():
    """docstring for Morse."""

    table = {'.-':'A','-...':'B','-.-.':'C',
    '-..':'D','.':'E','..-.':'F',
    '--.':'G','....':'H','..':'I',
    '.---':'J','-.-':'K','.-..':'L',
    '--':'M','-.':'N','---':'O',
    '.--.':'P','--.-':'Q','.-.':'R',
    '...':'S','-':'T','..-':'U',
    '...-':'V','.--':'W','-..-':'X',
    '-.--':'Y','--..':'Z','-----':'0',
    '.----':'1','..---':'2','...--':'3',
    '....-':'4','.....':'5','-....':'6',
    '--...':'7','---..':'8','----.':'9'}
    
    inverseTable = {v : k for k, v in table.iteritems()}

    def __init__(self):
            pass

    def testApi(self,test_string):

        repArray = self.repeticionList(test_string)

        minmaxarray = self.minMax(test_string)

        ceros13 = (minmaxarray[0] + minmaxarray[1])/3
        ceros23 = (minmaxarray[0] + minmaxarray[1])*2/3
        oneAvgLen = (minmaxarray[2] + minmaxarray[3]) / 2

        print "average de unos : " + str(oneAvgLen) + "| 1/3 de ceros : " + str(ceros13) + " | 2/3 de ceros :" + str(ceros23)

        ## testeo del metodo que convierte la entrada de bits en morse
        morse = self.decodeBits2Morse(test_string)
        print "codigo morse : " + morse

        ## testeo el conversor de morse a palabras humanas
        human = self.translate2Human(morse)
        print "palabras traducidas : " + human

        ## testeo el conversor inverso a morse
        morse = self.translate2Morse(human)
        print "conversion inversa : " + morse + "EOS"


    # uso strings para codificar 0 y 1 podria ser bits pero es mas facil para debugguear
    def decodeBits2Morse(self,bits_array):
        # asumo que tengo almenos un punto y una raya en la cadena, sino debo primero pedir al menos uno de ambos para sincronizarme.
        # busco la maxima y minima repeticion de unos
        # luego tomo el promedio y separo las longitudes, si es menor al promedio es punto sino es raya
        # con los ceros debo hacer tres clasificaciones, entonces separo en tercios y voy a clasificar de menor a mayor.
        # primer tercio : espacio entre punto o raya, segundo tercio : espacio entre caracteres y tercer tercio : espacio entre palabras
        morse = ''
        minmaxarray = self.minMax(bits_array)
        ceros13 = (minmaxarray[0] + minmaxarray[1])/3
        ceros23 = (minmaxarray[0] + minmaxarray[1])*2/3
        oneAvgLen = (minmaxarray[2] + minmaxarray[3]) / 2
        ones = 0
        ceros = 0
        for c in bits_array:
            if(c == '1'):
                ones+= 1
                if(ceros > 0):
                    if(ceros <= ceros13):
                        morse += ''
                    elif(ceros > ceros13 and ceros <= ceros23):
                        morse += ' '
                    else:
                        morse += '   '
                    ceros = 0
            else:
                ceros+= 1
                if(ones > 0):
                    if(ones <= oneAvgLen): # considero un punto
                        morse += '.'
                    else:
                        morse += '-'
                    ones = 0
        return morse

    # esta funcion me da la minima y maxima repeticion de ceros y unos (en ese orden)
    def minMax(self,bits_array):
        (ceroRepList,oneRepList) = self.repeticionList(bits_array)
        ## saco los outliers para tener mejores minimos y maximos
        ceroRepList = self.removeOutliers(ceroRepList)
        oneRepList = self.removeOutliers(oneRepList)
        print "cero list filtrada: " + str(ceroRepList)
        print "unos list filtrada: " + str(oneRepList)
        minCeros = ceroRepList[0]
        minOnes = oneRepList[0]
        maxCeros = ceroRepList[-1]
        maxOnes = oneRepList[-1]

        return [minCeros,maxCeros,minOnes,maxOnes]

    def removeOutliers(self,orderlist):
        q1 = np.median(orderlist[:int(len(orderlist)/2)])
        q3 = np.median(orderlist[int(len(orderlist)/2):])
        iqr = q3 - q1
        maxlimit = q3 + 1*iqr
        minlimit = q1 - 1*iqr
        orderlist = filter(lambda e: e > minlimit and e < maxlimit ,orderlist)
        return orderlist

    # esta funcion me da la lista de repeticiones de ceros y unos ordenada de menor a mayor
    def repeticionList(self,bits_array):
        ceroRepSet = Set()
        oneRepSet = Set()
        oneAcum = 0
        ceroAcum = 0

        for c in bits_array:
            if (c == '1'):
                oneAcum+= 1
                if(ceroAcum > 0):
                    ceroRepSet.add(ceroAcum)
                    ceroAcum = 0
            else:
                ceroAcum+= 1
                if(oneAcum > 0):
                    oneRepSet.add(oneAcum)
                    oneAcum = 0

        # la ultima parte la tengo que chequear aca
        if(oneAcum > 0):
            oneRepSet.add(oneAcum)
        if(ceroAcum > 0):
            ceroRepSet.add(ceroAcum)

        # ordeno y saco repetidos
        ceroRepList = list(ceroRepSet)
        ceroRepList.sort()
        oneRepList = list(oneRepSet)
        oneRepList.sort()

        return (ceroRepList,oneRepList)

    def translate2Human(self,morse_array):
        humanWords = ''
        words = morse_array.split('   ')
        for i,word in enumerate(words):
            if(word):
                letterList = word.split()
                for letter in letterList:
                    humanWords += self.morse2char(letter)
            if(i < len(words)-1):
                humanWords += ' '

        return humanWords



    def translate2Morse(self,words):
        # Lista de palabras
        wordList = words.split()
        morse = ''
        for i,word in enumerate(wordList):
            for j,letter in enumerate(word):
                morse += self.char2morse(letter)
                if(not (i == len(wordList)-1 and j == len(word)-1)):
                    morse += ' '
            if(i < len(wordList)-1):
                morse += '  '
        return morse


    def morse2char(self,morse):
        try:
            return self.table[morse]
        except KeyError, e:
            return '?'


    def char2morse(self,morse):
        try:
            return self.inverseTable[morse]
        except:
            return '?'


if __name__ == '__main__':
    main()
