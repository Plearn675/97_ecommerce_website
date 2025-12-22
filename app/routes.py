from flask import render_template, redirect, url_for, flash, request, current_app
from . import db
from .models import User, Product
from .forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required
import stripe
import os

@current_app.route("/")
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

@current_app.route("/checkout")
@login_required
def checkout():
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Total Order'},
                'unit_amount': 2000, # Example: $20.00
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('home', _external=True),
        cancel_url=url_for('home', _external=True),
    )
    return redirect(session.url, code=303)