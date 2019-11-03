# 2ndGenSports

Static Pages need to be in Static folder 
Html pages need to be in Templates folder

create a virutal environtment

You can install Miniconda and create a virutal env. Just google

Install the dependencies with pip install -r requirement.txt.

To run app. python 2ndgen.py

localhost:5000


first time installing ntlk, you'll have to download the library 
so you have to put nltk.download() in the 2ndgen.py , comment out that line after the first time trial


So upload Pdf words. 
Don't use Pypdf2, the pdf extraction is terrible. 

Current pdf extraction uses tika, which uses a multithread virtual machine to process text. Works pretty fast 196 pages in less than 1 minute.



