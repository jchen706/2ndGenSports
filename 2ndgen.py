import os
from werkzeug.utils import secure_filename

import PyPDF2
import json

from flask import Flask, render_template, session, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

#change this path to a folder for the upload
UPLOAD_FOLDER = 'C:/Users/jchen/Documents/2ndGenSports/static/pdfs'

ALLOWED_EXTENSIONS = {'txt'}
DEBUG = True
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my security sucks'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    year = False
    #form = MediaForm()

    if(request.method == "POST"):

        year = request.form['year']
        team = request.form['team']
        gender = request.form['gender']
        sport = request.form['sport']

        print(year)
        print(team)
        print(gender)
        print(sport)

        if request.files:

            file1 = request.files["pdffile"]

            if (file1.filename == ''):
                flash('No file selected')

            if(file1 and allowed_file(file1.filename)):
                file1.save(os.path.join(app.config['UPLOAD_FOLDER'], file1.filename))
                print('file save')

    else:
        return render_template('home.html')
    return render_template('home.html')

@app.route('/successful')
def successful():
    return render_template('successful.html')

if __name__ == '__main__':
    app.run(debug=True)
