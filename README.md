# morse
morse code translator in python

## Enviroment

python 2.7

## Uso

existen dos ejecutables : 

### morse.py 

corre tres test basicos cada uno a distintas velocidades de transmicion de los pulsos binarios. El codigo es el mismo del ejemplo del enunciado. 

### test_input.py

Es un intento de simular un telegrafo analogico en nuestro mundo digita, envia pulsos con la tecla SPACE y a medida que transcurre el tiempo se producen pausas (equivalente a ceros en este script). Al terminar se debe presionar ENTER y el sistema intentara decodificar en morse y luego a lenguaje humano (segun tabla aportada en el enunciado)
Es un script de consola hecho con curses

## API

La API para traducir morse a castellano se puede consultar de la siguente forma en estas url's:

* curl -X POST "https://morse-192815.appspot.com/translate/2text" -d '{ "text" : ".... --- .-.. .-   -- . .-.. .." }'

* curl -X POST "https://morse-192815.appspot.com/translate/2morse" -d '{ "text" : "HOLA MELI" }'

Por convencion mia, para que sea mas legible, el conjunto de pulsos que forman un caracter se separan con un espacio y las palabras se separan con tres.

