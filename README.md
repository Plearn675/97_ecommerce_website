# Flask eCommerce Store

A full-stack eCommerce application built with Flask, SQLAlchemy, and Stripe API.

## Features
- **User Auth**: Secure login and registration.
- **Product Catalog**: Dynamic display of items from a database.
- **Shopping Cart**: Add/remove items with session-based tracking.
- **Payments**: Secure checkout flow integrated with Stripe.

## Setup
1. Clone the repo: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Stripe keys to a `.env` file:
   - `STRIPE_PUBLIC_KEY=your_pk_test...`
   - `STRIPE_SECRET_KEY=your_sk_test...`
4. Run the app: `python run.py`