from sqlalchemy import Column, Integer, Float, String, DateTime, TIMESTAMP, ForeignKey, PrimaryKeyConstraint, func, Table
from sqlalchemy.orm import relationship, backref
from webapp.init_db import Base

class User(Base):
    __tablename__ = 'jin'
    print('__tabelname__' '==== 접속성공')
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    passwd = Column(String)
    nickname = Column(String)

    def __init__(self, email=None, passwd=None, nickname='손님', makeSha=False):
        self.email = email
        if makeSha:
            self.passwd = func.sha2(passwd, 256)
        else:
            self.passwd = passwd
        self.nickname = nickname
    print('정보입력 성공')

    def __repr__(self):
        return 'User %s, %r, %r, %r' % (self.id, self.email, self.passwd, self.nickname)
