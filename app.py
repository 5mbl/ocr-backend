from flask import Flask, render_template

from api.extractImg2Text import apiBlueprint  


app = Flask(__name__)
# api router for extracting text from images
app.register_blueprint(apiBlueprint, url_prefix='/api')

"""
@app.route('/')
def home():
    return "Home - API DIRECTORY"
"""
@app.route('/')
def home():
    return render_template('index.html')