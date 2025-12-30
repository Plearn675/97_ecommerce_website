# 🍎 Fresh Fruit E-Commerce Store

A full-stack e-commerce web application built with **Flask**, **SQLAlchemy**, and **Stripe API**. This project features a functional shopping cart, user authentication, and a secure checkout flow.

## 🚀 Features
* **User Authentication**: Secure registration and login using hashed passwords (Werkzeug).
* **Product Catalog**: Dynamic display of fruits retrieved from a SQLite database.
* **Shopping Cart**: Session-based cart allowing users to add/remove items and adjust quantities (KG).
* **Stripe Integration**: Real-time checkout process using Stripe's hosted payment pages.
* **Responsive Design**: Styled with Bootstrap 5 for a clean, mobile-friendly interface.

## 🛠️ Tech Stack
* **Backend**: Python / Flask
* **Database**: SQLite / Flask-SQLAlchemy
* **Payments**: Stripe API
* **Frontend**: Jinja2 Templates / Bootstrap 5
* **Security**: Flask-Login / Dotenv (Environment Variables)

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/Plearn675/97_ecommerce_website.git](https://github.com/Plearn675/97_ecommerce_website.git)
   cd 97_ecommerce_website
   
2. **Create a virtual environment**:
   python -m venv venv
   source venv/Scripts/activate  # Windows

3. **Install dependencies**:
    pip install flask flask-sqlalchemy flask-login stripe python-dotenv werkzeug

4. **Set up environment variables: Create a .env file in the root directory**:
    SECRET_KEY=your_generated_random_string
    STRIPE_PUBLIC_KEY=pk_test_your_key_here
    STRIPE_SECRET_KEY=sk_test_your_key_here

5. **Initialize the database: Run your setup script or run this in a python shell**:
    from app import create_app, db
    app = create_app()
    with app.app_context():
        db.create_all()

6. **Run the application**:
    python run.py