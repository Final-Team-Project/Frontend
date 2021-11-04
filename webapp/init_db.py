from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()
# Declare connection
mysql_url = "mysql+pymysql://root:12345@localhost:3306/user?charset=utf8"
engine = create_engine(mysql_url,pool_recycle=500, pool_size=5, max_overflow=20, echo=False, echo_pool=True)
print('mysql_url' '==== 접속 성공')

# Declare & create Session
db_session = scoped_session( sessionmaker(autocommit=False, autoflush=False, bind=engine) )

# Create SqlAlchemy Base Instance
Base = declarative_base()
Base.query = db_session.query_property()

def init_database():
    Base.metadata.create_all(bind=engine)
