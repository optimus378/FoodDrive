from flask import Flask, Blueprint, render_template,request, redirect, url_for, flash, abort, send_file,abort,Response, make_response
from flask_httpauth import HTTPBasicAuth
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField, TextAreaField, FileField, HiddenField, IntegerField, RadioField, ValidationError
from wtforms.validators import InputRequired, Email, Length, NumberRange
from flask_wtf.file import FileAllowed, FileRequired
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
import datetime
import io
import csv
import re
import json as JSON
from fooddrive.models import Agent


root = Blueprint('root', __name__,template_folder='templates/root')

## Authenticated USERS ##
users = {
    "foodadmin": "Apassword!"
}
auth = HTTPBasicAuth()
@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


##FORMS ##
    ## Custom Validator ##
def bag_multiple_check(form, field):
        x = field.data
        if x % 50 != 0:
            raise ValidationError('Bags must be in multiples of 50')
        return
        

class RegForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email'),Length(max=50)])
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    marketcenter = RadioField('Market Center', choices = [('SWMC', 'KW Austin Southwest'),('NWMC','KW Austin Northwest')], default ='SWMC')
    streetspicker = StringField(label = 'Find Streets')
    streets = HiddenField()
    bagnumber = IntegerField(label = 'Number of Bags' ,validators=[InputRequired(),NumberRange(0,2000), bag_multiple_check])



@root.route('/modal')
def modal():
    return render_template('root/modal.html')

@root.route('/', methods = ['GET','POST'])
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
            return render_template('root/editsuccess.html', form = form , email=form.email.data)
    return render_template('root/newform.html' ,form = form)

@root.route('/agentpage/<agentemail>', methods = ['GET','POST'])
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
            flash('Successfully Updated '+ agent.email+'.', 'info')
            return render_template('root/editsuccess.html', email = email)
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
            flash('Successfully Updated '+ agent.email+'.','info')
            return render_template('root/editsuccess.html', email = email)
    return render_template('root/agentpage.html', form = form, streets=streets,marketcenter=marketcenter,bags=bags, email= email, firstname=firstname,lastname=lastname, message='')
    
@root.route('/backend')
@auth.login_required
def backend():
    query = Agent.objects()
    return render_template('root/backend.html' ,query = query,)

@root.route('/backend/<agentemail>', methods = ['GET','POST'])
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
            return redirect('root/backend')
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
            return redirect('root/backend')
    return render_template('root/backendagent.html', form = form, streets=streets,marketcenter=marketcenter,bags=bags, email= email, firstname=firstname,lastname=lastname, message='')

@root.route('/deleteagent/<email>', methods = ['GET'])
@auth.login_required
def deleteuser(email):
    agent = Agent.objects.get(email=email)
    agent.delete()
    flash("Agent Deleted.")
    return redirect(url_for('root.backend'))

@root.route('/api/checkstreet/<street>', methods = ['GET'])
def checkstreet(street):
    try:
        Agent.objects.get(streets=street[:-9])
        return Response(status=200)
    except:
        return Response(status=404)
## This code needs to be updated. There's no Check for a Down Database. 

@root.route('/api/checkemail/<email>', methods = ['GET'])
def checkemail(email):
    try:
        Agent.objects.get(email=email)
        return Response(status=200)
    except:
        return Response(status=404)


@root.route('/api/export/<marketcenter>')
def exportcsv(marketcenter):
    if marketcenter == "ALL":
        query = Agent.objects()
    else:
        query = Agent.objects(marketcenter=marketcenter)
    querylen = len(query)
    si = io.StringIO()
    writer = csv.writer(si, delimiter=',', lineterminator='\n')
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
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename="+marketcenter+".csv"
    output.headers["Content-type"] = "text/csv"
    return output
