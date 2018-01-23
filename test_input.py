#!/usr/bin/python
import curses, os, time
from morse import MorseAPI

def main(win):

    #win.nodelay(True) # no bloqueo esperando el input en win.getch()
    key=""
    pulses = ''
    pause_wait = 0
    win.clear()
    win.addstr(0,6,"Simulador de telegrafo para codigo morse",curses.A_BOLD)
    win.addstr(5,1,"Queres un telegrafo analogico? (Es mas dificil!) [Y/n]")
    key = win.getkey()
    win.clear()
    if(key == 'Y' or key == 'y'):
        win.addstr(2,1,"Los pulsos (1's) se ingresan con el SPACE, las pausas son la ausencia de pulso (0's) van apareciendo solas con el paso del tiempo." )
        win.addstr(3,1,"presiona ENTER para terminar el envio y procesar")
        win.addstr(6,1,"Atento! Es muy sensible a las inconsistencias", curses.A_BOLD)
        key = win.getkey()
        curses.halfdelay(5) # tiempo que se bloquea esperando un input en win.getch()
        pause_wait = 0.5
    else:
        win.addstr(2,1,"Los pulsos (1's) se ingresan con el SPACE, las pausas son la ausencia de pulso (0's) se generan con cualquier otra tecla." )
        win.addstr(3,1,"presiona ENTER para terminar el envio y procesar")
        win.addstr(6,1,"Atento! Es muy sensible a las inconsistencias", curses.A_BOLD)


    win.clear()
    win.addstr("pulsos :",curses.A_BOLD)
    start_time = time.time()
    while 1:
        try:
            key = win.getch() # input del usuario
            win.clear()
            win.addstr("pulsos :",curses.A_BOLD)

            if(key == 32): # espacio
                pulses += '1'
            else:
                if(elapsed_time >= pause_wait):
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
    win.addstr(2,1,"codigo morse : " + morse)

    ## testeo el conversor de morse a palabras humanas
    human = mapi.translate2Human(morse)
    win.addstr(3,1,"palabras traducidas : " + human)

    curses.nocbreak()
    win.getkey()

curses.wrapper(main)
