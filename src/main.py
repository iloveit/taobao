#coding = utf-8
from taobao import *

def getData(page,pageSize):
    url = "https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8"
    url += "&q&viewFlag=A&sortType=default&searchStyle=&searchRegion=city:&searchFansNum="
    url += "&currentPage=%d&pageSize=%d" % (page,pageSize)
    
    tb = Taobao(url)
    jsonStr = tb.getData()
    mmlst = tb.parser(jsonStr)
    
    ds = DataStore()
    ds.create()

    for girl in mmlst:
        ds.insert(girl)

def showData():
    ds = DataStore()
    i = 0
    for girlInfo in ds.select():
        print i,girlInfo.realName, girlInfo.city
        i += 1

def downPhoto():
    ds = DataStore()
    i = 0
    for girlInfo in ds.select():
        urlStr = girlInfo.cardUrl
        if len(urlStr) == 0:
            continue
        filetype = urlStr.split('.')
        imgUrl = 'http:' + urlStr
        imgName = girlInfo.city + '-' + girlInfo.realName + '.' + filetype[-1]
        ds.saveImage(imgUrl, imgName)

        print i,girlInfo.realName, girlInfo.city
        i += 1
            
def main():
    downPhoto()
    


if __name__ == "__main__" :
    main()