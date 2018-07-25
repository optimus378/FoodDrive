from flask import Flask, render_template,request, redirect, url_for, flash, abort, send_file,abort,Response
from flask_httpauth import HTTPBasicAuth
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField, TextAreaField, FileField, HiddenField, IntegerField, RadioField
from wtforms.validators import InputRequired, Email, Length, NumberRange
from flask_wtf.file import FileAllowed, FileRequired
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
import datetime
import csv
import re
import json as JSON

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisISAScreent@!#$WRSDAFGW#$%&H'
Bootstrap(app)
app.config['MONGODB_SETTINGS'] = {
    'db': 'FoodDrive',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine(app)
## Authenticated USERS ##
users = {
    "foodadmin": "KWDrive45%"
}
auth = HTTPBasicAuth()
@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None
## Database ## 

class Agent(db.Document):
    marketcenter = db.StringField(required=True)
    email = db.EmailField(required = True)
    firstname = db.StringField(max_length=50)
    lastname = db.StringField(max_length=50)
    bagnumber = db.IntField(max_value=5000, precision=0)
    streets = db.ListField()
    created_at = db.DateTimeField(default=datetime.datetime.now, editable=False,)


##FORMS ##
class RegForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'),Length(max=50)])
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    marketcenter = RadioField('Market Center', choices = [('SWMC', 'KW Austin Southwest'),('NWMC','KW Austin Northwest')], default ='SWMC')
    streetspicker = StringField('Find Streets')
    streets = HiddenField()
    bagnumber = IntegerField('Number of Bags' ,validators=[InputRequired(),NumberRange(0,5000)])

@app.route('/modal')
def modal():
    return render_template('modal.html')

@app.route('/', methods = ['GET','POST'])
def newform():
    form = RegForm()
    if form.validate_on_submit():
            streetjson = JSON.loads(form.streets.data)
            streets = [d['street'] for d in streetjson]
            agent = Agent(email=form.email.data.lower(),
                          firstname= form.firstname.data,
                          lastname = form.lastname.data,
                          bagnumber=form.bagnumber.data,
                          marketcenter = form.marketcenter.data,
                          streets=streets)
            agent.save()
            return render_template('editsuccess.html', form = form)
    return render_template('newform.html' ,form = form)

@app.route('/agentpage/<agentemail>', methods = ['GET','POST'])
def agentpage(agentemail):
    query= Agent.objects.get(email=agentemail)
    form = RegForm(marketcenter=query.marketcenter)
    marketcenter = query.marketcenter
    streets= query.streets
    bags = query.bagnumber
    email = query.email
    firstname = query.firstname
    lastname = query.lastname
    if form.validate_on_submit():
        if not form.streets.data:
            streets=[]
            agent = Agent.objects(email=form.email.data).modify(upsert=True,
                          set__firstname= form.firstname.data,
                          set__lastname = form.lastname.data,
                          set__bagnumber=form.bagnumber.data,
                          set__marketcenter = form.marketcenter.data,
                          push__streets=streets,
                          set__email=form.email.data)
            agent.save()
            flash('Updated '+ agent.email+'.', 'info')
            return render_template('agentpage.html', form = form, streets=streets,marketcenter=marketcenter,bags=bags, email= email, firstname=firstname,lastname=lastname, message='')
        else:
            print(form.streets.data)
            streetjson = JSON.loads(form.streets.data)
            streets = [d['street'] for d in streetjson]
            agent = Agent.objects(email=form.email.data).modify(upsert=True,
                          set__firstname= form.firstname.data,
                          set__lastname = form.lastname.data,
                          set__bagnumber=form.bagnumber.data,
                          set__marketcenter = form.marketcenter.data,
                          set__streets=streets,
                          set__email=form.email.data)
            agent.save()
            flash('Updated '+ agent.email+'.','info')
            return render_template('agentpage.html', form = form, streets=streets,marketcenter=form.marketcenter.data,bags=bags, email= email, firstname=firstname,lastname=lastname, message='')
    return render_template('agentpage.html', form = form, streets=streets,marketcenter=marketcenter,bags=bags, email= email, firstname=firstname,lastname=lastname, message='')
    
@app.route('/backend')
@auth.login_required
def backend():
    query = Agent.objects()
    return render_template('backend.html' ,query = query,)

@app.route('/backend/<agentemail>', methods = ['GET','POST'])
@auth.login_required
def backendedit(agentemail):
    query= Agent.objects.get(email=agentemail)
    form = RegForm(marketcenter=query.marketcenter)
    marketcenter = query.marketcenter
    streets= query.streets
    bags = query.bagnumber
    email = query.email
    firstname = query.firstname
    lastname = query.lastname
    if form.validate_on_submit():
        if not form.streets.data:
            streets=[]
            agent = Agent.objects(email=form.email.data).modify(upsert=True,
                          set__firstname= form.firstname.data,
                          set__lastname = form.lastname.data,
                          set__bagnumber=form.bagnumber.data,
                          set__marketcenter = form.marketcenter.data,
                          push__streets=streets,
                          set__email=form.email.data)
            agent.save()
            flash('Updated '+ agent.email+'.')
            return redirect('/backend')
        else:
            print(form.streets.data)
            streetjson = JSON.loads(form.streets.data)
            streets = [d['street'] for d in streetjson]
            agent = Agent.objects(email=form.email.data).modify(upsert=True,
                          set__firstname= form.firstname.data,
                          set__lastname = form.lastname.data,
                          set__bagnumber=form.bagnumber.data,
                          set__marketcenter = form.marketcenter.data,
                          set__streets=streets,
                          set__email=form.email.data)
            agent.save()
            flash('Updated '+ agent.email+'.')
            return redirect('/backend')
    return render_template('backendagent.html', form = form, streets=streets,marketcenter=marketcenter,bags=bags, email= email, firstname=firstname,lastname=lastname, message='')

@app.route('/api/deleteagent/<email>', methods = ['GET'])
@auth.login_required
def deleteuser(email):
    agent = Agent.objects.get(email=email)
    agent.delete()
    flash("Agent Deleted.")
    return redirect('/backend')

@app.route('/api/checkstreet/<street>', methods = ['GET'])
def checkstreet(street):
    try:
        query = Agent.objects.get(streets=street[:-9])
        return Response(status=200)
    except:
        return Response(status=404)
## This code needs to be updated. There's no Check for a Down Database. 

@app.route('/api/checkemail/<email>', methods = ['GET'])
def checkemail(email):
    try:
        query = Agent.objects.get(email=email)
        return Response(status=200)
    except:
        return Response(status=404)


@app.route('/api/export/<marketcenter>')
def exportcsv(marketcenter):
    if marketcenter == "ALL":
        query = Agent.objects()
    else:
        query = Agent.objects(marketcenter=marketcenter)
    querylen = len(query)
    with open('static/'+marketcenter+'.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerow(["First Name", "Last Name", "Email", "Streets", "Bags","Submission Date", "Marketcenter"])
        mc = [query[i]['marketcenter'] for i in range(0,querylen)]
        firstname = [query[i]['firstname'] for i in range(0,querylen)]
        lastname = [query[i]['lastname']for i in range(0,querylen)]
        email = [query[i]['email']for i in range(0,querylen)]
        streets = [query[i]['streets']for i in range(0,querylen)]
        bagnumber = [query[i]['bagnumber']for i in range(0,querylen)]
        created_at = [query[i]['created_at']for i in range(0,querylen)]
        formattedDate = [datetime.datetime.isoformat(i, sep='-', timespec='minutes') for i in created_at]
        queryzip=zip(firstname,lastname,email,streets,bagnumber,formattedDate,mc)
        for row in (queryzip):
            writer.writerow(row)
        writer.writerow([""])
        writer.writerow(["", "", "", "Total Bags", sum(bagnumber)])
    return send_file('static/'+marketcenter+'.csv', as_attachment=True)

if __name__ == '__main__':
    app.run()