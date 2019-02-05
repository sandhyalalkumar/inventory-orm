from src.models import db
from src.models import ma

class VariantsProperty(db.Model):
    """
    Create a variant properties table
    """
    __tablename__ = 'variants_properties'

    id = db.Column(db.String(10), primary_key=True)
    variantsId = db.Column(db.String(10))
    property = db.Column(db.String(50))
    value = db.Column(db.String(20))

    def __init__(self, data):
        self.id = data.get('id')
        self.variantsId = data.get('variantsId')
        self.property = data.get('property')
        self.value = data.get('value')

    def __repr__(self):
        return 'Variants Properties: {}'.format(self.id)

class VariantsPropertySchema(ma.Schema):
    class Meta:
        fields = ('id', 'variantsId', 'property', 'value')