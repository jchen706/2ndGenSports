# 2nd Generation Sports

## Team & Contact Information

1. Jun Chen  jchen706@gatech.edu 
2. Phillip Hong phong9@gatech.edu 
3. Justin Chiu jchiu33@gatech.edu 
4. Eric Vizcaya-Eternod eve6@gatech.edu
5. Jesus Gonzalez jgonzalez314@gatech.edu 

## Release Notes version 1.0
* Web Scraper support
* Added gender to table
* Added ability to delete entries from “All Data” table
* Updated “About” page

## Bug Fixes
* Checkboxes being off screen
* Highlighting using same colors for different words
* Cutting off ends of long sentences
* Keywords not being counted near punctuation
* Many false positives

## Known Bugs
* Error may occur if trying to process a pdf that is not in the 'static' folder 
* Highlighter “on/off” toggle gets put to the left of the results table when processing a PDF with a small amount of hits
* Web scraper does not support the school Brigham Young University (BYU) due to their unique web formatting
* The word “sea-son” may be acting like a hit on the keyword “son” in the Florida Gators 2019 Football Media Guide; “sea-son” appears when a paragraph of text gets read

## Install Guide version 1.0
### Pre-requisites:
* Miniconda Python 3.7: https://docs.conda.io/en/latest/miniconda.html
* Use all default settings when installing Miniconda
* You must also have JRE 1.8 installed and configured before proceeding. See https://www.java.com/en/download/

### Dependencies:
* All dependency downloads are handled in the “Installation” section of the guide below 
* For names of specific packages used, read requirements.txt in the repository
* Open an Anaconda Prompt window

### Download:
* https://github.com/jchen706/2ndGenSports
* There will be a download button on the right side of the page

### Build:
No build necessary for this app.

### Installation
* Download the repository to your local machine
* Open an Anaconda Prompt window and navigate to the root directory of the repository. It should be called 2ndGenSports-master
If you are unfamiliar with how to navigate a command prompt window, here is a [Mac tutorial](https://www.macworld.com/article/2042378/master-the-command-line-navigating-files-and-folders.html "Mac tutorial") and a [Windows tutorial](https://www.watchingthenet.com/how-to-navigate-through-folders-when-using-windows-command-prompt.html "Windows tutorial")
* Create and activate the environment by executing the following commands in the Anaconda prompt window:
    * `conda create -n myenv python=3.6`
    * `conda activate myenv`
* Install the dependencies from requirements.txt by executing this command:
    `pip install -r requirements.txt`
* This could take a while because there are quite a few dependencies.
* Next do the following to install AWSCLI
    `pip install awscli`
* You will need an AWS key to use the database. Contact the developers for a key at jchen706@gatech.edu
* To configure AWS do the following to enter your key information
    * `aws configure`
    * Use “us-east-1” as the Default Region Name
    * Ignore the Default output format, you can type ‘None’
* Open a python shell by typing “python” into the Anaconda Prompt window and pressing Enter
* Execute the following commands:
    * `import nltk`
    * `nltk.download(‘punkt’)`
* Exit the python shell by typing “exit()” and pressing Enter

### Running Application
* Make sure you have your miniconda environment running
    * `conda activate myenv`
* Execute the following command in an Anaconda Prompt window to run the Python web application on localhost:5000
    * `python 2ndgen.py`
* Open a browser and type or paste http://localhost:5000 into the address bar
* Hit enter and you should see the website displayed

### Troubleshooting
* Be sure to install all the dependencies on the miniconda environment you created. You will know that you are in your miniconda environment if you see `myenv` in the Anaconda Prompt window
* If you are having trouble running the application, make sure you have first activated the miniconda environment using `conda activate myenv`
