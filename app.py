from flask import Flask, render_template, request, session, redirect, url_for, flash
import os

app = Flask(__name__)


PRODUCTS = [
    {"id": 1, "name": "Mint Gum", "images": ["/static/img/Mintextra.png"], "price": 29, "description": "En frisk tyggegummi med sterk mintsmak."},
    {"id": 2, "name": "Strawberry Gum", "images": ["/static/img/strawberryextra.png"], "price": 29, "description": "Søt og fruktig tyggegummi med jordbærsmak."},
    {"id": 3, "name": "Blueberry Gum", "images": ["/static/img/blueberryextra.png"], "price": 29, "description": "En mild og behagelig tyggegummi med blåbærsmak."},
    {"id": 4, "name": "Watermelon Gum", "images": ["/static/img/watermelonextra.png"], "price": 29, "description": "En saftig tyggegummi med smak av vannmelon."},
    {"id": 5, "name": "Cinnamon Gum", "images": ["/static/img/cinnamonextra.png"], "price": 29, "description": "En varm og krydret tyggegummi med kanelpreg."},
    {"id": 6, "name": "Mango Gum", "images": ["/static/img/mangoextra.png"], "price": 29, "description": "Eksotisk og søt tyggegummi med fyldig mangosmak."},
    {"id": 7, "name": "Cola Gum", "images": ["/static/img/colaextra.png"], "price": 29, "description": "Klassisk tyggegummi med nostalgisk colasmak."},
    {"id": 8, "name": "Bubblegum Gum", "images": ["/static/img/bubblegumextra.png"], "price": 29, "description": "Den originale bubblegum-smaken søt, myk og ikonisk."},
    {"id": 9, "name": "Lakris Gum", "images": ["/static/img/lakrisextra.png"], "price": 29, "description": "Intens og karakteristisk tyggegummi med ekte lakrissmak."}
]

def find_product(product_id):
    return next((p for p in PRODUCTS if p['id'] == product_id), None)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/produkt')
def produkt():
    return render_template('product.html')

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

@app.route('/tyggis')
def tyggis():
    return render_template('tyggis.html', produkter=PRODUCTS)

if __name__ == '__main__':
    app.run(debug=True)