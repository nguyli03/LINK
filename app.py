from flask import Flask, render_template, request, Response, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipes', methods = ['POST'])
def recipes():
    ingredients = request.form['ingredients']
    print(ingredients)
    ingredients = ingredients.replace(' ','%20')
    res = requests.get("https://api.edamam.com/search?q="+ingredients+"&app_id=7f091258&app_key=c3905a1267e3c6a8fa220231cb84004e&from=0&to=3")
    print(res.json())
    return render_template('recipes.html', res=res.json()['hits'])

@app.route('/favorites', methods=['POST'])
def saveFav():
    newFav = request.values('recipeName')
    print("NEW FAVORITE:", newFav)
    return render_template('favorites.html', res=newFav)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contactUs')
def contactUs():
    return render_template('contactUs.html')

# @app.route('/save', methods=['POST'])
# def saveToDb():


if __name__=='__main__':
    app.run(debug=True)
