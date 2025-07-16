from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Fallah bot ativo com sucesso!'
