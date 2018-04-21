from flask import Flask, render_template, request, Response, jsonify
import requests
import json
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, create_engine, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
import hashlib, uuid

app = Flask(__name__)

salt = os.environ['SALT']
Base=declarative_base()
postgresql_uri=os.environ['DATABASE_URL']
API_ID = os.environ['API_ID']
API_KEY = os.environ['API_KEY']
engine=create_engine(postgresql_uri)

Session = sessionmaker(bind=engine)
db = Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipes', methods = ['POST'])
def recipes():
    ingredients = request.form['ingredients']
    ingredients = ingredients.replace(' ','%20')
    res = requests.get("https://api.edamam.com/search?q="+ingredients+"&app_id="+API_ID+"&app_key="+API_KEY+"&from=0&to=3")
    # print(res.json())
    return render_template('recipes.html', res=res.json()['hits'])

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginHelper', methods = ['POST'])
def loginHelper():
    username = request.form['username']
    password = request.form['password']
    hashed_password = hashlib.sha512(item['password'].encode('utf-8') + salt.encode('utf-8')).hexdigest()
    res = db.execute("""SELECT username, password from user where username = '%s' and password = '%s';"""%(username,hashed_password))
    res= res.fetchall()
    if len(res) > 0:
        return render_template('index.html')
    return render_template('login.html',res = 'The information is incorrect, please try again')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signupHelper', methods=['GET', 'POST'])
def signupHelper():
    username = request.form['username']
    password = request.form['password']
    hashed_password = hashlib.sha512(item['password'].encode('utf-8') + salt.encode('utf-8')).hexdigest()
    res = db.execute("""SELECT id, password from %s where username = '%s';"""%(item['role'], item['username']))
    res = res.fetchall()
    if len(res) >0:
        return render_template('login.html', res = 'You have already signed up. Please login here')
    else:
        db.execute("""INSERT into users(username, password) VALUES ('%s','%s');"""%(username,hashed_password))
        db.commit()
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)
