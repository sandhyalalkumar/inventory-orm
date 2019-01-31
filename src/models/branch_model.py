from src.models import db
class Branch(db.Model):
    """
    Create branch table
    """

    __tablename__ = 'branches'

    id = db.Column(db.String(10), primary_key=True)
    branch_name = db.Column(db.String(100))

    def __repr__(self):
        return 'Branch: {}'.format(self.branch_name)