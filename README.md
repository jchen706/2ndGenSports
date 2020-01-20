# 2nd Generation Sports

## Team & Contact Information

1. Jun Chen  jchen706@gatech.edu 
2. Phillip Hong phong9@gatech.edu 
3. Justin Chiu jchiu33@gatech.edu 
4. Eric Vizcaya-Eternod eve6@gatech.edu
5. Jesus Gonzalez jgonzalez314@gatech.edu 

## Setup

Using Miniconda Python 3.7 to install a virtual python environment. 
Miniconda: https://docs.conda.io/en/latest/miniconda.html 

Clone or Download the Repository

Open Miniconda or Anaconda Prompt

#### Create Environment
`$conda create -n myenv python=3.6`
`$conda activate myenv`

Go to the respository root directory.

##### Install Dependences from requirements.txt
`$pip install -r requirements.txt`

##### Run the Application
`$python 2ndgen.py`
Application currently runs on localhost:5000

## More Information
First time installing ntlk, you'll have to download the library 
so you have to put nltk.download() in the 2ndgen.py , comment out that line after  the first time trial or on command line python editor
here:

```python
import nltk
nltk.download('punkt')
```



Don't use Pypdf2, the pdf extraction is terrible. 

Current pdf extraction uses tika, which uses a multithread virtual machine to process text. Works pretty fast 196 pages in less than 1 minute.



