from app import db
from datetime import datetime

class UserFeedBack(db.Model):
    __tablename__ = "UserResponse"
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    features = db.Column(db.String(5000))
    target = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    def __repr__(self):
        return f'<UserFeedBack {self.features:r}>'

