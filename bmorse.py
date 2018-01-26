#!/usr/bin/python
from morse import MorseAPI
import random
import argparse


class Bmorse():

    def __init__(self,varianza,ritmo,input_text):
        self.var = varianza
        self.velocidad = ritmo
        self.text = input_text

        self.point = self.velocidad
        self.line = self.point * 3
        self.space = self.velocidad
        self.letter_sep = self.point * 3
        self.word_sep = self.point * 5

    def generateRandomBinaryMorse(self):
        binary = ''
        mapi = MorseAPI('')
        morse = mapi.translate2Morse(self.text)
        wordList = morse.split('  ')
        for i,word in enumerate(wordList):
            for j,letter in enumerate(word):
                binary += self.randCodify(letter)
                if(j < len(word)-1):
                    binary += self.ranLenSec('0',self.letter_sep)
            if(i < len(wordList)-1):
                binary += self.ranLenSec('0',self.word_sep)

        return binary

    def randCodify(self,code):
        binary = ''
        for i,c in enumerate(code):
            if(c == '.'):
                binary += self.ranLenSec('1',self.point)
            elif (c == '-'):
                binary += self.ranLenSec('1',self.line)
            if(i != len(code)-1):
                binary += self.ranLenSec('0',self.space)

        return binary

    def ranLenSec(self,c,min):
        return  c * (min + random.randint(self.var * -1,self.var))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", help="los pulsos y pausas varian en +/- v",default=1)
    parser.add_argument("-r", help="ritmo de transferencia de los pulsos",default=3)
    parser.add_argument("-s", help="palabra a codificar",default="HOLA MELI")
    args = parser.parse_args()

    bmorse = Bmorse(int(args.v),int(args.r),str(args.s))

    test_input = bmorse.text
    mapi = MorseAPI('')
    morse = mapi.translate2Morse(test_input)
    print "codigo morse : " + morse
    randBinaryCode = bmorse.generateRandomBinaryMorse()
    print "codigo binario: " + randBinaryCode
    remorse = mapi.decodeBits2Morse(randBinaryCode)
    print "codigo re-morse : " + remorse
    print "codigo rehuman : " + mapi.translate2Human(remorse)


if __name__ == '__main__':
    main()
