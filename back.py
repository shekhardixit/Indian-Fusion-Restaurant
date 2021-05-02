# pylint: disable=no-member
from flask import Flask, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

class Login(db.Model):
    __tablename__ = "login"
    sno = db.Column(db.Integer(), primary_key=True)
    emailid = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(10), nullable=False)  

class Contact(db.Model):
    __tablename__ = "contact"
    cid = db.Column(db.Integer(), primary_key=True)
    cfname = db.Column(db.String(20), nullable=False)
    clname = db.Column(db.String(20), nullable=False)
    ctcode = db.Column(db.Integer(), primary_key=True)
    ctnum = db.Column(db.Integer(), primary_key=True)
    cemail = db.Column(db.String(30), nullable=False)
    cfeedback = db.Column(db.String(300), nullable=False)
    fdate = db.Column(db.String(12), nullable=True)
    

@app.route("/", methods=["GET","POST"])
def login_page():
    if (request.method == "POST"):
    	#Fetch entry for database
        email = request.form.get('email')
        pwd = request.form.get('pwd')

        #Enter fetched data to database (class_Login=fetching_data_name)
        entry = Login(emailid=email, password=pwd)
        db.session.add(entry)
        db.session.commit()
        if email==params['admin_user'] and pwd==params['admin_password']:
            # setting session variable
            session['user'] = email
            session['pass'] = pwd
            return render_template("review.html", params=params)
    return render_template('index.html', params=params)
    

@app.route('/about')
def about():
    return render_template('aboutus.html', params=params)

@app.route('/contact', methods=["GET","POST"])
def contact_page():
    if (request.method == "POST"):
    	#Fetch entry for database(fetching_data_name= input_name_in_htmlcode)
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        tcode = request.form.get('areacode')
        tnum = request.form.get('telnum')
        email = request.form.get('emailid')
        feedback = request.form.get('feedback')

        #Enter fetched data to database (class_Login=fetching_data_name)
        entry = Contact(cfname=fname, clname=lname, ctcode=tcode, ctnum=tnum, cemail=email, cfeedback=feedback)
        db.session.add(entry)
        db.session.commit()
        
    return render_template('contactus.html', params=params)

@app.route("/review", methods=["GET"])
def reviewus_page():
    reviews = Contact.query.filter_by().all()[0:params['no_of_posts']]
    cnt = len(reviews)
    return render_template('review.html', params=params, reviews=reviews, cnt=cnt)

app.run(debug=True)
    