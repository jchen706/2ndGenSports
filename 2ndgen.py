from flask import Flask, render_template, session, redirect, url_for, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER ='./uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

app.config['SECRET_KEY'] = 'my security sucks'

class MediaForm(FlaskForm):

    year = StringField('Year: ', validators = [DataRequired()])
    team = StringField('Team:', validators = [DataRequired()])
    sport =SelectField('Sport:', choices=[('foot', 'Football'),('basket', 'BasketBall')], validators = [DataRequired()] )
    gend = SelectField('Gender: ', choices=[('M','Male'), ('F','Female')], validators = [DataRequired()] )
    mediapdf = FileField('PDF:', validators=[FileRequired()])
    submit = SubmitField('Submit')

@app.route('/',methods = ['GET','POST'])
def index():
    year = False

    form = MediaForm()

    if form.validate_on_submit():

        session['year'] = form.year.data
        session['team'] = form.team.data
        session['sport'] = form.sport.data
        session['gend'] = form.gend.data
        session['mediapdf']= form.mediapdf.data


        form.year.data = ''
        form.team.data = ''
        form.sport.data = ''
        form.gend.data = ''
        form.mediapdf.file = ''
        return redirect(url_for('successful'))
    return render_template('home.html', form = form)

@app.route('/successful')
def successful():
    return render_template('successful.html')



if __name__ == '__main__':
    app.run()
