from flask import Flask, render_template, session, redirect, url_for, request, abort, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
import os
from werkzeug.utils import secure_filename

import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import TweetTokenizer, sent_tokenize

import PyPDF2
import json
#import textract

import tika
tika.initVM()
from tika import parser
import mysql.connector
from mysql.connector import Error





#from flask_sqlalchemy import SQLAlchemy
#import SQLAlchemy

#absolute path of the file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#change this path to a folder for the upload
UPLOAD_FOLDER = '\static\pdfs'

ALLOWED_EXTENSIONS = {'pdf'}
DEBUG = True
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1547@localhost/alchemy'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = '1111'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#db = SQLAlchemy(app)

# class PdfFile(db.Model):
#     """docstring for ."""
#     id = db.Column(db.Integer, primary_key = True)
#     year = db.Column(db.Integer,)
#
#     def __init__(self, arg):
#         super(, self).__init__()
#         self.arg = arg


@app.errorhandler(400)
def bad_request(e):
     return render_template('400.html'), 400





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class MediaForm(FlaskForm):

    year = StringField('Year: ', validators = [DataRequired()])
    team = StringField('Team:', validators = [DataRequired()])
    sport =SelectField('Sport:', choices=[('foot', 'Football'),('basket', 'BasketBall')], validators = [DataRequired()] )
    gend = SelectField('Gender: ', choices=[('M','Male'), ('F','Female')], validators = [DataRequired()] )
    submit = SubmitField('Submit')

@app.route('/uploadpdf',methods = ['GET','POST'])
def newIndex():
    if(request.method == "POST"):

        if request.files:

            file1 = request.files["pdffile"]

            if (file.filename == ''):
                flash('No file selected')

            if(file and allowed_file(file.filename)):
                file1.save(os.path.join(app.config['UPLOAD_FOLDER'], file1.filename))
                print('file save')


            return redirect(request.url)

    return render_template("uploadpdf.html")


@app.route('/',methods = ['GET','POST'])
def index():
    processed = False
    year = 0000
    team = "No Team"
    gender = "No Input"
    sport = "No Input"
    list1 = []

    error_year = False
    error_team = False
    error_gender = False
    error_sport = False
    error_file = False

    #form = MediaForm()
    print(BASE_DIR)

    file_path = BASE_DIR + app.config['UPLOAD_FOLDER']
    print(file_path)

    #database server connection ...
    try:
        connection = mysql.connector.connect(host='localhost',
                                         database='sportgen',
                                         user='root',
                                         password='1547')

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


    #action posted from frontend
    if(request.method == "POST"):

        year = request.form['year']
        team = request.form['team']
        gender = request.form['gender']
        sport = request.form['sport']
        processed = True


        


        try:
            year = int(year)
        except:
            error_year = True

        try:
            year = int(year)
        except:
            error_year = True
  
        





        



        #count
        #pdf
          
        print(year)
        print(team)
        print(gender)
        print(sport)

        if request.files:

            file1 = request.files["pdffile"]
            print(file1.filename == '')

            if (file1.filename == ''):
                flash('No file selected')
                abort(400, description="No file submitted.")

            print(allowed_file(file1.filename))
            if(allowed_file(file1.filename)):
                file1.save(os.path.join(file_path, file1.filename))
                file = open(os.path.join(file_path, file1.filename), 'r')





                # read_file = file.read()
                # text = nltk.Text(nltk.word_tokenize(read_file))

                # match = text.concordance('parent')
                # print(match)
                # creating a pdf file object
                #
                pdfFileObj = open(os.path.join(file_path, file1.filename), 'rb')

                # creating a pdf reader object
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

                # printing number of pages in pdf file
                print(pdfReader.numPages)

                # creating a page object
                pageObj = pdfReader.getPage(0)

                # extracting text from page
                print(pageObj.extractText())
                #text = textract.process(os.path.join(app.config['UPLOAD_FOLDER'], file1.filename), extension='pdf')

                parsed = parser.from_file(os.path.join(file_path, file1.filename))
                #print(parsed["metadata"])
                #print(parsed["content"])
                input_text = parsed['content']

                tokenizer_words = TweetTokenizer()
                tokens_sentences = [tokenizer_words.tokenize(t) for t in nltk.sent_tokenize(input_text)]
                #print(tokens_sentences)
                wantedList=['parent','Parents', 'Father', 'Mother', 'father', 'mother', 'dad', 'Dad', 'Mom', 'mom']
                count = 0
                
                for eachSentence in tokens_sentences:
                    for each in wantedList:
                        if each in eachSentence:
                            count+=1
                            #print(eachSentence)
                            #print(" ")
                            #print(" ")
                            aSentence =' '.join(eachSentence)
                            list1.append(aSentence)


                #print(count)
                # for i in range(count):
                #     print(list[i])
                #     print('')


                # closing the pdf file object
                pdfFileObj.close()
                print('file save')
                
                return render_template('home.html', processed = processed, team_name =team , team_year=year, team_gender=gender, team_sport=sport, list1 = list1, len1 = len(list1))
        else:
            abort(400, description="No file submitted.")



    else:
        
        
        return render_template('home.html', processed = processed, team_name =team , team_year=year, team_gender=gender, team_sport=sport, list1 = list1, len1 = len(list1))


    return render_template('home.html',processed = processed, team_name =team , team_year=year, team_gender=gender, team_sport=sport, list1 = list1,len1 = len(list1))

@app.route('/processing')
def successful():
    return render_template('process.html')

if __name__ == '__main__':
    app.run(debug=True)
