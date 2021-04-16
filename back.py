from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ristoranteb4'
db = SQLAlchemy(app)

class Login(db.Model):
    __tablename__ = "login"
    sno = db.Column(db.Integer(), primary_key=True)
    emailid = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    

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
    return render_template('index.html')
    

@app.route('/about')
def about():
    return render_template('aboutus.html')

@app.route('/contact')
def contact():
    return render_template('contactus.html')

app.run(debug=True)
    