#!/usr/bin/python
#imports
import sys
from sets import Set

# main con casos de prueba simple
def main():

    morseAPI = MorseAPI('')
    #test_string = '1101101100111'+'00000'+'1111110001111111100111111'+'00000'+'11101111111101110111'+'0000'+'11000111111'+'00000000'+'11111100111111'+'00000'+'1100001101111111101110111'+'000000'+'1101110'
    slow = "000000000000011111110000111111000011111000011111110000000000111111111111110000111111111110000011111111110000000011111100000111111111111000011111000111111000000000011111100001111111111111000000000000000000000001111111111000011111111110000000001111100000000011111100000111111111100011111000011111000000000011111000001111100000000000"
    medium = "00000000110110110011100000111111000111111001111110000000111011111111011101110000000110001111110000000001111110011111100000001100000110111111110111011100000011011100000000000"
    fast = "000000101011001100000111100111100111110000101111100110110000010011110000000111100111110001000011011111011010000110100000000000"
    test_extermo = "0000000"

    print "Se testean diferentes velocidades para un mismo mensaje..."

    print "-------------- SLOW -----------------"
    morseAPI.testApi(slow)
    print "-------------- MEDIUM -----------------"
    morseAPI.testApi(medium)
    print "-------------- FAST -----------------"
    morseAPI.testApi(fast)
    ## testeo la api con una cadenas raras
    morseAPI.testApi(test_extermo)

    morseAPI2 = MorseAPI(slow)
    morseAPI2.testApi(slow)


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

    ceros13 = 0
    ceros23 = 0
    oneAvgLen = 0
    sync = False

    """
        Constructor que recibe un preambulo que consta de los simbolos '.- .   .-' (AE A)
        y se sincroniza
    """
    def __init__(self,preambule):
        if(preambule != ''):
            self.syncronize_pulses(preambule)
            self.sync = True

    def testApi(self,test_string):

        repArray = self.repeticionList(test_string)

        minmaxarray = self.minMax(test_string)

        self.ceros13 = (minmaxarray[0] + minmaxarray[1])/3
        self.ceros23 = (minmaxarray[0] + minmaxarray[1])*2/3
        self.oneAvgLen = (minmaxarray[2] + minmaxarray[3]) / 2

        print "average de unos : " + str(self.oneAvgLen) + "| 1/3 de ceros : " + str(self.ceros13) + " | 2/3 de ceros :" + str(self.ceros23)

        ## testeo del metodo que convierte la entrada de bits en morse
        morse = self.decodeBits2Morse(test_string)
        print "codigo morse : " + morse

        ## testeo el conversor de morse a palabras humanas
        human = self.translate2Human(morse)
        print "palabras traducidas : " + human

        ## testeo el conversor inverso a morse
        morse = self.translate2Morse(human)
        print "conversion inversa : " + morse + "EOS"


    # uso strings para codificar 0 y 1 podria ser bits pero es mas facil de visualizar. OPTIMO SERIA USAR BITS!

    """
        Funcion que busca decodificar una secuencia binaria a codigo morse.
        La secuencia se asume no constante pero de representacion consistente.

        Procedimiento:

        Busco la maxima y minima repeticion de unos de un rango representativo.
        Luego tomo el promedio y separo las longitudes, si es menor al promedio
        es punto sino es raya.
        Con los ceros debo hacer tres clasificaciones, entonces separo en tercios
         y voy a clasificar de menor a mayor:
        primer tercio : espacio entre punto o raya
        segundo tercio : espacio entre caracteres
        tercer tercio : espacio entre palabras
    """
    def decodeBits2Morse(self,bits_array):

        morse = ''
        if(not self.sync):
            self.syncronize_pulses(bits_array)
        ones = 0
        ceros = 0
        for c in bits_array:
            if(c == '1'):
                ones+= 1
                if(ceros > 0):
                    if(ceros <= self.ceros13):
                        morse += ''
                    elif(self.finDeLetra(ceros)):
                        morse += ' '
                    else:
                        morse += '   '
                    ceros = 0
            else:
                ceros+= 1
                if(ones > 0):
                    if(ones <= self.oneAvgLen): # considero un punto
                        morse += '.'
                    else:
                        morse += '-'
                    ones = 0
        return morse

    """
        Funcion que hace la sincronizacion para saber los limites de senalizacion
    """
    def syncronize_pulses(self, bits_array):
        minmaxarray = self.minMax(bits_array)
        self.ceros13 = (minmaxarray[0] + minmaxarray[1])/3
        self.ceros23 = (minmaxarray[0] + minmaxarray[1])*2/3
        self.oneAvgLen = (minmaxarray[2] + minmaxarray[3]) / 2

    def finDeLetra(self, ceros):
        return ceros > self.ceros13 and ceros <= self.ceros23

    def finDePalabra(self, ceros):
        return ceros > self.ceros23

    def finDeTransicion(self,ceros):
        return ceros > 3 * self.ceros23

    """
        esta funcion me da la minima y maxima repeticion de ceros y unos
        (en ese orden)
    """
    def minMax(self,bits_array):
        (ceroRepList,oneRepList) = self.repeticionList(bits_array)
        ## saco los outliers para tener mejores minimos y maximos,
        ## simpre y cuando haya al menos dos elementos
        if(len(ceroRepList) > 2):
            ceroRepList = self.removeOutliers(ceroRepList)
        if(len(oneRepList) > 2):
            oneRepList = self.removeOutliers(oneRepList)
        print "cero list filtrada: " + str(ceroRepList)
        print "unos list filtrada: " + str(oneRepList)

        if(len(ceroRepList) > 0):
            minCeros = ceroRepList[0]
            maxCeros = ceroRepList[-1]
        else:
            minCeros=maxCeros=0

        if(len(oneRepList) > 0):
            minOnes = oneRepList[0]
            maxOnes = oneRepList[-1]
        else:
            minOnes=maxOnes=0

        return [minCeros,maxCeros,minOnes,maxOnes]

    """
        Una funcion que ejecuta una forma de quitar elementos muy extremos
        (outliers) altos y bajos para poder tomar un promedio mas representativo
    """

    def removeOutliers(self,orderlist):
        q1 = self.median(orderlist[:int(len(orderlist)/2)])
        q3 = self.median(orderlist[int(len(orderlist)/2):])
        iqr = q3 - q1
        maxlimit = q3 + 1*iqr
        minlimit = q1 - 1*iqr
        orderlist = filter(lambda e: e > minlimit and e < maxlimit ,orderlist)
        return orderlist

    """
        Funcion que me da la media de una lista ya ordenada
    """
    def median(self,orderlist):
        if(len(orderlist) % 2 == 0): # si es impar
            return ((orderlist[(len(orderlist)-1)/2] + orderlist[(len(orderlist)-1)/2 + 1]) / 2)
        else:
            return orderlist[(len(orderlist)-1)/2]

    """
        esta funcion me da la lista de repeticiones de ceros y unos,
        ordenada de menor a mayor, sin repeticiones
    """
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

    """
        Funcion que traduce una secuencia codigo morse a palabras legibles,
        segun tabla de correspondencias dada
        Unica convension por ser mas legible:
        espacio entre palabras es de exactamente 3 espacios
    """
    def translate2Human(self,morse_array):
        humanWords = ''
        words = morse_array.split('   ')
        for i,word in enumerate(words):
            if(word):
                word.strip()
                letterList = word.split()
                for letter in letterList:
                    humanWords += self.morse2char(letter)
            if(i < len(words)-1 and word != ''):
                humanWords += ' '

        return humanWords


    """
        Funcion que traduce palabras legibles a una secuencia en codigo morse,
        segun tabla de correspondencias dada.
        Unica convension por ser mas legible:
        espacio entre secuenias de codigo morse es de exactamente 3 espacios
    """
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

    """
        Funcion que obtiene el caracter correspondente a un determinado codigo morse.
        Si no lo encuentra devuelve ?
    """
    def morse2char(self,morse):
        try:
            return self.table[morse]
        except KeyError, e:
            return '?'

    """
        Funcion que obtiene el codigo morse correspondente a un determinado caracter.
        Si no lo encuentra devuelve ?
    """
    def char2morse(self,morse):
        try:
            return self.inverseTable[morse]
        except:
            return '?'


if __name__ == '__main__':
    main()
