#!/usr/bin/python
import curses, os, time
from morse import MorseAPI

def main(win):
    #win.nodelay(True)
    curses.halfdelay(5)
    key=""
    pulses = ''
    win.clear()
    win.addstr("pulsos :",curses.A_BOLD)
    start_time = time.time()
    while 1:
        #time.sleep (100.0 / 1000.0)
        try:
            key = win.getch()
            win.clear()
            win.addstr("pulsos :",curses.A_BOLD)

            if(key == 32): # espacio
                pulses += '1'
            else:
                if(elapsed_time >= 0.5):
                    pulses += '0'
                    start_time = time.time()
            win.addstr(pulses)
            if key == 10: # Enter
                break
        except Exception as e:
           # No input
           pass

        elapsed_time = time.time() - start_time

    win.clear()
    # traduzco lo que se acaba de tipear
    mapi = MorseAPI()

    morse = mapi.decodeBits2Morse(pulses)
    win.addstr(0,0,"codigo morse : " + morse)

    ## testeo el conversor de morse a palabras humanas
    human = mapi.translate2Human(morse)
    win.addstr(1,0,"palabras traducidas : " + human)

    curses.nocbreak()
    win.getkey()

curses.wrapper(main)
