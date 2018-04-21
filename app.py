from flask import Flask, render_template, request, Response, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipes', method = ['POST']):
def recipes():
    ingredients = request.form['ingredients']
    ingredients = ingredients.replace(' ','%20')
    res = requests.get("https://api.edamam.com/search?q="+ingredients+"%20breat,tomato&app_id=7f091258&app_key=c3905a1267e3c6a8fa220231cb84004e&from=0&to=1")
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)
