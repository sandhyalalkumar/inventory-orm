from src.models import db
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


    def __repr__(self):
        return 'Product Variant: {}'.format(self.name)