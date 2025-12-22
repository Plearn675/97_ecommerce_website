from app import create_app, db
from app.models import Product

app = create_app()
with app.app_context():
    test_item = Product(name="Cool T-Shirt", price=2500, description="The softest cotton ever.")
    db.session.add(test_item)
    db.session.commit()
    print("Product added!")
