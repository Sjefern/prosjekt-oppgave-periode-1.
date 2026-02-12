from flask import Flask, render_template, request, session, redirect, url_for, flash
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/handlekurv')
def jandlekurv():
    return render_template('handlekurv.html')

@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')

@app.route('/sokedatabase')
def sokedatabase():
    return render_template('sokedatabase.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/bestillinger')
def bestillinger():
    return render_template('bestillinger.html')

if __name__ == '__main__':
    app.run(debug=True)