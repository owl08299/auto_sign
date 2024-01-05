# models.py
from datetime import datetime
from final import db

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    def __repr__(self):
        return f"<Record {self.username} - {self.timestamp}>"


