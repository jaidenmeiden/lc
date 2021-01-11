#!/usr/bin/env python
# coding: utf-8

# # EVALUACIÓN DE ETIQUETADORES MORFOSINTÁCTICOS PARA EL ESPAÑOL

# In[ ]:


import nltk
from nltk.corpus import cess_esp as cess
from nltk.tag import hmm
from nltk.tag import tnt
from nltk.tag.sequential import AffixTagger
from nltk.tag import brill, BigramTagger, BrillTaggerTrainer, CRFTagger, RegexpTagger, UnigramTagger
from nltk.tag.perceptron import PerceptronTagger
nltk.download('cess_esp')

import matplotlib.pyplot as plt

import numpy as np
from numpy import mean
from numpy import std

import scipy as sp
import scipy.stats

import inspect
import random
import time

import sklearn
from sklearn import svm
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

get_ipython().system('pip3 install sklearn_crfsuite')
get_ipython().system('pip install python-crfsuite')
get_ipython().system('pip install pythainlp')


# 1.**Objetivos del trabajo:**
# 
# * Conocer distintas herramientas de etiquetado morfosintáctico del paquete NLTK
# * Aplicar   la   metodología   de   validación   cruzada   para   entrenar   y   evaluar etiquetadores morfosintácticos.
# * Construir modelos de etiquetado morfosintáctico para el español a partir de corpus anotados
# * Comparar las prestaciones de distintos etiquetadores incluyendointervalos de confianza
# 
# 2.**Descripción del trabajo:**
# 
# El trabajo consiste  en  la  evaluación  de  las  prestaciones  dedistintosetiquetadores  morfosintácticos para uncorpus  del español(cess-esp).  En  esta  experimentación  se  estudiará  cómo  afectan  diversos parámetros  a  las  prestaciones  del  sistema:  el  tamaño  del  corpus  de  entrenamiento,  el  método  de suavizado para las palabras desconocidas, el juego de categorías morfosintácticas utilizado, etc.
# 
# Además,  se  compararán  las  prestaciones  de  distintos  etiquetadores  morfosintácticos  basados  en distintos paradigmas de aprendizaje.
# 
# Para ello,se utilizará el paquete NLTKque implementa diferentes etiquetadores morfosintácticos.
# 
# La evaluación de los etiquetadores se realizará mediante una validación cruzadasobre 10 partidoes del corpus.  Esta metodología consiste en dividir el corpus en 10 partes de similar tamaño, y ejecutar diez  experimentos.
# 
# En cada ejecución se  toman  9  partes  como  entrenamiento  y  1  como  prueba,  de manera que la parte de prueba siempre sea diferente.
# 
# La evaluación de las prestaciones del etiquetador es el resultado de calcular la media de la precisión de etiquetado (accuracy) sobre las distintas partidoes.
# 
# accuracy= número palabras etiquetadas correctamentedel test/ número total de palabrasdel test
# 
# IMPORTANTE:   Los   resultados   de accuracyobtenidos   deberán   presentarse   siempre   con el correspondiente intervalode confianza
# 
# ## Funciones

# In[ ]:


def label_transform (lista):
    for position, item in enumerate(lista):
        if item[1].startswith('v') or item[1].startswith('F'):
            lista[position] = ( lista[position][0], item[1][:3] ) 
        else:
            lista[position] = ( lista[position][0] , item[1][:2] )
    return lista
    

def eliminarAnotaciones(lista):
    for idx,tagged_word in enumerate(lista):
        if tagged_word[0] == '*0*' or tagged_word[0] == 'sn':
            lista.pop(idx)
        else:
            pass
    
    return label_transform(lista)

def validacion_cruzada(classificador,train_data,k):
    kf = KFold(k,shuffle=True)
    scores=[]
  
    for i,j in kf.split(train_data):
        if type(classificador) == type(hmm.HiddenMarkovModelTrainer()):
            model = classificador.train_supervised(train_data[i[0]:i[-1]])
            scores.append(model.evaluate(train_data[j[0]:j[-1]]))
        else:
            classificador.train(train_data[i[0]:i[-1]])
            scores.append(classificador.evaluate(train_data[j[0]:j[-1]]))
    
    return scores

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h,h


# ### Corpus

# In[ ]:


oraciones_sin_procesar = cess.tagged_sents()
oraciones_sin_procesar


# In[ ]:


oraciones_procesadas = []

for i in oraciones_sin_procesar:
    procesada = eliminarAnotaciones(i)
    oraciones_procesadas.append(procesada)
    
oraciones_procesadas


# In[ ]:


train_completo, test_completo = train_test_split(oraciones_sin_procesar, test_size=0.10, random_state=42)
train_reducido, test_reducido = train_test_split(oraciones_procesadas, test_size=0.10, random_state=42)


# # Tarea 1:
# 
# #### Evaluación del etiquetador ‘hmm’ sobre el corpus ‘cess-esp’ utilizando el juego de categorías completo y reducido.
# 
# Utilizando el etiquetador hmm basado en modelos de Markov, se realizará una validación cruzada sobre 10 partidoes del corpus. Barajar el corpus antes de realizar las partidoes. Presentar los resultados en forma de tabla y gráficamente, incluyendo los intervalos de confianza.

# In[ ]:


modelo = hmm.HiddenMarkovModelTrainer()
accuracys_completo = validacion_cruzada(modelo, list(oraciones_sin_procesar), k=10)


# In[ ]:


accuracys_reducido = validacion_cruzada(modelo, oraciones_procesadas, k=10)


# In[ ]:


print('Completo: ',mean_confidence_interval(accuracys_completo))
print('Reducido: ',mean_confidence_interval(accuracys_reducido))


# In[ ]:


print(accuracys_completo)


# In[ ]:


print(accuracys_reducido)


# In[ ]:


fig, ax = plt.subplots(figsize=(20,2))

fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')

ax.table(cellText=np.array( [accuracys_completo, accuracys_reducido ] ).T, colLabels=["Precisión completo","Precisión reducido"], loc='center')

fig.tight_layout()

plt.show()


# In[ ]:


_, _, _, err_completo = mean_confidence_interval(accuracys_completo[1:])
_, _, _, err_reducido = mean_confidence_interval(accuracys_reducido[1:])


# In[ ]:


plt.figure(figsize=(10,5))
plt.errorbar(range(10), accuracys_completo,yerr=err_completo, fmt='o', label='Precisión Completo')
plt.errorbar(range(10), accuracys_reducido,yerr=err_reducido, fmt='o', label='Precisión Reducido')
plt.ylim(0.97, 1)
plt.title('Comparación')
plt.xlabel('Particiones')
plt.ylabel('Exactitud')
plt.legend()
plt.show()


# # Tarea 2:
# 
# #### Evaluación de las prestaciones del etiquetador respecto a la cantidad de datos de aprendizaje.
# 
# Se trata de estudiar cómo varían las prestaciones del etiquetador hmm cuando varía el tamaño del corpus de aprendizaje. Para este experimento se dividirá el corpus de entrenamiento en 10 partes de tamaño similar. La partición 10 se tomará como test, y las 9 partidoes restantes se tomarán como entrenamiento. En cada ejecución, se irá incrementando sucesivamente el tamaño del corpus de entrenamiento, manteniendo fija la partición de test.
# 
# > **Importante:** Para esta tarea **no es necesario** realizar la validación cruzada.

# In[ ]:


trainers = []

acc = []
tmp = []

kf = KFold(n_splits=10,shuffle=True)
for _, j in  kf.split(oraciones_procesadas):
    trainers.append(oraciones_procesadas[j[0]:j[-1]])

for idx,i in enumerate(trainers[:9]):
    tmp += i
    model = modelo.train_supervised(tmp)
    acc.append(model.evaluate(trainers[-1]))
    print("Entre 0 y ",len(tmp) - 1," Exactitud: ",acc[idx])


# In[ ]:


plt.figure(figsize=(10,5))
plt.plot(range(9), acc, 'o', label='Exactitud')
plt.title('Variación')
plt.xlabel('Particiones')
plt.ylabel('Exactitud')
plt.legend()
plt.show()


# # Tarea 3:
# 
# #### Evaluación del método de suavizado para palabras desconocidas para el etiquetador tnt.
# 
# El etiquetador tnt por defecto no incorpora un método de suavizado para las palabras desconocidas. Utiliza un método basado en los sufijos de las palabras para construir un modelo para las palabras desconocidas (Affix Tagger). En base al sufijo de la palabra desconocida le asigna una categoría morfosintáctica. Este método funciona razonablemente bien para el inglés.
# 
# En concreto, se trata de estudiar diferentes longitudes del sufijo (número de letras que se tienen en cuenta) y estudiar cómo varían las prestaciones del etiquetador. Una vez se haya decidido el sufijo que mejores prestaciones proporciona, incorporarlo como modelo de suavizado al etiquetador tnt y comprobar si aumenta sus prestaciones.

# In[ ]:


accuracys = []
accuracysSolo = []


# In[ ]:


for i in range(-1,-5,-1):
    #SIN TNT
    affix_tagger = AffixTagger(train=train_reducido,affix_length=i)
    evalSolo = affix_tagger.evaluate(test_reducido)
    accuracysSolo.append(evalSolo)
    print("Suavizado Solo con  Affix_Length = ",i," Accuracy: ", evalSolo)

    #CON TNT
    tnt_tagging =  tnt.TnT(unk=affix_tagger,Trained=True)
    tnt_tagging.train(train_reducido)
    evaluacion = tnt_tagging.evaluate(test_reducido)
    accuracys.append(evaluacion)
    print("TnT Con suavizado Affix_Length = ",i," Accuracy: ", evaluacion)


# In[ ]:


print(accuracys)


# In[ ]:


print(accuracysSolo)


# In[ ]:


fig, ax = plt.subplots(figsize=(20,2))

fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')

ax.table(cellText=np.array([range(1,5),accuracys,accuracysSolo]).T, colLabels=["Affix Length","Accuracy","Accuracy Affix Solo"], loc='center')

fig.tight_layout()

plt.show()


# # Tarea 4:
# 
# #### Evaluación del resto de etiquetadores.
# 
# Se deberán utilizar otros paradigmas de etiquetado. Como mínimo el etiquetador de Brill y algún otro como, CRF, perceptron. Se deberá realizar una comparativa de prestaciones respecto a los etiquetadores tnt y hmm, utilizando el juego de categorías reducido.
# 
# Cuando se utilice el etiquetador de Brill, probar con diferentes etiquetados iniciales, por ejemplo probar con Unigram Tagger y con hmm tagger.
# 
# La comparación puede ser sólo de una partición, si el coste temporal de la validación cruzada requiere mucho tiempo.

# In[ ]:


xlabels = []
accuracys = []


# In[ ]:


def entrenar_bill(initial_tagger,tagger_name):
    brill_tagger = BrillTaggerTrainer(initial_tagger=initial_tagger,templates=brill.brill24())
    tagger1 = brill_tagger.train(train_reducido[:1000])
    evaluacion = tagger1.evaluate(test_reducido[:1000])
    xlabels.append("Brill Tagger "+tagger_name)
    accuracys.append(evaluacion)


# In[ ]:


# instanciamos y entrenamos brill con el tagger Regexp basado en el ejemplo de uso del mismo.
tagger = RegexpTagger([
(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),   # cardinal numbers
(r'(The|the|A|a|An|an)$', 'AT'),   # articles
(r'.*able$', 'JJ'),                # adjectives
(r'.*ness$', 'NN'),                # nouns formed from adjectives
(r'.*ly$', 'RB'),                  # adverbs
(r'.*s$', 'NNS'),                  # plural nouns
(r'.*ing$', 'VBG'),                # gerunds
(r'.*ed$', 'VBD'),                 # past tense verbs
(r'.*', 'NN')                      # nouns (default)
])
entrenar_bill(tagger,"RegexpTagger")


# In[ ]:


tagger = UnigramTagger(train_reducido[:1000])
tagger.evaluate(test_reducido[:1000])
entrenar_bill(tagger,"UnigramTagger")


# In[ ]:


tagger = BigramTagger(train_reducido[:1000])
tagger.evaluate(test_reducido[:1000])
entrenar_bill(tagger,"BigramTagger")


# In[ ]:


ct = CRFTagger()
ct.train(train_reducido[:1000],'model.crf.tagger')
evaluacion = ct.evaluate(test_reducido[:1000])
xlabels.append("CRF Tagger")
accuracys.append(evaluacion)


# In[ ]:


tagger = PerceptronTagger(load=False)
tagger.train(train_reducido[:1000])
evaluacion = tagger.evaluate(test_reducido[:1000])
xlabels.append("Perceptron Tagger")
accuracys.append(evaluacion)


# In[ ]:


print(accuracys)


# In[ ]:


print(xlabels)


# In[ ]:


fig, ax = plt.subplots(figsize=(20,2))

fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')

ax.table(cellText=[accuracys], colLabels=xlabels, loc='center')

fig.tight_layout()

plt.show()

