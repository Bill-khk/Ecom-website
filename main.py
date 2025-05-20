import os, stripe

from flask import Flask, render_template, redirect, url_for, session, request

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


@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    session['cart'].remove(product_id)
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


from wtforms import IntegerField, SelectField, SubmitField, StringField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
import datetime, stripe

year = int(datetime.datetime.now().strftime("%Y"))
years = [year + i for i in range(0, 5)]
year_choices = [(str(y), str(y)) for y in years]


class CheckoutForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    number = IntegerField('Card number', validators=[DataRequired()])
    exp_month = SelectField('exp_month',
                            choices=[(1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'),
                                     (8, '08'), (9, '09'), (10, '10'), (11, '11'), (12, '12')],
                            validators=[DataRequired()])
    exp_year = SelectField('exp_year', choices=[year_choices[0], year_choices[1], year_choices[2], year_choices[3],
                                                year_choices[4]], validators=[DataRequired()])
    cvc = IntegerField('cvc', validators=[Length(min=3, max=3)])
    submit = SubmitField('Pay')


@app.route('/checkout/<price>', methods=['GET', 'POST'])
def checkout(price):
    STRIPE_KEY = os.environ.get('STRIPE_KEY')
    stripe.api_key = STRIPE_KEY
    form = CheckoutForm()
    if request.method == 'POST':
        print(
            f'{int(price[0:price.find('.')])}$ - {request.form['name']} - {request.form['number']}, {request.form['exp_month']}/{request.form['exp_year']}, {request.form['cvc']}')
        CONNECTED_ACCOUNT_ID = os.environ.get('ACC_ID')
        payment_intent = stripe.PaymentIntent.create(
            amount=int(float(price) * 100),  # amount in cents
            currency="usd",
            payment_method="pm_card_visa",
            stripe_account=f'{CONNECTED_ACCOUNT_ID}',
        )

        # payment_method = stripe.PaymentMethod.create(
        #     type="card",
        #     card={
        #         "exp_month": int(request.form['exp_month']),
        #         "exp_year": int(request.form['exp_year']),
        #         "number": str(request.form['number']),
        #         "cvc": str(request.form['cvc']),
        #     },
        # )
    else:
        # Test values
        form.name.data = 'John Doe'
        form.number.data = '4242424242424242'
        form.exp_month.data = '12'
        form.exp_year.data = '2025'
        form.cvc.data = '123'

    # TODO: Implement Stripe Checkout integration here
    return render_template('checkout.html', form=form, price=price)


@app.route('/create-checkout-session/<price>', methods=['POST'])
def create_checkout_session(price):
    STRIPE_KEY = os.environ.get('STRIPE_KEY')
    stripe.api_key = STRIPE_KEY
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Total price',
                },
                'unit_amount': int(float(price) * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('success', _external=True),
        cancel_url=url_for('cancel', _external=True),
    )

    return redirect(session.url, code=303)


if __name__ == '__main__':
    app.run()
