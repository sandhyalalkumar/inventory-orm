from src.models import db
from src.models import ma
class Variants(db.Model):
    """
    Create a product variant table
    """

    __tablename__ = 'variants'

    id = db.Column(db.String(10), primary_key=True)
    productId = db.Column(db.String(60))
    sellingPrice = db.Column(db.Float)
    costPrice = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, data):
        self.id = data.get('id')
        self.productId = data.get('productId')
        self.sellingPrice = data.get('sellingPrice')
        self.costPrice = data.get('costPrice')
        self.quantity = data.get('quantity')

    def __repr__(self):
        return 'Product Variant: {}'.format(self.id)

class VariantsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'productId', 'sellingPrice', 'costPrice', 'quantity')