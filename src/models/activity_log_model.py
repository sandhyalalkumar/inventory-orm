from src.models import db
from src.models import ma

class ActivityLog(db.Model):
    """
    Create branch table
    """

    __tablename__ = 'activity_log'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    oldValue = db.Column(db.String(20))
    newValue = db.Column(db.String(20))
    action = db.Column(db.String(20))
    ontable = db.Column(db.String(20))

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