# Lingüistica computacional

## SRILM - Tutorial
#### Resumen
Este tutorial lo guiará a través de los pasos de la instalación y ejecución de SRILM, una herramienta para producir modelos de lenguaje, archivos de conteo de n-gramas y muchos otros recursos lingüísticos. Podrás crear **El archivo de origen n-gram**, **El archivo de destino n-gram**, **Modelo del lenguaje fuente** y el **Modelo del lenguaje destino**. 
#### Instalación
Los pasos a continuación lo guían a través del proceso de instalación de SRILM para que sea utilizado por [QuEst SVM Model Builder Paso](https://okapiframework.org/wiki/index.php/QuEst_SVM_Model_Builder_Paso) y [QuEst Quality Estimation Paso](https://okapiframework.org/wiki/index.php/QuEst_Quality_Estimation_Paso). SRILM se ejecuta tanto en Linux, Mac y Windows, aunque el último deberá tener instalado un entorno  [Cygwin](http://www.cygwin.com/).  

**Paso 1:** Si es un usuario de Linux ó Mac, descargue todas las herramientas necesarias que se enumeran en la [página de descargas SRILM](http://www.speech.sri.com/projects/srilm/download.html). Si es un usuario de Windows, descargue e instale [Cygwin](http://www.cygwin.com/), asegurándose de seleccionar todas las herramientas necesarias durante la instalación. Si Cygwin acusa de alguna herramienta faltante durante la instalación de SRILM, reinstale Cygwin y seleccione las herramientas faltantes durante su instalación.

**Paso 2:** Descargue la última versión de SRILM completando el formulario disponible en la [página de descargas SRILM](http://www.speech.sri.com/projects/srilm/download.html).

**Paso 3:** Desempaquete el archivo dentro de la carpeta que desea que se instale SRILM. Los usuarios de Windows deben elegir una carpeta dentro de su instalación de Cygwin para que los siguientes pasos sean más simples de manejar.

**Paso 4:** Abra el Makefile dentro de la carpeta donde se descomprimió SRILM usando cualquier editor de texto.

**Paso 5:** Debería encontrar una línea comentada que se parezca a esto: 
```bash
# SRILM = /home/speech/stolcke/project/srilm/devel
```
Elimine el carácter "**#**" del principio de esta línea y sustituya **/home/speech/stolcke/project/srilm/devel** con la ruta a la carpeta donde desempaquetó SRILM inicialmente. Los usuarios de Windows deben usar la ruta relativa a la carpeta raíz de Cygwin. Ejemplos:

Para usuarios de Linux ó Mac: 
```bash
SRILM = /home/oem/tools/srilm
```
Para los usuarios de Windows, suponga que ha instalado Cygwin en la carpeta **C:/cygwin64/** y ha descomprimido SRILM en la carpeta **C:/cygwin64/srilm**: 
```bash
SRILM = /srilm
```
**Paso 6:** Usando una terminal Linux / Mac o una terminal Cygwin, navegue hasta la carpeta donde ha desempaquetado SRILM.

**Paso 7:** Ejecute el comando **make**.


Si ha seguido estos pasos correctamente, los binarios compilados de SRILM deben encontrarse dentro de la siguiente carpeta:

Para el ejemplo de Linux ó Mac del **Paso 5**:  
```bash
/home/oem/tools/srilm/bin/[your_machine_type]/
```
Para el ejemplo de Cygwin del **Paso 5**: 
```bash
C:/cygwin64/srilm/bin/cygwin/
```

> **_NOTA:_** Esta es la ruta que debe utilizar como parámetro de [QuEst SVM Model Builder Paso](https://okapiframework.org/wiki/index.php/QuEst_SVM_Model_Builder_Paso) y el [QuEst Quality Estimation Paso](https://okapiframework.org/wiki/index.php/QuEst_Quality_Estimation_Paso).

Si la carpeta en cuestión está vacía o no existe, se ha producido algún error durante la compilación de SRILM. Intente seguir los pasos con más cuidado y, si el problema persiste, intente consultar foros en línea o póngase en contacto con los desarrolladores de SRILM.

---

#### Ejecución
Los siguientes pasos le permitirán producir modelos de idioma y archivos de recuento de N-gramas con SRILM.

**Paso 1**: Navegue a la carpeta de binarios de su instalación de SRILM usando un terminal Linux ó Mac o un terminal Cygwin en caso de que sea un usuario de Windows. La carpeta de binarios a la que nos referimos es la que contiene las aplicaciones compiladas de SRILM, como **ngram** y **ngram-count**.

**Paso 2**: Run the following command: 
```bash
./ngram-count -text [corpus] -lm [output_language_model] -order 3 -write [output_ngram_file_path]
```


Si siguió los pasos correctamente, encontrará el modelo de lenguaje producido en la ruta proporcionada como parámetro en **[output_language_model]**, y el archivo de recuentos de N-gram en la ruta proporcionada en **[output_ngram_file_path]**. Si no encuentra esos archivos o SRILM acusa de un error, intente volver a ejecutar SRILM y preste mucha atención a los pasos anteriores. Si el problema persiste, evalúe los foros en línea o comuníquese con los desarrolladores de SRILM.