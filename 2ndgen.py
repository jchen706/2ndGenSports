from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my security sucks'

class MediaForm(FlaskForm):

    year = StringField('Year: ', validators = [DataRequired()])
    team = StringField('Team:', validators = [DataRequired()])
    sport =SelectField('Sport:', choices=[('foot', 'Football'),('basket', 'BasketBall')], validators = [DataRequired()] )
    gend = SelectField('Gender: ', choices=[('M','Male'), ('F','Female')], validators = [DataRequired()] )
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

        form.year.data = ''
        form.team.data = ''
        form.sport.data = ''
        form.gend.data = ''
        return redirect(url_for('successful'))
    return render_template('home.html', form = form)

@app.route('/successful')
def successful():
    return render_template('successful.html')

if __name__ == '__main__':
    app.run()
