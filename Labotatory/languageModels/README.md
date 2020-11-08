# Lingüistica computacional

## SRILM Installation and Running Tutorial
#### Overview
This tutorial will guide through the steps of the installation and running of SRILM, a tool for producing language models, n-gram count files and many other linguistic resources. With this tutorial you will be able to produce the **Source n-gram file**, **Target n-gram file**, **Source language model** and the **Target language model**, which are required by the QuEst SVM Model Builder Step and the QuEst Quality Estimation Step. 
#### Installation
The steps below guide you through the process of installing SRILM for it to be used by the [QuEst SVM Model Builder Step](https://okapiframework.org/wiki/index.php/QuEst_SVM_Model_Builder_Step) and [QuEst Quality Estimation Step](https://okapiframework.org/wiki/index.php/QuEst_Quality_Estimation_Step). SRILM runs on both Linux/Mac or Windows, although the later will need to have a [Cygwin](http://www.cygwin.com/) environment installed.  

> **_NOTE:_** This tutorial have been tested only with 64 bits operational systems.

**Step 1:** If you are a Linux/Mac user, download all the required tools listed at the [SRILM download page](http://www.speech.sri.com/projects/srilm/download.html). If you are a Windows user, download and install [Cygwin](http://www.cygwin.com/), making sure to select all the required tools during the installation. If Cygwin accuses of any missing tools during the installation of SRILM, re-install Cygwin and select the missing tools during its installation.

**Step 2:** Download the latest version of SRILM by filling out the form available at the [SRILM download page](http://www.speech.sri.com/projects/srilm/download.html).

**Step 3:** Unpack the file inside the folder you desire for SRILM to be installed. Windows users should choose a folder inside their installation of Cygwin for the following steps to be simpler to handle.

**Step 4:** Open the Makefile inside the folder where SRILM was unpacked using any text editor.

**Step 5:** You should find a commented line which looks something like this: 
```bash
# SRILM = /home/speech/stolcke/project/srilm/devel
```
Remove the "**#**" character from the beginning of this line and substitute **/home/speech/stolcke/project/srilm/devel** with the path to the folder where you have unpacked SRILM initially. Windows users should use the path relative to Cygwin's root folder. Examples:

For Linux/Mac users: 
```bash
SRILM = /home/tools/user/srilm
```
For Windows users, suppose that you have installed Cygwin in the folder **C:/cygwin64/** and have unpacked SRILM in the folder **C:/cygwin64/srilm**: 
```bash
SRILM = /srilm
```
**Step 6:** Using either a Linux/Mac terminal or a Cygwin terminal, navigate to the folder where you have unpacked SRILM.

**Step 7:** Run the command **make**.


If you have followed this steps correctly, the compiled binaries of SRILM should be found inside the following folder:

For the Linux/Mac example of **Step 5**:  
```bash
/home/tools/user/srilm/bin/[your_machine_type]/
```
For the Cygwin example of **Step 5**: 
```bash
C:/cygwin64/srilm/bin/cygwin/
```

> **_NOTE:_** This is the path you must use as the SRILM binaries folder parameter for the [QuEst SVM Model Builder Step](https://okapiframework.org/wiki/index.php/QuEst_SVM_Model_Builder_Step) and the [QuEst Quality Estimation Step](https://okapiframework.org/wiki/index.php/QuEst_Quality_Estimation_Step).

If the folder in question is empty or does not exist, some error have occurred during the compilation of SRILM. Try to follow the steps more carefully and, if the problem persists, try consulting forums online or contact the developers of SRILM. 

---

#### Running
The following steps will allow you to produce both Language Models and N-gram Count Files with SRILM.

**Step 1**: Navigate to the binaries folder of your SRILM installation using either a Linux/Mac terminal, or a Cygwin terminal in case you are a Windows user. The binaries folder we refer to is the one which contains the compiled applications of SRILM, such as **ngram** and **ngram-count**.

**Step 2**: Run the following command: 
```bash
./ngram-count -text [corpus] -lm [output_language_model] -order 3 -write [output_ngram_file_path]
```


If you followed the steps correctly, you will find the Language Model produced at the path provided as a parameter in **[output_language_model]**, and the N-gram Counts File at the path provided in **[output_ngram_file_path]**. If you do not find those files or SRILM accuses of an error, try re-running SRILM and paying very close attention to the steps above. If the problem persists, assess online forums or contact the developers of SRILM. 