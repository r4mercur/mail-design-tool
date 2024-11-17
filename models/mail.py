import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models import db


class Mail(db.Model):
    __tablename__ = 'mails'

    id = Column(Integer, primary_key=True)
    subject = Column(String(255))
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='mails')
