from flask import Flask, render_template, request, flash,redirect
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail, Message
from flask_wtf import CSRFProtect 
import threading

# opening config file
with open("config.json", "r") as f:
    params = json.load(f)["params"]

app = Flask(__name__)
mail = Mail(app)
app.secret_key = b'_53oi3uriq9pifpff;apl'
csrf = CSRFProtect(app) 

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = params['user-name']
app.config['MAIL_PASSWORD'] = params['user-password']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# configuration database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///contact.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV'] = 'development'
db = SQLAlchemy(app)

# create contact model
class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"

# For database viewer (custom)
class ContactView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    form_columns = ["name","email", "desc", "data_created"]
    column_list = ["sno","name","email", "desc", "data_created"]

if app.config['ENV'] == 'development':
    # Enable Flask-Admin only in development
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
    # admin.add_view(ModelView(User, db.session))
    admin.add_view(ContactView(Contact,db.session))
    
else:
    # Disable Flask-Admin in other environments
    pass

# functions for mailing using threads
def mail_to_owner(msg):
    with app.app_context():
        mail.send(msg)

def mail_to_sender(msg):
    with app.app_context():
        mail.send(msg)

@app.route('/')
def hello_world():
    year = datetime.now().year
    return render_template("index.html", year=year)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            desc = request.form['desc']
            contact = Contact(name=name, email=email, desc=desc)
            db.session.add(contact)
            db.session.commit()      
            # mailing to owner
            owner = "luxmotivatelife@gmail.com"
            msg = Message(
                'Hello',
                sender = email,
                recipients = [owner]
                )
            msg.body = 'I am hero'
            msg.html = "<h1>mail send to owner</h1>"
            t1 = threading.Thread(target=mail_to_owner, args=[msg])
            t1.start()           

            # mailing to sender
            msg = Message(
                'Hello',
                sender = owner,
                recipients = [email]
                )
            msg.body = 'I am hero'
            msg.html = "mail send to sender"
            t1 = threading.Thread(target=mail_to_sender, args=[msg])
            t1.start()
        except Exception as e:
            flash("Some error occured while submiting your credential",e)
        else:
            flash("your credential submited successfully")
    return redirect("/")

# begin the app
if __name__=="__main__":
    app.run(debug="True", port=8000)