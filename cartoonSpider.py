from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
from multiprocessing import Lock, Pool
import os
import time


def get_one_page(url):
    browser.implicitly_wait(10)
    browser.get(url)
    #print(browser.page_source)
    img_url = browser.find_element_by_xpath("//div[@id='images']/img").get_attribute('src')
    data = urllib.request.urlopen(img_url).read()
    with open(str(num)+'.jpg', 'wb')as f:
        f.write(data)  
        num += 1 

def get_url(CartoonName):
    url = "http://www.duzhez.com/search/?keywords=" + CartoonName
    datalist = []
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(url)
    data = browser.find_elements_by_xpath("//li[@class='list-comic']/p[1]/a")
    for i in data:
        info = []
        info.append(i.text)
        info.append(i.get_attribute('href'))
        datalist.append(info)
        print("编号"+str(len(datalist))+":"+info[0])
    if(len(datalist)==1):
        choice = 1
    else:
        choice = input("请输入编号:")
    CartoonUrl = datalist[int(choice)-1][1]
    browser.get(CartoonUrl)
    chapterUrl = []
    url = browser.find_elements_by_xpath('//ul[@id="chapter-list-1"]/li/a')
    for i in url:
        chapterUrl.append(i.get_attribute('href'))
    return chapterUrl


def get_one_chapter(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(3)
    listStr = browser.find_element_by_xpath("//div[@id='images']/p").text
    numlist = listStr.split('/',1)
    numlist = numlist[1].split(')')
    numMax = int(numlist[0])
    num = 1
    for i in range(num,numMax+1):
        tempurl = url +'?p='+str(i)
        browser.get(tempurl)
        imgurl = browser.find_element_by_xpath("//div[@id='images']/img").get_attribute('src')
        yield imgurl
    browser.close()
    #return nexturl

def download_img(index,imglist):
    print(index)
    print(imglist)
    while(index<=len(imglist)):
        data = urlopen(imglist[index]).read()
        with open(str(index)+'.jpg','wb')as f:
            f.write(data)
        print(index)
        index += 4


def spider(chapterNum,cartoonUrl):
    path = os.getcwd()
    while(chapterNum<len(cartoonUrl)):
        url = cartoonUrl[chapterNum]
        imglist=[]
        if os.path.isdir(str(chapterNum))==True:
            pass
        else:
            os.makedirs(str(chapterNum))
        print(chapterNum)
        temppath =path+'\\'+str(chapterNum)
        os.chdir(temppath)
        #nexturl = get_one_chapter(nexturl)
        for i in get_one_chapter(url):
            imglist.append(i)
        print("******************************************************")
        print(imglist)
        for i in range(len(imglist)):
            data = urlopen(imglist[i]).read()
            with open(str(i)+'.jpg','wb')as f:
                f.write(data)
            print(i)
        print('----------------------------------------------------------')
        chapterNum+=5
        os.chdir(path)


def days(str1,str2):
    date1=datetime.strptime(str1[0:10],"%Y-%m-%d")
    date2=datetime.strptime(str2[0:10],"%Y-%m-%d")
    num=(date1-date2).days
    return num
    
if __name__ == '__main__':
    start = time.clock()
    cartoonName = input("请输入您想爬取的漫画的名称：")
    cartoonUrl = get_url(cartoonName)
    #spiderPool = Pool(processes=5)
    #for i in range(5):
    #    spiderPool.apply_async(spider, (i,cartoonUrl))
    spiderPool = Pool(processes=2)
    spiderPool.apply_async(spider,(1,cartoonUrl))
    spiderPool.apply_async(spider,(4,cartoonUrl))
    print ("Started processes")
    spiderPool.close()
    spiderPool.join()
    print(time.clock()-start)
   # spider(cartoonUrl[0],0)
    #get_one_chapter('http://www.930mh.com/manhua/14396/531851.html')
    #spider('http://www.duzhez.com/manhua/14396/531851.html',40)

 #   data = urlopen(imgurl).read()
 #       with open(str(i)+'.jpg','wb')as f:
  #          f.write(data)