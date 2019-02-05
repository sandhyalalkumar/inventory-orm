from src.models import db
from src.models import ma

class Branch(db.Model):
    """
    Create branch table
    """

    __tablename__ = 'branches'

    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    district = db.Column(db.String(20))
    state = db.Column(db.String(20))
    country = db.Column(db.String(20))
    location = db.Column(db.String(100))

    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.district = data.get('district')
        self.state = data.get('state')
        self.country = data.get('country')
        self.location = data.get('location')

    def __repr__(self):
        return 'Branch: {}'.format(self.id)

class BranchSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'district', 'state', 'country', 'location')