from flask import Flask, render_template, request, session, redirect, url_for, flash
from db import (
    verify_user,
    get_user_by_email,
    create_user,
    init_db,
)

app = Flask(__name__)
app.secret_key = "en_lang_og_hemmelig_nøkkel_her"  # For sikre sessions

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
def handlekurv():
    return render_template('handlekurv.html')

@app.route('/kontakt', methods=['GET', 'POST'])
def kontakt():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if verify_user(email, password):
            user = get_user_by_email(email)
            session['user_id'] = user['id']
            session['user_email'] = user['email']

            flash('Innlogging vellykket.', 'success')
            return redirect(url_for('index'))

        flash('Feil epost eller passord. Prøv igjen.', 'error')

    user_id = session.get('user_id')
    user_email = session.get('user_email')
    return render_template('kontakt.html', user_id=user_id, user_email=user_email)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    flash('Du er nå logget ut.', 'success')
    return redirect(url_for('kontakt'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')

        if not username or not email or not password:
            flash('Fyll ut alle felt.', 'error')
            return render_template('register.html')

        if password != password2:
            flash('Passordene matcher ikke.', 'error')
            return render_template('register.html')

        created = create_user(username, email, password)
        if not created:
            flash('Epost er allerede registrert. Prøv å logge inn.', 'error')
            return render_template('register.html')

        flash('Registrering vellykket. Logg inn for å fortsette.', 'success')
        return redirect(url_for('kontakt'))

    return render_template('register.html')

@app.route('/sokedatabase')
def sokedatabase():
    return render_template('sokedatabase.html')

@app.route('/bestillinger')
def bestillinger():
    return render_template('bestillinger.html')

@app.route('/tyggis')
def tyggis():
    return render_template('tyggis.html', produkter=PRODUCTS)

if __name__ == '__main__':
    app.run(debug=True)