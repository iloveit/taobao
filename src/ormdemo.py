#coding=utf-8
from sqlalchemy import *
from sqlalchemy.orm import *
from User import *

engine = create_engine('sqlite:///./sqlalchemy.db', echo=True) # 定义引擎
metadata = MetaData(engine) # 绑定元信息

#create db table
def create():
    users_table = Table('users', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('name', String(40)),
                        Column('email', String(120)))
    users_table.create()
    
    #users_table = Table('users', metadata, autoload=True)
    i = users_table.insert()
    i.execute(name='rsj217', email='rsj21@gmail.com')
    i.execute({'name': 'ghost'},{'name': 'test'})

def insert():
    users_table = Table('users', metadata, autoload=True)
    mapper(User, users_table)
    Session = sessionmaker(bind=engine)
    session = Session()
    u = User()
    u.name = 'new'
    session.add(u)
    session.flush()
    session.commit()
    
def select():
    users_table = Table('users', metadata, autoload=True)
    mapper(User, users_table)
    
    ul = User()
    session = create_session()
    query = session.query(User)
    u = query.filter_by(name='rsj217').first()
    print 'u:',u
    
def main():
    insert()

if __name__ == '__main__':
    main()