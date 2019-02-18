from PyQt5.QtCore import QThread,QThread,pyqtSignal
import Cartoon
from time import sleep
import threading
from os import chdir,makedirs,getcwd,remove
from os.path import isdir
from urllib.request import urlopen,Request
from requests.exceptions import RequestException
class homeRecommendThread(QThread):
    homeRecommend_startSignal = pyqtSignal()    # 括号里填写信号传递的参数
    homeRecommend_endSignal = pyqtSignal()
    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
        self.spider = Cartoon.CartoonSpider("update")
        self.spider.ifhomeRecommendUpdate()
        self.homeRecommend_endSignal.emit()    # 发射信号

class comicSearch(QThread):
    signal = pyqtSignal(list)    # 括号里填写信号传递的参数
    def __init__(self,name):
        super().__init__()
        self.name = name

    def __del__(self):
        self.wait()

    def run(self):
        self.spider = Cartoon.CartoonSpider("search")
        self.spider.comicSearch(self.name)
        self.signal.emit(self.spider.comicSearchList)

class comicDetail(QThread):
    signal = pyqtSignal(list,list,list,str)    # 括号里填写信号传递的参数
    def __init__(self,name,url,choice,img):
        super().__init__()
        self.img = img
        self.choice=choice
        self.url = url
        self.name = name
    def __del__(self):
        self.wait()

    def run(self):
        self.spider = Cartoon.CartoonSpider("search")
        if self.choice==1:
            req = Request(self.img,headers = self.spider.headers)
            data = urlopen(req,timeout=10).read()
            with open("./home/top/0.jpg","wb+")as f:
                f.write(data)
        self.info,self.urlList,self.titleList = self.spider.getUrlList(self.url)
        self.signal.emit(self.info,self.urlList,self.titleList,self.name)

class comicImgList(QThread):
    progress_signal = pyqtSignal(float,int)
    finish_signal = pyqtSignal(str,int,int)
    def __init__(self,urlList,index,name):
        super().__init__()
        self.urlList = urlList
        self.index = index
        self.name = name
        self.threads1 =[]
        self.threads2 = []
    def __del__(self):
        self.wait()

    def run(self):
        self.finish = 0
        num = len(self.urlList)
        download = 0
        self.spider = Cartoon.CartoonSpider("search")
        self.img = []
        for i in range(len(self.urlList)):
            #self.progress_signal.emit(progress)
            t1 = MyThread(self.spider.comicImgList,(self.urlList[i],))
            self.threads1.append(t1)
            #t2 = threading.Thread(target=self.spider.comicImgDownload,args=())
            #self.threads2.append(t2)
        path = getcwd()
        downloadPath = path +'\\Download'
        if isdir(downloadPath+'\\'+self.name)==True:
            pass
        else:
            makedirs(downloadPath+'\\'+self.name)
        downloadPath += '\\'+self.name
        for i in range(len(self.urlList)):
            if isdir(downloadPath+'\\'+str(i))==True:
                pass
            else:
                makedirs(downloadPath+'\\'+str(i))
        for i in range(len(self.threads1)):
            self.threads1[i].setDaemon(True)
            self.threads1[i].start()
        for i in range(len(self.threads1)):
            imgList = self.threads1[i].get_result()
            t2 = MyThread(self.spider.comicImgDownload,(imgList,self.name,i))
            self.threads2.append(t2)
            download+=1
            self.progress_signal.emit(float(download/num)*30,self.index)
        for t in self.threads2:
            t.setDaemon(True)
            t.start()
        for t in self.threads2:
            self.finish += t.get_result()
            self.progress_signal.emit(30+float(self.finish)/num*70,self.index)
        self.finish_signal.emit(self.name,self.index,num)

class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
 
    def run(self):
        self.result = self.func(*self.args)
 
    def get_result(self):
        threading.Thread.join(self) # 等待线程执行完毕
        try:
            return self.result
        except Exception:
            return None
            
class movie(QThread):
    signal = pyqtSignal(str)    # 括号里填写信号传递的参数
    def __init__(self,name):
        super().__init__()
        self.name = name
    def __del__(self):
        self.wait()

    def run(self):
        self.spider = Cartoon.CartoonSpider("search")
        movieList = self.spider.movieGet(self.name)
        print(movieList)
        if len(movieList)!=0:
            movie = movieList[0]
        else:
            movie = "未寻找到该资源"
        self.signal.emit(movie)