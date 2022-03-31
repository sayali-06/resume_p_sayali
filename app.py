#importing libraries
from flask import Flask, render_template, session, request, redirect, flash, jsonify
from flask.helpers import url_for
from flask.wrappers import Request
from flask_login.utils import logout_user
from flask_pymongo import PyMongo
import bcrypt
from passlib.hash import pbkdf2_sha256
from flask_login import login_required
from flask_mongoengine import MongoEngine
from werkzeug.utils import secure_filename
import os, textract,docx2txt
from pdfminer.high_level import extract_text
from nltk.corpus import stopwords
from asyncio.windows_events import NULL
import requests
import json
import numpy as np
import pandas as pd
from pandas import json_normalize # easy JSON -> pd.DataFrame
import re
import json
from resuumes import extract_name
from resumeskill import extract_skills
from education2 import extract_education





#intialize app
app= Flask(__name__, template_folder='templates') 

#connecting with mongo
app.config['MONGO_DBNAME'] = 'resume'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/resume'
app.secret_key = 'sayali'
mongo = PyMongo(app)

db = MongoEngine()
db.init_app(app)   

#file
UPLOAD_FOLDER = ''
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg','html','docx','doc'])

# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))
EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 'B.COM','BAS','B.Arch.','BA','BFA'
            'ME', 'M.E', 'M.E.', 'M.S','Masters' ,'MBA','MFA','M.Ed.','MPA','MPH','MSW','M.Pub.',
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII','B.Ed','AAS','AA','AS'
        ]

def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
   
#class User(db.Document):
 #   name = db.StringField()
  #  email = db.StringField()
   # profile_pic = db.StringField()

@app.route('/')
def home():
    return render_template('home.html')

#candidate login
@app.route('/cand_login')
def cand_log():
    return render_template('candidate_login.html')

#company_login
@app.route('/comp_login')
def companylogin():
    return render_template('company_login.html')

#candidate_login
@app.route('/candidate_login',methods=['POST','GET'])
def candidate():
    if request.method=='POST':
        user= mongo.db.candidate
        login_user = user.find_one({'username':request.form['username']})
        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'),login_user['password']) == login_user['password']:
                print("pass: ",bcrypt.hashpw(request.form['password'].encode('utf-8'),bcrypt.gensalt()))
                session['username'] = request.form['username']
                return render_template('upload.html')
            return 'invalid password'
        return 'signup first'   
    return render_template('candidate_login.html')

#company_login
@app.route('/company_login',methods=['POST','GET'])
def compcandidate():
    if request.method=='POST':
        user= mongo.db.company
        login_user = user.find_one({'username':request.form['username']})
        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'),login_user['password']) == login_user['password']:
                session['username'] = request.form['username']

                return render_template('company_homee.html')
            return 'invalid password'
        return 'signup first'   
    return render_template('company_login.html')
    
#candidate register
@app.route('/cand_register')
def cand_reg():
    return render_template('candidate_register.html')

#company register
@app.route('/comp_register')
def comp_reg():
    return render_template('company_register.html')


#candidate register
@app.route('/candidate_register', methods=['POST'])
def register():
    if request.method == 'POST':
        user= mongo.db.candidate

        hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'),bcrypt.gensalt())
        existing_user = user.find_one({'username':request.form.get('username')}) 
        if existing_user is None:
            user.insert_one({'name': request.form.get('name'),'username' : request.form.get('username'),'dob':request.form.get('const {propertyName} = objectToDestruct;'),'phoneno' : request.form.get('phoneno'), 'password' :hashpass})
            session['username'] = request.form['username']
        else:
            return 'username already exists'
    return redirect(url_for('candidate'))

#company register
@app.route('/company_register', methods=['POST'])
def compregister():
    if request.method == 'POST':
        user= mongo.db.company
        hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'),bcrypt.gensalt())
        existing_user = user.find_one({'username':request.form.get('username')}) 
        if existing_user is None:
            user.insert_one({'name': request.form.get('name'),'username' : request.form.get('username'),'dob':request.form.get('const {propertyName} = objectToDestruct;'),'phoneno' : request.form.get('phoneno'), 'password' :hashpass})
            session['username'] = request.form['username']
        else:
            return 'username already exists'
    return redirect(url_for('compcandidate'))


#signout
@app.route('/signout')
def signout():
    session.pop('username', None)
    return redirect(url_for('home'))

@login_required
#file uploading
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
     
    filename = secure_filename(file.filename)
    
    #to find path of a file
    path = os.path.abspath(filename)
    print("file is",path)

    #saving file in database
    if file and allowed_file(file.filename):
        print('success file')

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #usersave = User(name=rs_username, email=inputEmail, profile_pic=file.filename)
        #usersave.save()


        #to check file extension and to convert it into text
        ext = os.path.splitext(filename)[-1].lower()
        if ext == ".docx":
            txt = docx2txt.process(path)
            

            print    
        elif ext == ".pdf":
            print ( " This is pdf file")
            txt = extract_text(path)
            
          
            
        elif ext == ".html":
            txt = textract.process(path)
            print ("This is a html file")

        else:
            print("This file type is not supported")

        
            

        print(txt.replace('\n',' '))

        print()
        print("SUMMARY OF RESUME")
        names = extract_name(txt)
        print('Name of candidate: ',names)

        print()
        skill = extract_skills(txt)
        print('Skills of candidate: ', skill)

        print()
        
        PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
        phone = re.findall(PHONE_REG, txt)
        if phone:
            number = ''.join(phone[0])
        try:
            if txt.find(number) >=0 and len(number) <16:
                print("Phone no of candidate:\t",number)
        except:
            print("no number")

        EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\. \-+_]+\.[a-z]+')

        emails = re.findall(EMAIL_REG, txt)
        if emails:
            print("Email Id of candidate:\t",emails[0])

        education = extract_education(txt)
        print('Education of candidate',education)

        mongo.save_file(file.filename,file)
   
        username = session['username']
        login_user = mongo.db.candidate.find_one({'username':username})
        
        user =mongo.db.candidate
        user.update({'username' : username}, {'name':login_user['name'],'username':login_user['username'], 'dob':login_user['dob'],'phoneno':login_user['phoneno'],'password':login_user['password'],'skills':skill,'file_name':filename ,'education':education})


        #mongo.db.candidate.insert({'file_name':filename})
       # flash('File successfully uploaded ' + file.filename + ' to the database!')
     
        return render_template('/home2.html') 
    else:
       flash('Invalid Upload only txt, pdf, png, jpg, jpeg, gif,html,docx') 
    return redirect('/') 



@app.route('/test', methods=['POST','GET'])
def output():
    if request.method == 'POST':
        output = request.get_json()
        print(output) # This is the output that was stored in the JSON within the browser
       
        result = json.loads(output) #this converts the json output to a python dictionary
        print(result) # Printing the new dictionary
        print(type(result))#this shows the json converted as a python dictionary
        user =mongo.db.company
        username = session['username']
        
        canduser =mongo.db.candidate
        
        login_user = user.find_one({'username':username})
        user.update({'username' : username}, {'name':login_user['name'],'username':login_user['username'], 'dob':login_user['dob'],'phoneno':login_user['phoneno'],'password':login_user['password'],'req_skills':output},upsert=True)
        summary = canduser.find({'skills':'R'})
        print(summary)
        return jsonify('',render_template('testing.html',summary=summary))
        # for data in summary:
        # #     print(data)
        
   
 
if __name__ == '__main__':
    app.run(debug=True)