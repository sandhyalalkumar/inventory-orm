from src.models import db
from src.models import ma
class Product(db.Model):
    """
    Create product table
    """

    __tablename__ = 'products'

    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100))
    brand = db.Column(db.String(20))
    category = db.Column(db.String(20))
    product_code = db.Column(db.String(200))

    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.brand = data.get('brand')
        self.category = data.get('category')
        self.product_code = data.get('product_code')

    def __repr__(self):
        return 'Product: {}'.format(self.id)

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'brand', 'category', 'product_code')
