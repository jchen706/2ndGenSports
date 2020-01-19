# 2nd Generation Sports

**Team**

Jun Chen
Phillip Hong
Justin Chiu
Eric Vizcaya-Eternod
Jesus Gonzalez

**Setup**

Using Miniconda Python 3.7 to install a virtual python environment. 
Miniconda: https://docs.conda.io/en/latest/miniconda.html 

Clone or Download the Repository

Open Miniconda or Anaconda Prompt

####Create Environment
`$conda create -n myenv python=3.6
 $conda activate myenv
`




first time installing ntlk, you'll have to download the library 
so you have to put nltk.download() in the 2ndgen.py , comment out that line after the first time trial


So upload Pdf words. 
Don't use Pypdf2, the pdf extraction is terrible. 

Current pdf extraction uses tika, which uses a multithread virtual machine to process text. Works pretty fast 196 pages in less than 1 minute.



