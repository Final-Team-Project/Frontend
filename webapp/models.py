from sqlalchemy import Column, Integer, Float, String, DateTime, TIMESTAMP, ForeignKey, PrimaryKeyConstraint, func, Table
from sqlalchemy.orm import relationship, backref
from webapp.init_db import Base

class User(Base):
    __tablename__ = 'JIN'
    id = Column(Integer, primary_key=True)  
    email = Column(String, unique=True)
    passwd = Column(Integer)
    nickname = Column(String)

    def __init__(self, email=None, passwd=None, nickname='손님', makeSha=False):
        self.email = email
        self.passwd = passwd
        self.nickname = nickname
        if makeSha:
            self.passwd = func.sha2(passwd, 256)
        else:
            self.passwd = passwd
        self.nickname = nickname

    def __repr__(self):
        return 'User %s, %r, %r, %r' % (id, self.email, self.passwd, self.nickname)
