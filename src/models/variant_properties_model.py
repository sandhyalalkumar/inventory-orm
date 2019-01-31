from src.models import db
class VariantProperty(db.Model):
    """
    Create a variant properties table
    """

    __tablename__ = 'variants_properties'

    id = db.Column(db.String(10), primary_key=True)
    variant = db.Column(db.String(50))
    value = db.Column(db.String(20))


    def __repr__(self):
        return 'Variant Properties: {}'.format(self.variant_id)