from flask import Flask, render_template, request, session, redirect, url_for, flash
from db import (
    verify_user,
    get_user_by_email,
    create_user,
    init_db,
    add_cart_item,
    get_cart_items_for_user,
    remove_cart_item_for_user,
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
    product_id = request.args.get('product_id', type=int)
    
    if not product_id:
        flash('Produkt ikke funnet.', 'error')
        return redirect(url_for('tyggis'))
    
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    
    if not product:
        flash('Produkt ikke funnet.', 'error')
        return redirect(url_for('tyggis'))
    
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    user_id = session.get('user_id')
    
    if not user_id:
        flash('Du må logge inn for å legge produkter i handlekurven.', 'error')
        return redirect(url_for('kontakt'))
    
    quantity = request.form.get('quantity', 1, type=int)
    
    if quantity < 1:
        flash('Antall må være minst 1.', 'error')
        return redirect(url_for('produkt', product_id=product_id))
    
    add_cart_item(user_id, product_id, quantity)
    flash('Produkt lagt til i handlekurven!', 'success')
    return redirect(url_for('handlekurv'))

@app.route('/handlekurv')
def handlekurv():
    user_id = session.get('user_id')
    
    if not user_id:
        flash('Du må logge inn for å se handlekurven.', 'error')
        return redirect(url_for('kontakt'))
    
    # Hent handlekurv fra database
    cart_items = get_cart_items_for_user(user_id)
    
    # Bygg liste med produktinfo
    items = []
    total = 0
    
    for cart_item in cart_items:
        product = next((p for p in PRODUCTS if p['id'] == cart_item['product_id']), None)
        if product:
            item = {
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'quantity': cart_item['quantity']
            }
            items.append(item)
            total += product['price'] * cart_item['quantity']
    
    return render_template('handlekurv.html', items=items, total=total)

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    user_id = session.get('user_id')
    
    if not user_id:
        flash('Du må logge inn.', 'error')
        return redirect(url_for('kontakt'))
    
    remove_cart_item_for_user(user_id, product_id)
    flash('Produkt fjernet fra handlekurven.', 'success')
    return redirect(url_for('handlekurv'))

@app.route('/kontakt', methods=['GET', 'POST'])
def kontakt():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if verify_user(email, password):
            user = get_user_by_email(email)
            session['user_id'] = user['id']
            session['user_email'] = user['email']

            # Migrer session-cart til DB
            sess_cart = session.get('cart', {})
            for k, v in sess_cart.items():
                try:
                    pid = int(k)
                    qty = int(v.get('quantity', 0))
                except Exception:
                    continue
                if qty > 0:
                    add_cart_item(user['id'], pid, qty)

            session.pop('cart', None)
            flash('Innlogging vellykket.', 'success')
            return redirect(url_for('tyggis'))

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