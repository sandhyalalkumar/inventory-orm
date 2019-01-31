from src.models import db
from src.models import ma
class ProductVariant(db.Model):
    """
    Create a product variant table
    """

    __tablename__ = 'product_varient'

    id = db.Column(db.String(10), primary_key=True)
    product_id = db.Column(db.String(60))
    selling_price = db.Column(db.Float)
    cost_price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, data):
        self.id = data.get('id')
        self.product_id = data.get('product_id')
        self.selling_price = data.get('selling_price')
        self.cost_price = data.get('cost_price')
        self.quantity = data.get('quantity')

    def __repr__(self):
        return 'Product Variant: {}'.format(self.id)

class ProductVariantSchema(ma.Schema):
    class Meta:
        fields = ('id', 'product_id', 'selling_price', 'cost_price', 'quantity')