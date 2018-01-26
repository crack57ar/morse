# morse
morse code translator in python

## Enviroment

python 2.7

## Uso

existen dos ejecutables : 

### morse.py 

corre tres test basicos cada uno a distintas velocidades de transmicion de los pulsos binarios. El codigo es el mismo del ejemplo del enunciado. 

### test_input.py

Es un intento de simular un telegrafo analogico en nuestro mundo digital, envia pulsos con la tecla SPACE y a medida que transcurre el tiempo se producen pausas (equivalente a ceros en este script). El modo analogico necesita de un preambulo para sincronizarse, el preambulo sera el codigo morse correspondiente a la frase AE A ('.- .   .-'), si la sincronizacion no es correcta el mensaje sera mal interpretado.
Existe una opcion digital en la que al presionar cualquier otra tecla (menos ENTER) se insertan las pausas (ceros), para hacerlo mas simple y pausado. Ademas aqui la sincronizacion se hace con el mensaje entero y es mas precisa.
Al terminar se debe presionar ENTER y el sistema intentara decodificar en morse y luego a lenguaje humano (segun tabla aportada en el enunciado)
Es un script de consola hecho con curses. 

### bmorse.py

Un script que genera, dado un texto, su representacion en pulsos binarios de codigo morse. Posee parametros de alatoriedad para simular el error humano. Si estos son muy altos puede desatar el caos!

usage: bmorse.py [-h] [-v V] [-r R] [-s S]

optional arguments:
  -h, --help  show this help message and exit
  -v V        los pulsos y pausas varian en +/- v
  -r R        ritmo de transferencia de los pulsos
  -s S        palabra a codificar

## API

La API para traducir morse a castellano se puede consultar de la siguente forma en estas url's:

* curl -X POST "https://morse-192815.appspot.com/translate/2text" -d '{ "text" : ".... --- .-.. .-   -- . .-.. .." }'

* curl -X POST "https://morse-192815.appspot.com/translate/2morse" -d '{ "text" : "HOLA MELI" }'

Por convencion mia, para que sea mas legible, el conjunto de pulsos que forman un caracter se separan con un espacio y las palabras se separan con tres.

