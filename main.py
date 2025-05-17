from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)  # Creating session object

# TODO list
# Implement Stripe - https://docs.stripe.com/payments/checkout
# Add quantity support in the cart
# Add a product details page (/product/<id>)
# Add user authentication (login/signup)
# Store the cart in a database instead of a session
# Use Flask Blueprints to organize code better
# Add order history and an admin interface
# TODO list - Flask session oriented :
# Add a session['visits'] counter
# Store a fake user_id in session (simulate login)
# Track a session['last_page'] for back-navigation
# Store form inputs temporarily in session


# Dummy product database
PRODUCTS = [
    {'id': 1, 'name': 'T-shirt', 'price': 20.00},
    {'id': 2, 'name': 'Cap', 'price': 10.00},
    {'id': 3, 'name': 'Mug', 'price': 15.00},
]

@app.route('/')
def home():
    return render_template('home.html', products=PRODUCTS)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(product_id)
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = []
    total = 0
    if 'cart' in session:
        for product_id in session['cart']:
            # next() avoid using two loop iteration
            product = next((item for item in PRODUCTS if item['id'] == product_id), None)
            if product:
                cart_items.append(product)
                total += product['price']

    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout')
def checkout():
    # TODO: Implement Stripe Checkout integration here
    return render_template('checkout.html')


if __name__ == '__main__':
    app.run()