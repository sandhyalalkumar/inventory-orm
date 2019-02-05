from src.models import db
from src.models import ma
class Product(db.Model):
    """
    Create product table
    """

    __tablename__ = 'products'

    id = db.Column(db.String(10), primary_key=True)
    branchId = db.Column(db.String(10))
    name = db.Column(db.String(100), unique=True)
    brand = db.Column(db.String(20))
    category = db.Column(db.String(20))
    productCode = db.Column(db.String(200), unique=True)

    def __init__(self, data):
        self.id = data.get('id')
        self.branchId = data.get('branchId')
        self.name = data.get('name')
        self.brand = data.get('brand')
        self.category = data.get('category')
        self.productCode = data.get('productCode')

    def __repr__(self):
        return 'Product: {}'.format(self.id)

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'branchId', 'name', 'brand', 'category', 'productCode')
