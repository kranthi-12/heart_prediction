#Important Modules
from flask import Flask,render_template, url_for ,flash , redirect
from forms import RegistrationForm, LoginForm
from flask import request
import numpy as np
import pickle
import email_validator
import os
import yaml
#from this import SQLAlchemy
app=Flask(__name__,template_folder='templates')

app.secret_key = '1a2b3c4d5e'

# RELATED TO THE SQL DATABASE
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
#FOR THE FIRST MODEL


# home page

#@app.route('/')
#def home():
 #  return render_template('index.html')






@app.route("/")

@app.route("/home")
def home():
    return render_template("home.html")
 
@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/heart")
def heart():
    return render_template("heart.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    form =RegistrationForm()
    if form.validate_on_submit():
        #flash("Account created for {form.username.data}!".format("success"))
        flash("Account created","success")      
        return redirect(url_for("home"))
    return render_template("register.html", title ="Register",form=form )
@app.route("/login", methods=["POST","GET"])
def login():
    form =LoginForm()
    if form.validate_on_submit():
        #if form.email.data =="sho" and form.password.data=="password":
        flash("You Have Logged in !","success")
        return redirect(url_for("home"))
    #else:
    #   flash("Login Unsuccessful. Please check username and password","danger")
    return render_template("login.html", title ="Login",form=form )
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,11)
    loaded_model = pickle.load(open("rf_model.pkl", "rb")) 
    result = loaded_model.predict(to_predict)
    return result[0]
    
@app.route('/result',methods = ["GET","POST"])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        result = ValuePredictor(to_predict_list)
        if int(result)==1:
            prediction='HEART STROKE'
        else:
            prediction='Healthy'       
    return(render_template("result.html", prediction=prediction))


if __name__ == "__main__":
    app.run(debug=True)
