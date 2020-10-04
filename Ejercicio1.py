def divWordsDictionary(listaPalabras):
  contexto = []
  palabras = []
  categorias = []
  compuesto = []
  for p in listaPalabras:
    temp = p.split('/')
    palabras.append(temp[0].lower())
    categorias.append(temp[1])
    compuesto.append(temp[0].lower() + '_' + temp[1])
  contexto.append(palabras)
  contexto.append(categorias)
  contexto.append(compuesto)
  return contexto

def listaDictionaryFrec(listaPalabras, pos):
  extract = divWordsDictionary(listaPalabras).copy()
  extract[pos].sort()
  frecuencia = [extract[pos].count(p) for p in extract[pos]]
  return dict(list(zip(extract[pos],frecuencia)))

def listaDictionaryMorfosintacticasFrec(listaPalabras, palabras, compuesto):
  lista = listaPalabras.copy()
  lista.sort()
  extract = divWordsDictionary(lista).copy()
  busqueda = {}
  for x in range(len(lista)):
    busqueda[extract[0][x]] = [palabras[extract[0][x]], {}]
  for x in range(len(lista)):
    for key in busqueda:
      if key == extract[0][x]:
        busqueda[extract[0][x]][1][extract[1][x]] = compuesto[extract[0][x] + '_' + extract[1][x]]
  return busqueda

def bigramasFrec(listaPalabras, pos):
  extract = divWordsDictionary(listaPalabras).copy()
  lista = extract[pos]
  lista.insert(0, '<S>')
  lista.append('</S>')
  bigrama = {}
  for x in range(len(lista) - 1):
    bigrama[(lista[x], lista[x + 1])] = 0
  for x in range(len(lista) - 1):
    bigrama[(lista[x], lista[x + 1])] = bigrama.get((lista[x], lista[x + 1])) + 1
  return bigrama

def probabilidades(palabra, categorias, morfosintacticas):
  print()
  print('######## Palabra: ' + palabra + ' ########')
  repite = morfosintacticas[palabra]
  for key, value in repite[1].items():
    print('P( ' +  key + ' | ' + palabra +' )=' + str(value/repite[0]))
  print()
  for key, value in repite[1].items():
    print('P( ' +  palabra + ' | ' + key +' )=' + str(value/categorias[key]))
  print('######## Fin ########')


cadena="El/DT perro/N come/V carne/N de/P la/DT carnicería/N  y/C de/P la/DT nevera/N y/C canta/V el/DT la/N la/N la/N ./Fp"
listaPalabras = cadena.split()

# Ejercicio 
categorias = listaDictionaryFrec(listaPalabras, 1)
print('####################### Ejercicio 1 #############################')
print('Obtener  un diccionario, que para cada categoría, muestre su frecuencia. Ordenar el resultado alfabéticamente por categoría')
print(categorias)
print()

# Ejercicio 2
palabras = listaDictionaryFrec(listaPalabras, 0)
compuesto = listaDictionaryFrec(listaPalabras, 2)
print('####################### Ejercicio 2 #############################')
print('Obtener un diccionario, que para cada palabra, muestre su frecuencia, y una lista de sus categorías morfosintácticas con su respectiva frecuencia. Mostrar el resultado ordenado alfabéticamente por  palabra')
morfosintacticas = listaDictionaryMorfosintacticasFrec(listaPalabras, palabras, compuesto)
print(morfosintacticas)
print()

# Ejercicio 3
print('####################### Ejercicio 3 #############################')
print('Calcular la frecuencia de los todos los bigramas de la cadena, considerar un símbolo inicial <S>  y un símbolo final </S>para la cadena')
print(bigramasFrec(listaPalabras, 1))
print()

# Ejercicio 4
print('####################### Ejercicio 4 #############################')
print('Construir una función que devuelva las probabilidades léxicas  P(C|w) y de emisión P(w|C) para una palabra dada (w)  para todas sus categorías (C)  que aparecen en el diccionario construido anteriormente. Si la palabra no existe en el diccionario debe decir que la palabra es desconocida')
print(palabras)
for key in palabras.keys():
  probabilidades(key, categorias, morfosintacticas)
print()