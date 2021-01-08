from flask import Flask
from flask import Flask, flash, redirect, render_template,url_for, request, session, abort
import os
import datetime
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

@app.route('/')
def home():
    return "go to login server"

@app.route('/signup', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      Session = sessionmaker(bind=engine) 
      s = Session()
      emails= request.form.get('email')
       
      users = s.query(User).filter(User.email.in_([emails]))
      r = users.first()
      if r:
          flash("Email already exist","danger")
          return render_template('sighup.html')
      else:     
        if not request.form['email'] or not  request.form['password']:
            flash('Please enter all the fields', 'error')
        else:
            data = User(request.form['email'], request.form['password'])
         
            session.add(data)
            session.commit()
            flash("Record was successfully added now login","success")
            return redirect(url_for('do_admin_login'))
   return render_template('sighup.html')

@app.route('/login', methods=['GET','POST'])
def do_admin_login():
    if request.method =='POST': 
        POST_EMAIL = str(request.form['email'])
        POST_PASSWORD = str(request.form['password'])

        Session = sessionmaker(bind=engine)
        s = Session()
        ems=s.query(User).filter(User.email.in_([POST_EMAIL]))
        em=ems.first()
        full = s.query(User).filter(User.email.in_([POST_EMAIL]), User.password.in_([POST_PASSWORD]) )
        final = full.first()
        if final:
            return redirect(url_for('profile'))
        else:
            if em:
                flash("Your password is wrong","danger")
                return render_template('login.html')
            else:
                flash("Email does not exist","danger")
                return render_template('login.html')
    return render_template('login.html')
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/profile")
def profile():
    
    return render_template('profile.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='127.0.0.1', port=5000)