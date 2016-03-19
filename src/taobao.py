#coding = utf-8
import requests
import json
from sqlalchemy import *
from sqlalchemy.orm import *

class MMInfo(object):
    def __init__(self):
        self.userId = ''
        self.realName = ''
        self.city = ''
        self.cardUrl = ''
        self.avatarUrl = ''
        
    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.realName, self.city)
    
class Taobao(object):
    def __init__(self, url):
        self.url = url
        
    def getData(self):
        response = requests.get(self.url)
        return response.content.decode('GBK')
    
    def parser(self, jsonStr):
        jsdata = json.loads(jsonStr)
        return jsdata['data']['searchDOList']
    
class DataStore(object):
    def __init__(self):
        self.engine = create_engine('sqlite:///./sqlalchemy.db', echo=False)
        self.metadata = MetaData(self.engine)
        
    def create(self):
        try:
            info_table = Table('mminfo', self.metadata, autoload=True)
        
        except:
            info_table = Table('mminfo', self.metadata,
                                Column('userId', String(40), primary_key=True),
                                Column('realName', String(40)),
                                Column('city', String(20)),
                                Column('cardUrl', String(256)),
                                Column('avatarUrl', String(256)))
            print("create db table:mminfo")
            info_table.create()
    
    def insert(self, girl):
        info_table = Table('mminfo', self.metadata, autoload=True)
        clear_mappers()
        mapper(MMInfo, info_table)

        girlInfo = MMInfo()
        girlInfo.userId = str(girl['userId'])
        girlInfo.realName = girl['realName']
        girlInfo.city = girl['city']
        girlInfo.cardUrl = girl['cardUrl']
        girlInfo.avatarUrl = girl['avatarUrl']
        
        Session = sessionmaker(bind = self.engine)
        session = Session()
        try:
            session.add(girlInfo)
            session.flush()
            session.commit()
        except:
            print(girlInfo)
            session.rollback()
        finally:
            session.close()
        
        
    def select(self):
        info_table = Table('mminfo', self.metadata, autoload=True)
        clear_mappers()
        mapper(MMInfo, info_table)
        session = create_session()
        query = session.query(MMInfo)
        
        return query.all()
    
    def saveImage(self, imgUrl,imgName = "default.jpg"):
        response = requests.get(imgUrl, stream=True)
        image = response.content
        DstDir="/Users/qzdx/picture/"
        print("save:"+DstDir+imgName+"\n")
        try:
            with open(DstDir+imgName ,"wb") as jpg:
                jpg.write(image)
                return
        except IOError:
            print("IO Error\n")
            return
        finally:
            jpg.close()
