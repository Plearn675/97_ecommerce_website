from flask import render_template, redirect, url_for, flash, request, current_app, session
from . import db, login_manager
from .models import User, Product
from .forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import stripe
import os

# This helper tells Flask-Login how to find a user by their ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@current_app.route("/")
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

@current_app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@current_app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@current_app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@current_app.route("/checkout", methods=['POST'])
@login_required
def checkout():
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    if not stripe.api_key:
        return "Stripe Secret Key not found in environment variables", 500

    total = 0
    if 'cart' in session:
        for p_id, quantity in session['cart'].items():
            product = Product.query.get(int(p_id))
            if product:
                total += (product.price * quantity)

    if total == 0:
        flash("Your cart is empty!", "warning")
        return redirect(url_for('home'))

    session_stripe = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Fruit Store Order'},
                'unit_amount': total,
            },
            'quantity': 1,
        }],
        mode='payment',
        # FIXED: Points to 'success' route instead of 'home'
        success_url=url_for('success', _external=True),
        cancel_url=url_for('view_cart', _external=True),
    )
    return redirect(session_stripe.url, code=303)

@current_app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']
    id_str = str(product_id)

    if id_str in cart:
        cart[id_str] += 1
    else:
        cart[id_str] = 1

    session['cart'] = cart
    session.modified = True
    flash("Added to cart!", "success")
    return redirect(url_for('home'))

@current_app.route("/cart")
def view_cart():
    if 'cart' not in session or not session['cart']:
        return render_template('cart.html', display_cart=[], total=0)

    display_cart = []
    total = 0
    for p_id, quantity in session['cart'].items():
        product = Product.query.get(int(p_id))
        if product:
            subtotal = product.price * quantity
            total += subtotal
            display_cart.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
    return render_template('cart.html', display_cart=display_cart, total=total)

@current_app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    if 'cart' in session:
        cart = session['cart']
        id_str = str(product_id)
        if id_str in cart:
            cart.pop(id_str)
            session.modified = True
            flash("Item removed.", "info")
    return redirect(url_for('view_cart'))

@current_app.route("/success")
def success():
    # FIXED: Clears the cart and forces session update
    session.pop('cart', None)
    session.modified = True
    return render_template('success.html')