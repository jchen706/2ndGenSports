from flask import Flask, render_template, session, redirect, url_for, request, abort, flash, stream_with_context, Response, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
import os
from werkzeug.utils import secure_filename

import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import TweetTokenizer, sent_tokenize

import json


import tika
#tika.initVM()
from tika import parser


import re

from nltk.tokenize import sent_tokenize
from dynamo import *




from scraper import *
from s3 import * 
from scraperdynamo import *

#from flask_sqlalchemy import SQLAlchemy
#import SQLAlchemy 

import time 
from rq import Queue 
from rq.job import Job 
from redis import Redis
from worker import conn 

import jinja2 
import sys

q = Queue(connection=conn)

#absolute path of the file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#change this path to a folder for the upload
UPLOAD_FOLDER = '/static/pdfs'

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


keyWordList = ['parent','parents', 'father', 'mother', 'dad', 'mom', 'son', 'daughter']


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

            if (file1.filename == ''):
                flash('No file selected')

            if(file1 and allowed_file(file1.filename)):
                file1.save(os.path.join(app.config['UPLOAD_FOLDER'], file1.filename))
                print('file save')


            return redirect(request.url)

    return render_template("uploadpdf.html")


def workerParser(file_path, file):   


    upload_file(file.filename,file)
    s3_obj = dowload_file(file.filename, os.path.join(file_path, file.filename))


    return parser.from_file(os.path.join(file_path, file.filename))


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

    #database server connection ... for MySQL
    # try:
    #     connection = mysql.connector.connect(host='localhost',
    #                                      database='sportgen',
    #                                      user='root',
    #                                      password='1547')

    #     if connection.is_connected():
    #         db_Info = connection.get_server_info()
    #         print("Connected to MySQL Server version ", db_Info)
    #         cursor = connection.cursor()
    #         cursor.execute("select database();")
    #         record = cursor.fetchone()
    #         print("You're connected to database: ", record)
    # except Error as e:
    #     print("Error while connecting to MySQL", e)
    # finally:
    #     if (connection.is_connected()):
    #         cursor.close()
    #         connection.close()
    #         print("MySQL connection is closed")


    #action posted from frontend 

    print("right before post method check")
    if(request.method == "POST"):
        print("right after post medthod check")
        if request.form['action'] == "submit":

            print("past submit action form check")

            isGetPreviousResults = False

            checkedList = []
            year = request.form['year']
            team = request.form['team']
            gender = request.form['gender']
            sport = request.form['sport']
            processed = True

            print("past attribute retrieval from form")



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
                print("right before accessing pdffile")

                file1 = request.files["pdffile"]
                print(file1.filename == '') 

                print("right after pdffile")

                if (file1.filename == ''):
                    flash('No file selected')
                    abort(400, description="No file submitted.")

                print(allowed_file(file1.filename))
                if(allowed_file(file1.filename)):

                    # upload_file(file1.filename,file1)
                    # s3_obj = dowload_file(file1.filename, os.path.join(file_path, file1.filename))

                    #file1.save(os.path.join(file_path, file1.filename))
                    #file = open(os.path.join(file_path, file1.filename), 'r')
                    #parsed = parser.from_file(s3_obj['Body'].read().decode(encoding="utf-8",errors="ignore"))


                    job = q.enqueue(workerParser, file_path, file1) 


                    return redirect(url_for('workerProcessPDF', jobId = job.id, year = year, gender = gender, sport = sport, team = team))


            else:
                abort(400, description="No file submitted.")

        elif request.form['action'] == "getPreviousResults":


            isGetPreviousResults = True

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


            keyWordCountDict = {}
            try:
                item = getItem(sport, team, year, gender)
            except KeyError as e:
                return render_template('402.html')


            checkedList = item["checkedList"]
            resultsList = item["resultsList"]

            for aSentence in resultsList:
                for each in keyWordList:
                    if each in aSentence.lower().split():

                        if (each in keyWordCountDict):
                            keyWordCountDict[each] += 1
                        else:
                            keyWordCountDict[each] = 1

            return render_template('home.html', processed = processed, isGetPreviousResults = isGetPreviousResults, team_name =team , team_year=year, team_gender=gender, team_sport=sport, list1 = resultsList, len1 = len(resultsList), checkedList = checkedList, keyWordList = keyWordList, keyWordCountKeys = keyWordCountDict.keys(), keyWordCountDict = keyWordCountDict)




    else:


        return render_template('home.html', processed = processed, team_name =team , team_year=year, team_gender=gender, team_sport=sport, list1 = list1, len1 = len(list1))


    return render_template('home.html',processed = processed, team_name =team , team_year=year, team_gender=gender, team_sport=sport, list1 = list1,len1 = len(list1))

@app.route('/workerProcessPDF') 
def workerProcessPDF(): 

    jobId = request.args.get("jobId") 
    year = request.args.get("year") 
    gender = request.args.get("gender")
    sport = request.args.get("sport")
    team = request.args.get("team")

    # try:
    #     return_dict = base_scraper(roster_url, base_url)
    # except:
    #     return render_template('404.html')


    job = Job.fetch(jobId, connection=conn) 
    status = job.get_status() 

    if status != 'finished':
        return get_template(refresh = True)  
    else:

        processed = True 
        isGetPreviousResults = False  


        parsed = job.result 

        input_text = parsed['content']

        tokenizer_words = TweetTokenizer()
        tokens_sentences = [tokenizer_words.tokenize(t) for t in nltk.sent_tokenize(input_text)]
        #print(tokens_sentences)

        count = 0

        wantedList=['parent','Parents', 'Father', 'Mother', 'father', 'mother', 'dad', 'Dad', 'Mom', 'mom', 'son', 'Son', 'daughter', 'Daughter']

        wantedListDictionary = {}
        count1 = 0
        wantedListSentences = []

        #keeps track of the count of each keyword. Key: "keyword", Value: "count". Note that similar keywords like parent and Parents fall under the same key.
        keyWordCountDict = {}

        import csv
        with open('employee_file.csv', mode='w', encoding='utf-8', newline='') as employee_file:
                employee_writer = csv.writer(employee_file, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                employee_writer.writerow(tokens_sentences)

        for i in range(len(tokens_sentences)):
            wantedListDictionary[count1] = []
            eachSentence = tokens_sentences[i]
            #punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            import string
            #file3 = open('newfile.txt', "w")
            #file3.writelines(", ".join(str(x) for x in eachSentence))

            # foundKeyWord = False
            hits=[]
            for each in wantedList:
                if each in eachSentence:
                    print(eachSentence)
                    hits.append(eachSentence)
                    with open('sentence.csv', mode='w', encoding='utf-8', newline='') as sen_file:
                        employee_writer = csv.writer(sen_file, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        employee_writer.writerow(hits)

                # if not foundKeyWord:


                    #print(" ")
                    #print(" ")
                    if eachSentence[len(eachSentence)-2] == "No":
                        #print(tokens_sentences[i+1])
                        #print(eachSentence)
                        eachSentence.extend(tokens_sentences[i+1])
                        #print(eachSentence)


                    aSentence =' '.join(eachSentence)
                    #print(aSentence)
                    wantedListDictionary[count1].append(aSentence)
                    count1+=1
                    wantedListSentences.append(aSentence)
                    # foundKeyWord = True

                # if (each.lower() in keyWordCountDict):
                #     keyWordCountDict[each.lower()] += 1
                # else:
                #     keyWordCountDict[each.lower()] = 1


                    break
        #print(wantedListSentences)

        with open('sentence2.csv', mode='w', encoding='utf-8', newline='') as sen1_file:
                        employee_writer = csv.writer(sen1_file, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        employee_writer.writerow(wantedListSentences)


        cuttedWantedListDictionary = {}
        sente = []
        for j in range(len(wantedListSentences)):
             cuttedWantedListDictionary[j] = []
             shortenedSentences = wantedListSentences[j].split(' ')
             #print(shortenedSentences)
             for i in range(len(shortenedSentences)):
                 for eachword in wantedList:
                        if (eachword == shortenedSentences[i]):
                           if (eachword.lower()=='son') or (eachword.lower()=='daughter'):
                               if(shortenedSentences[i+1] != 'of'):
                                   continue

                           #hortenedSentences[i] = eachword
                           if (len(shortenedSentences) < 36):
                               #print(11111)
                               #print(eachword)
                               cuttedWantedListDictionary[j].append(shortenedSentences)
                               sente.append(shortenedSentences+[1,1,1,1])
                               break
                           else:
                             try:
                                 #print(list33[i-15:i+20])
                                 #print(22222)
                                 #print(eachword)
                                 #print(i)
                                 #print(len(shortenedSentences))
                                 a = shortenedSentences[i:50]
                                 if i > 17:
                                    a = shortenedSentences[i-15:i+20]
                                 #print(a)
                                 cuttedWantedListDictionary[j].append(a)
                                 sente.append(a+[2,2,2,2])

                             except:
                                #print(333333)
                                #print(eachword)
                                a = shortenedSentences[i:]
                                #print(a)
                                cuttedWantedListDictionary[j].append(a)
                                sente.append(a+[3,3,3,3])

                                #dic[count].append(a)

        #print('hereeeee')

        with open('sentence3.csv', mode='w', encoding='utf-8', newline='') as sen3_file:
                        employee_writer = csv.writer(sen3_file, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        employee_writer.writerow(sente)

        #print(cuttedWantedListDictionary)
        list33 = []
        #print(len(cuttedWantedListDictionary))

        for key in cuttedWantedListDictionary:
            for ij in range(len(cuttedWantedListDictionary[key])):
                 if(len(cuttedWantedListDictionary[key][0]) > 0):
                    aSentence =' '.join(cuttedWantedListDictionary[key][0])
                     #print(aSentence)


                    list33.append(aSentence.strip())

                    for each in keyWordList:
                        if each in aSentence.lower().split():

                            if (each in keyWordCountDict):
                                keyWordCountDict[each] += 1
                            else:
                                keyWordCountDict[each] = 1
                    break


        return render_template('home.html', processed = processed, isGetPreviousResults = isGetPreviousResults, team_name =team , team_year=year, team_gender=gender, team_sport=sport, list1 = list33, len1 = len(list33), keyWordList = keyWordList, keyWordCountKeys = keyWordCountDict.keys(), keyWordCountDict = keyWordCountDict)




@app.route('/processing')
def successful():
    return render_template('process.html')



@app.route('/postCheckList',methods = ['POST', 'GET'])
def postCheckList():
    print('here post check list')

    if(request.method == "POST"):
        year = None
        team = None
        gender = None
        sport = None
        team = request.form['teamName']
        year = request.form['teamYear']
        sport = request.form['teamSport']
        gender = request.form['gender']
        list1 = request.form.getlist('checkboxVal')
        resultsList = request.form.getlist('result')
        count = len(list1)
        teamid = sport+team+str(year)

        print(sport)
        print(team)
        print(year)
        print(count)





        keyWordCountDict = {}
        for aSentence in list1:

            for each in keyWordList:

                if each in aSentence.lower().split():

                    if (each in keyWordCountDict):
                        keyWordCountDict[each] += 1
                    else:
                        keyWordCountDict[each] = 1


        added = False
        putItem(sport,team,year,count, keyWordCountDict, list1, resultsList, gender)

        added = True
        item1 = getItem(sport,team, year, gender)
        item1 = [item1]




        return render_template('postedList.html', added1 = added , items = item1, keyWordList = keyWordList, keyWordCountKeys = keyWordCountDict.keys(), keyWordCountDict = keyWordCountDict)
    else:
        return render_template('postedList.html', teamId="nothing is processed")


    return render_template('postedList.html', teamId="nothing is processed")


@app.route('/getAll', methods = ['GET'])
def getAllData():




    if(request.method == "GET"):
        items = getAllItems()
        added = False

        return render_template('postedList.html', added1 = added, items = items, keyWordList = keyWordList)


@app.route('/getScraperData', methods = ['GET'])
def getAllScraperData():




    if(request.method == "GET"):
        items = scrapergetAllItems()
        added = False

        return render_template('postedScraper.html', added1 = added, items = items, keyWordList = keyWordList)

@app.route('/getScraper', methods= ['GET'])
def getScraper():
    url = None
    #url = request.form['input_url']
    #print(url)

    if(request.method == 'GET'):
        return render_template('scraperx.html')

@app.route('/postscraper',methods = ['GET','POST'])
def processScraper():
    #URL = 'https://mgoblue.com/sports/mens-basketball/roster'

    base_url = None
    url = None
    processed = False


    if(request.method == "POST"):
        roster_url = request.form['roster_input_url']
        base_url = request.form['base_url']
        #format_type = request.form['format']
        year = request.form['year']
        gender = request.form['gender']
        sport = request.form['sport']
        team = request.form['team']


        error_scraper = False 
        processed = True 


        roster_url = str(roster_url)
        base_url = str(base_url)
        #format_type = str(format_type)

        print(roster_url)
        print(base_url)
        #print(format_type)

        return_dict = None 
        

        try: 
            job = q.enqueue(base_scraper, roster_url, base_url)
            # return_dict = base_scraper(roster_url, base_url)
        except:
            return render_template('404.html')


        # while job.result == None:
        #     time.sleep(5) 

        # return_dict = job.result 

        return redirect(url_for('workerProcessScraper', jobId = job.id, year = year, gender = gender, sport = sport, team = team))


    else:
        return render_template('scraperx.html', teamId="nothing is processed", processed=processed)



    return render_template('scraperx.html', teamId="nothing is processed", processed=processed) 


def get_template(refresh=False): 
    template_str = '''<html>
    <head>
      {% if refresh %}
        <meta http-equiv="refresh" content="5">
      {% endif %} 

      <style>
        .loader {
          position: absolute;
          left: 50%;
          top: 50%;
          z-index: 1;
          width: 150px;
          height: 150px;
          margin: -75px 0 0 -75px;
          border: 16px solid #f3f3f3;
          border-radius: 50%;
          border-top: 16px solid #3498db;
          width: 120px;
          height: 120px;
          -webkit-animation: spin 2s linear infinite;
          animation: spin 2s linear infinite;
        }  

        /* Safari */
        @-webkit-keyframes spin {
          0% { -webkit-transform: rotate(0deg); }
          100% { -webkit-transform: rotate(360deg); }
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        select {
          margin-left: 5px;
          margin-right: 5px;
        }
      </style>
    </head>
    <body>
    <div align="center">
      <div id ="loaderid" class="loader"></div>
    </div>
    </body>
    </html>'''
    return render_template_string(template_str, refresh=refresh)

@app.route('/workerProcessScraper')
def workerProcessScraper():

    error_scraper = False 
    processed = True  
    
    jobId = request.args.get("jobId") 
    year = request.args.get("year") 
    gender = request.args.get("gender")
    sport = request.args.get("sport")
    team = request.args.get("team")

    # try:
    #     return_dict = base_scraper(roster_url, base_url)
    # except:
    #     return render_template('404.html')


    job = Job.fetch(jobId, connection=conn) 
    status = job.get_status() 

    if status != 'finished':
        return get_template(refresh = True) 
    else: 

        return_dict = job.result

        if return_dict == None:

            return render_template('scraperx.html', teamId="nothing is processed", processed=processed)





        if error_scraper:

            return render_template('scraperx.html', teamId="nothing is processed", processed=processed)

        else:

            true_dict = return_dict.copy()
            for key1, value in true_dict.items():
                if len(value) == 0:
                    return_dict.pop(key1, None)




            keyWordCountDict = {}
            for key, value in return_dict.items():

                for each in keyWordList:

                    for bullet in value:

                        if each in bullet.lower().split():

                            if (each in keyWordCountDict):
                                keyWordCountDict[each] += 1
                                print("found " + each + " for " + key)
                                break
                            else:
                                keyWordCountDict[each] = 1
                                print("found " + each + " for " + key)
                                break


           
            # env = jinja2.Environment(
            #     loader=jinja2.FileSystemLoader("./templates")
            # )
            # template = env.get_template("scraperx.html")

            return render_template('scraperx.html', returnTeam=return_dict, processed=processed,
                team_name =team , team_year=year, team_gender=gender, team_sport=sport, keyWordList = keyWordList,
                keyWordCountKeys = keyWordCountDict.keys(), keyWordCountDict = keyWordCountDict, length_dict = len(return_dict))

            # return template.render(returnTeam=return_dict, processed=processed,
            #     team_name =team , team_year=year, team_gender=gender, team_sport=sport, keyWordList = keyWordList,
            #     keyWordCountKeys = keyWordCountDict.keys(), keyWordCountDict = keyWordCountDict, length_dict = len(return_dict))


@app.route('/postScraperCheck',methods = ['POST', 'GET'])
def postCheckListScraper():


    if(request.method == "POST"):
        year = None
        team = None
        gender = None
        sport = None
        team = request.form['teamName']
        year = request.form['teamYear']
        sport = request.form['teamSport']
        list1 = request.form.getlist("checkboxVal")
        gender = request.form['gender']
        newDict = {}
        import ast
        for i in range(len(list1)):
            #list1[i] = list1[i].replace("\'", "\"")
            print(list1[i])
            ab = ast.literal_eval(list1[i])
            newDict.update(ab)

        #diction = json.loads(list1)

        resultsList = request.form.getlist('result')
        count = len(list1)
        teamid = sport+team+str(year)

        print(sport)
        print(team)
        print(year)
        print(count)
        print("list $$$$")
        print(list1)
        print("result $$$$$$$")
        #print(newDict)





        keyWordCountDict = {}
        for aSentence in list1:

            for each in keyWordList:

                if each in aSentence.lower().split():

                    if (each in keyWordCountDict):
                        keyWordCountDict[each] += 1
                    else:
                        keyWordCountDict[each] = 1


        added = False
        scraperputItem(sport,team,year,count, newDict, keyWordCountDict, gender)

        added = True
        item1 = scrapergetItem(sport,team, year,gender)
        item1 = [item1]
        print(item1)




        return render_template('postedScraper.html',teamId="nothing is processed",added1=added, items = item1, teamDict=item1[0]['teamDict'], keyWordList = keyWordList, keyWordCountKeys = keyWordCountDict.keys(), keyWordCountDict = keyWordCountDict)
    else:
        return render_template('postedScraper.html', teamId="nothing is processed")


    return render_template('postedScraper.html', teamId="nothing is processed")

@app.route('/deleteAll', methods= ['POST', 'GET'])
def deleteAll():


    if(request.method == 'POST'):


        list1 = request.form.getlist("deleteCheck")
        for id in list1:
            deleteItem(id)

        items = getAllItems()
        added = False

        return render_template('postedList.html', added1 = added, items = items, keyWordList = keyWordList) 
    elif(request.method == 'GET'): 
        
        items = getAllItems() 
        added = False 

        return render_template('postedList.html', added1 = added, items = items, keyWordList = keyWordList)


@app.route('/deleteAllScraper', methods= ['POST', 'GET'])
def deleteAllScraper():


    if(request.method == 'POST'):


        list1 = request.form.getlist("deleteCheck")
        for id in list1:
            scraperdeleteItem(id)

        items = scrapergetAllItems()
        added = False

        return render_template('postedScraper.html', added1 = added, items = items, keyWordList = keyWordList) 
    elif(request.method == 'GET'): 
        
        items = scrapergetAllItems() 
        added = False 

        return render_template('postedScraper.html', added1 = added, items = items, keyWordList = keyWordList)




if __name__ == '__main__':
    app.run(debug=True)