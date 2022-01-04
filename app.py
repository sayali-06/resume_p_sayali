#importing libraries
from flask import Flask, render_template, session, request, redirect, flash
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
import nltk, re


#intialize app
app= Flask(__name__, template_folder='templates')
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

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','html','docx'])

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
   
class User(db.Document):
    name = db.StringField()
    email = db.StringField()
    profile_pic = db.StringField()

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
                return render_template('upload.html')
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
    return 'sign up completed, now login'

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
    return 'success'


#signout
@app.route('/signout')
def signout():
    session.pop('username', None)
    return redirect(url_for('home'))

#file uploading
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    
    rs_username = request.form['txtusername']
    inputEmail = request.form['inputEmail']
    filename = secure_filename(file.filename)
    
    #to find path of a file
    path = os.path.abspath(filename)
    print(path)

   
   
    #saving file in database
    if file and allowed_file(file.filename):
        print('success file')

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        usersave = User(name=rs_username, email=inputEmail, profile_pic=file.filename)
        usersave.save()

        #to check file extension and to convert it into text
        ext = os.path.splitext(filename)[-1].lower()
        if ext == ".docx":
            print( "is an docx")
            txt = docx2txt.process(path)
            print(txt.replace('\n',' '))
        elif ext == ".pdf":
            print ( "is a pdf")
            txt = extract_text(path)
        else:
            txt = textract.process(path)
        
            print ("is an html")

        person_names = []
        for sent in nltk.sent_tokenize(txt):
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                    person_names.append(''.join(chunk_leave[0] for chunk_leave in chunk.leaves()))
        print(" person names in resume\n",person_names)

        PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
        phone = re.findall(PHONE_REG, txt)
        if phone:
            number = ''.join(phone[0])

        if txt.find(number) >=0 and len(number) <16:
            print("phone no:\t",number)

        EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\. \-+_]+\.[a-z]+')

        emails = re.findall(EMAIL_REG, txt)
        if emails:
            print("email of candidate:\t",emails[0])

        mongo.save_file(file.filename,file)
        mongo.db.candidate.insert({'username':rs_username,'file_name':filename})
        flash('File successfully uploaded ' + file.filename + ' to the database!')
     
        return render_template('/home2.html') 
    else:
       flash('Invalid Upload only txt, pdf, png, jpg, jpeg, gif,html,docx') 
    return redirect('/') 
 

if (__name__ == '__main__'):
    app.run(debug=True)