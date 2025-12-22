import stripe
from flask import render_template, redirect, url_for, jsonify
from app import app

stripe.api_key = "YOUR_STRIPE_SECRET_KEY"

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        # In a real app, you'd calculate total from the DB/Cart
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'T-shirt'},
                    'unit_amount': 2000, # $20.00
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:5000/success',
            cancel_url='http://localhost:5000/cancel',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e)