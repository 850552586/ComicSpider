import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QMessageBox,QPushButton,QGridLayout,QMainWindow,QLabel,QToolButton
from PyQt5.QtWidgets import QLineEdit,QProgressBar,QInputDialog,QDialog,QDialogButtonBox
from PyQt5.QtCore import Qt,QCoreApplication,QSize
from PyQt5.QtGui import QIcon,QIntValidator
import qtawesome
from time import sleep
import Cartoon
import EasyDownThread

class EasyDown(QMainWindow):
    def __init__(self):
        super(EasyDown, self).__init__()
        self.spider = Cartoon.CartoonSpider("spider")
        self.init()
        self.initUI()
        self.buttonConnected()
        self.setWindowTitle("EasyDown-集成下载器")

    def init(self):
        self.detailNum = 0 #初次进入下载页
        self.comicSearchNum =0
        self.comicSearch2Num = 0
        self.imgThread_busy=[0,0,0,0,0]
        self.imgList = [[],[],[],[],[]]
        self.checkRecommend = 0
        self.hotCartoonInit = 0
        #更新每日推荐
        self.spider.readhomeRecommend()
        self.homeRecommendthread = EasyDownThread.homeRecommendThread()
        self.homeRecommendthread.homeRecommend_endSignal.connect(self.homeRecommendCallBack)
        self.homeRecommendthread.start()    # 启动线程

    def initUI(self):  
        self.setWindowIcon(QIcon('./home/UI/logo.png'))             
        self.setFixedSize(1200,960)
        self.imgwidth = 150
        self.imgheight = 150
        self.isfullscreen = False
        self.main_widget = QWidget()  # 创建窗口主部件
        self.main_layout = QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
 
        self.left_widget = QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格
 
        self.home_widget = QWidget() # 创建右侧部件
        self.home_widget.setObjectName('right_widget')
        self.home_layout = QGridLayout()
        self.home_widget.setLayout(self.home_layout) # 设置右侧部件布局为网格

        self.cartoon_widget = QWidget()
        self.cartoon_widget.setObjectName('right_widget')
        self.cartoon_layout = QGridLayout()
        self.cartoon_widget.setLayout(self.cartoon_layout)

        self.cartoonSearch_widget = QWidget()
        self.cartoonSearch_widget.setObjectName('right_widget')
        self.cartoonSearch_layout = QGridLayout()
        self.cartoonSearch_widget.setLayout(self.cartoonSearch_layout)

        #漫画下载页面
        self.cartoonDownloadWidget = QWidget()
        self.cartoonDownloadWidget.setObjectName('right_widget')
        self.cartoonDownload_layout = QGridLayout()
        self.cartoonDownloadWidget.setLayout(self.cartoonDownload_layout)

        self.cartoonDetailWidget = QWidget()
        self.cartoonDetailWidget.setObjectName('right_widget')
        self.cartoonDetail_layout = QGridLayout()
        self.cartoonDetailWidget.setLayout(self.cartoonDetail_layout)
        
        self.movieDownloadwidget = QWidget()
        self.movieDownloadwidget.setObjectName('right_widget')
        self.movieDownload_layout = QGridLayout()
        self.movieDownloadwidget.setLayout(self.movieDownload_layout)

        self.downloadManageWidget = QWidget()
        self.downloadManageWidget.setObjectName('right_widget')
        self.downloadManage_layout = QGridLayout()
        self.downloadManageWidget.setLayout(self.downloadManage_layout)

        self.describtionWidget = QWidget()
        self.describtionWidget.setObjectName('right_widget')
        self.describtion_layout = QGridLayout()
        self.describtionWidget.setLayout(self.describtion_layout)
        #四个数字：左上角对应行列数/占用行数/占用列数
        self.main_layout.addWidget(self.left_widget,0,0,12,1) # 左侧部件在第0行第0列
        self.main_layout.addWidget(self.home_widget,0,2,12,7) # 右侧部件在第0行第3列
        self.main_layout.addWidget(self.cartoon_widget,0,2,12,7)
        self.main_layout.addWidget(self.cartoonSearch_widget,0,2,12,7)
        self.main_layout.addWidget(self.cartoonDownloadWidget,0,2,12,7)
        self.main_layout.addWidget(self.cartoonDetailWidget,0,2,12,7)
        self.main_layout.addWidget(self.movieDownloadwidget,0,2,12,7)
        self.main_layout.addWidget(self.downloadManageWidget,0,2,12,7)
        self.main_layout.addWidget(self.describtionWidget,0,2,12,7)

        self.setCentralWidget(self.main_widget) # 设置窗口主部件
        self.center()
        self.setWindowFlags(Qt.FramelessWindowHint)    #边框隐去
        self.UI()
        self.homeShow()
        self.show()

    def UI(self):
        self.leftUI()
        self.homeUI()
        self.hotCartoonUI(0)
        self.cartoonDownloadUI()
        self.movieDownloadUI()
        self.manageDownloadUI()
        self.describtionUI()
        self.beautyUI()

    def homeShow(self):
        self.cartoon_widget.hide()
        self.cartoonDownloadWidget.hide()
        self.cartoonSearch_widget.hide()
        self.cartoonDetailWidget.hide()
        self.home_widget.show()
        self.movieDownloadwidget.hide()
        self.downloadManageWidget.hide()
        self.describtionWidget.hide()

    def hotCartoonShow(self):
        self.home_widget.hide()   
        self.cartoonDownloadWidget.hide() 
        self.cartoonSearch_widget.hide() 
        self.cartoonDetailWidget.hide()  
        self.cartoon_widget.show()
        self.movieDownloadwidget.hide()
        self.downloadManageWidget.hide()
        self.describtionWidget.hide()

    def cartoonDownloadShow(self):
        self.cartoonDownloadWidget.show()
        self.home_widget.hide()
        self.cartoonSearch_widget.hide()
        self.cartoonDetailWidget.hide()
        self.cartoon_widget.hide()
        self.movieDownloadwidget.hide()
        self.downloadManageWidget.hide()
        self.describtionWidget.hide()
    
    def cartoonSearchShow(self):
        self.cartoonDownloadWidget.hide()
        self.home_widget.hide()
        self.cartoonSearch_widget.show()
        self.cartoonDetailWidget.hide()
        self.cartoon_widget.hide()
        self.movieDownloadwidget.hide()
        self.downloadManageWidget.hide()
        self.describtionWidget.hide()
    
    def cartoonDetailShow(self):
        self.cartoonDownloadWidget.hide()
        self.home_widget.hide()
        self.cartoonSearch_widget.hide()
        self.cartoonDetailWidget.show()
        self.cartoon_widget.hide()
        self.movieDownloadwidget.hide()
        self.downloadManageWidget.hide()
        self.describtionWidget.hide()

    def describtionShow(self):
        self.cartoonDownloadWidget.hide()   
        self.home_widget.hide()
        self.cartoonSearch_widget.hide()
        self.cartoonDetailWidget.hide()
        self.cartoon_widget.hide()
        self.downloadManageWidget.hide()
        self.movieDownloadwidget.hide()
        self.describtionWidget.show()
  

    def movieDownloadShow(self):
        self.cartoonDownloadWidget.hide()   
        self.home_widget.hide()
        self.cartoonSearch_widget.hide()
        self.cartoonDetailWidget.hide()
        self.cartoon_widget.hide()
        self.downloadManageWidget.hide()
        self.movieDownloadwidget.show()
        self.describtionWidget.hide()

    def manageDownloadShow(self):
        self.cartoonDownloadWidget.hide()   
        self.home_widget.hide()
        self.cartoonSearch_widget.hide()
        self.cartoonDetailWidget.hide()
        self.cartoon_widget.hide()
        self.movieDownloadwidget.hide()
        self.downloadManageWidget.show()
        self.describtionWidget.hide()

    def leftUI(self):
        self.left_close = QPushButton("") # 关闭按钮
        self.left_close.setObjectName('left_button')
        self.left_visit = QPushButton("") # 空白按钮
        self.left_visit.setObjectName('left_button')
        self.left_mini = QPushButton("")  # 最小化按钮
        self.left_mini.setObjectName('left_button')
        self.home = QPushButton("首页")
        self.home.setObjectName("left_button")
        self.cartoon_download = QPushButton("漫画下载")
        self.cartoon_download.setObjectName('left_button')
        self.movie_download = QPushButton("电影链接")
        self.movie_download.setObjectName('left_button')
        self.manage_download = QPushButton("下载管理")
        self.manage_download.setObjectName('left_button')
        self.hot_cartoon = QPushButton("热门漫画")
        self.hot_cartoon.setObjectName("left_button")
        self.hot_movie = QPushButton("  ")
        self.hot_movie.setObjectName("left_button")
        self.contact = QPushButton("作品说明")
        self.contact.setObjectName("left_button")
        self.donate = QPushButton("赞赏一下")
        self.donate.setObjectName("left_button")
        self.left_label_1 = QPushButton("每日推荐")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QPushButton("下载模块")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QPushButton("联系与帮助")
        self.left_label_3.setObjectName('left_label')

        self.left_layout.addWidget(self.left_mini, 0,0,1,1)
        self.left_layout.addWidget(self.left_visit, 0,1,1,1)
        self.left_layout.addWidget(self.left_close, 0,2,1,1)
        self.left_layout.addWidget(self.left_label_1,1,0,1,3)
        self.left_layout.addWidget(self.home,2,0,1,3)
        self.left_layout.addWidget(self.hot_cartoon,3,0,1,3)
        self.left_layout.addWidget(self.hot_movie,4,0,1,3)
        self.left_layout.addWidget(self.left_label_2,5,0,1,3)
        self.left_layout.addWidget(self.cartoon_download,6,0,1,3)
        self.left_layout.addWidget(self.movie_download,7,0,1,3)
        self.left_layout.addWidget(self.manage_download,8,0,1,3)
        self.left_layout.addWidget(self.left_label_3,9,0,1,3)
        self.left_layout.addWidget(self.contact,10,0,1,3)
        self.left_layout.addWidget(self.donate,11,0,1,3)
        
    def homeUI(self):
        self.recommendPage = 1
        self.recommendImg = (self.recommendPage-1)*5
        self.recommendImg1 = '.\\home\\recommend\\r'+str(self.recommendImg+0)+'.jpg'
        self.recommendImg2 = '.\\home\\recommend\\r'+str(self.recommendImg+1)+'.jpg'
        self.recommendImg3 = '.\\home\\recommend\\r'+str(self.recommendImg+2)+'.jpg'
        self.recommendImg4 = '.\\home\\recommen\\r'+str(self.recommendImg+3)+'.jpg'
        self.recommendImg5 = '.\\home\\recommend\\r'+str(self.recommendImg+4)+'.jpg'
        self.recommendTitle1 = self.spider.recommendcomic_title[(self.recommendPage-1)*5]
        self.recommendTitle2 = self.spider.recommendcomic_title[(self.recommendPage-1)*5+1]
        self.recommendTitle3 = self.spider.recommendcomic_title[(self.recommendPage-1)*5+2]
        self.recommendTitle4 = self.spider.recommendcomic_title[(self.recommendPage-1)*5+3]
        self.recommendTitle5 = self.spider.recommendcomic_title[(self.recommendPage-1)*5+4]

        #-------------今日推荐-------------------------
        self.home_recommend_label = QLabel("今日推荐")
        self.home_recommend_label.setObjectName('right_lable')     
        #切换小页面
        self.recommend_page_widget = QWidget()  # 播放控制部件
        self.recommend_layout = QGridLayout()  # 播放控制部件网格布局层
        self.recommend_page_widget.setLayout(self.recommend_layout)
        self.recommend_button_1 = QPushButton(qtawesome.icon('fa.backward', color='#141414'), "")
        self.recommend_button_1.setStyleSheet("border:none")
        self.recommend_button_2 = QPushButton(qtawesome.icon('fa.forward', color='#141414'), "")
        self.recommend_button_2.setStyleSheet("border:none;")
        self.recommend_layout.addWidget(self.recommend_button_1, 0, 0)
        self.recommend_layout.addWidget(self.recommend_button_2, 0, 2)
        self.recommend_layout.setAlignment(Qt.AlignCenter)  # 设置布局内部件居中显示
        
        
        self.home_recommend_widget = QWidget() # 推荐封面部件
        self.home_recommend_layout = QGridLayout() # 推荐封面网格布局
        self.home_recommend_widget.setLayout(self.home_recommend_layout)


        self.home_recommend_button_1 = QToolButton()
        self.home_recommend_button_1.setText(self.recommendTitle1) # 设置按钮文本
        self.home_recommend_button_1.setIcon(QIcon(self.recommendImg1)) # 设置按钮图标
        self.home_recommend_button_1.setIconSize(QSize(self.imgwidth,self.imgheight)) # 设置图标大小
        self.home_recommend_button_1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
        self.home_recommend_button_1.clicked.connect(lambda:self.cartoonDetail(self.recommendTitle1,choice=1))

        self.home_recommend_button_2 = QToolButton()
        self.home_recommend_button_2.setText(self.recommendTitle2) # 设置按钮文本
        self.home_recommend_button_2.setIcon(QIcon(self.recommendImg2)) # 设置按钮图标
        self.home_recommend_button_2.setIconSize(QSize(self.imgwidth,self.imgheight)) # 设置图标大小
        self.home_recommend_button_2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
        self.home_recommend_button_2.clicked.connect(lambda:self.cartoonDetail(self.recommendTitle2,choice=1))

        self.home_recommend_button_3 = QToolButton()
        self.home_recommend_button_3.setText(self.recommendTitle3) # 设置按钮文本
        self.home_recommend_button_3.setIcon(QIcon(self.recommendImg3)) # 设置按钮图标
        self.home_recommend_button_3.setIconSize(QSize(self.imgwidth,self.imgheight)) # 设置图标大小
        self.home_recommend_button_3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
        self.home_recommend_button_3.clicked.connect(lambda:self.cartoonDetail(self.recommendTitle3,choice=1))

        self.home_recommend_button_4 = QToolButton()
        self.home_recommend_button_4.setText(self.recommendTitle4) # 设置按钮文本
        self.home_recommend_button_4.setIcon(QIcon(self.recommendImg4)) # 设置按钮图标
        self.home_recommend_button_4.setIconSize(QSize(self.imgwidth,self.imgheight)) # 设置图标大小
        self.home_recommend_button_4.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
        self.home_recommend_button_4.clicked.connect(lambda:self.cartoonDetail(self.recommendTitle4,choice=1))

        self.home_recommend_button_5 = QToolButton()
        self.home_recommend_button_5.setText(self.recommendTitle5) # 设置按钮文本
        self.home_recommend_button_5.setIcon(QIcon(self.recommendImg5)) # 设置按钮图标
        self.home_recommend_button_5.setIconSize(QSize(self.imgwidth,self.imgheight)) # 设置图标大小
        self.home_recommend_button_5.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
        self.home_recommend_button_5.clicked.connect(lambda:self.cartoonDetail(self.recommendTitle5,choice=1))

        self.home_recommend_layout.addWidget(self.home_recommend_button_1,0,1)
        self.home_recommend_layout.addWidget(self.home_recommend_button_2,0,2)
        self.home_recommend_layout.addWidget(self.home_recommend_button_3,0,3)
        self.home_recommend_layout.addWidget(self.home_recommend_button_4,0,4)
        self.home_recommend_layout.addWidget(self.home_recommend_button_5,0,5)

        self.home_layout.addWidget(self.home_recommend_label, 2, 0, 1, 9)
        self.home_layout.addWidget(self.recommend_page_widget,2,3,1,3)
        self.home_layout.addWidget(self.home_recommend_widget, 3, 0, 1, 9) 

        self.recommend_button_1.clicked.connect(lambda:self.recommendPageChange(-1))
        self.recommend_button_2.clicked.connect(lambda:self.recommendPageChange(1))
        #-------------------------简介图片-------------------
        homeintro_lable = QLabel("简介")
        homeintro_lable.setObjectName('right_lable')
        imgintro = QToolButton(self.home_widget)
        imgintro.setIcon(QIcon('./home/UI/intro.jpg'))
        imgintro.setIconSize(QSize(400,600))
        imgintro.resize(400,600)
        imgintro.move(50,320)
        imgintro.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        imgintro.setStyleSheet(
            '''
            QToolButton{border:none;margin-left:50px}
            '''
        )
        self.home_layout.addWidget(homeintro_lable,5,0,1,5)
        #----------------------热门电影------------------------
        self.home_movie_lable = QLabel("热门电影")
        self.home_movie_lable.setObjectName('right_lable')
        
        self.home_movie_widget = QWidget() # 播放歌单部件
        self.home_movie_layout = QGridLayout() # 播放歌单网格布局
        self.home_movie_widget.setLayout(self.home_movie_layout)
        
        self.home_movie_button_1 = QToolButton()
        self.home_movie_button_1.setText("疯狂的外星人")
        self.home_movie_button_1.setIcon(QIcon('./home/UI/r1.jpg'))
        self.home_movie_button_1.setIconSize(QSize(self.imgwidth+50,self.imgheight+50))
        self.home_movie_button_1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        self.home_movie_button_2 = QToolButton()
        self.home_movie_button_2.setText("白蛇缘起")
        self.home_movie_button_2.setIcon(QIcon('./home/UI/r2.jpg'))
        self.home_movie_button_2.setIconSize(QSize(self.imgwidth+50,self.imgheight+50))
        self.home_movie_button_2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        self.home_movie_button_3 = QToolButton()
        self.home_movie_button_3.setText("流浪地球")
        self.home_movie_button_3.setIcon(QIcon('./home/UI/r3.jpg'))
        self.home_movie_button_3.setIconSize(QSize(self.imgwidth+50,self.imgheight+50))
        self.home_movie_button_3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        self.home_movie_button_4 = QToolButton()
        self.home_movie_button_4.setText("谁前爱上他的")
        self.home_movie_button_4.setIcon(QIcon('./home/UI/r4.jpg'))
        self.home_movie_button_4.setIconSize(QSize(self.imgwidth+50,self.imgheight+50))
        self.home_movie_button_4.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        self.home_movie_layout.addWidget(self.home_movie_button_1,0,0)
        self.home_movie_layout.addWidget(self.home_movie_button_2, 0, 1)
        self.home_movie_layout.addWidget(self.home_movie_button_3, 1, 0)
        self.home_movie_layout.addWidget(self.home_movie_button_4, 1, 1)
        
        self.home_layout.addWidget(self.home_movie_lable, 5,5,1,4)       
        self.home_layout.addWidget(self.home_movie_widget, 6,5,1,4)  
        
        
        #----空白填充----
        self.home_empty_widget = QWidget() 
        self.home_empty_layout = QGridLayout() 
        self.home_empty_widget.setLayout(self.home_empty_layout)
        self.home_layout.addWidget(self.home_empty_widget,9,0,1,9)

    def cartoonDownloadUI(self):
        self.search_icon =QLabel(chr(0xf002) + ' '+'搜索  ')
        self.search_icon.setFont(qtawesome.font('fa', 16))
        self.cartoon_search_input = QLineEdit()
        self.cartoon_search_input.setPlaceholderText("输入漫画的名称进行搜索")

        self.cartoon_search_button = QPushButton("搜索一下")
        self.cartoon_search_button.setObjectName("right_button")
        self.cartoon_search_button.clicked.connect(self.cartoonDownloadSearch)

        self.cartoon_empty1_widget = QWidget()
        self.cartoon_empty1_layout = QGridLayout()
        self.cartoon_empty1_widget.setLayout(self.cartoon_empty1_layout)
        self.cartoon_empty2_widget = QWidget()
        self.cartoon_empty2_layout = QGridLayout()
        self.cartoon_empty2_widget.setLayout(self.cartoon_empty2_layout)

        self.cartoonDownload_layout.addWidget(self.search_icon,4,0,1,1)
        self.cartoonDownload_layout.addWidget(self.cartoon_search_button,5,4,2,1)
        self.cartoonDownload_layout.addWidget(self.cartoon_search_input,4,1,1,8)
        self.cartoonDownload_layout.addWidget(self.cartoon_empty1_widget,1,0,3,1)
        self.cartoonDownload_layout.addWidget(self.cartoon_empty2_widget,7,0,3,1)

        self.cartoon_search_button.setStyleSheet('''
            QPushButton{
                background-color: #FFF5EE;
                color:black;
                font-size:16px;
                height:40px;
                text-align:center;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
        ''')
    
    def describtionUI(self):
        imgintro = QToolButton(self.describtionWidget)
        imgintro.setIcon(QIcon('./home/UI/describtion.jpg'))
        imgintro.setIconSize(QSize(900,600))
        imgintro.resize(900,600)
        imgintro.move(0,150)
        imgintro.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        imgintro.setStyleSheet(
            '''
            QToolButton{border:none;margin-left:50px}
            '''
        )

    def cartoonDownloadSearch(self):
        text = self.cartoon_search_input.text()
        if text !="":
            self.comicSearchthread = EasyDownThread.comicSearch(text)
            self.comicSearchthread.signal.connect(self.comicSearchCallBack)
            self.comicSearchthread.start()
            self.cartoon_search_button.setEnabled(False)
            self.cartoon_search_button.setText("提示：搜索中(´・ω・)ﾉ")
            self.cartoon_search_button.setStyleSheet('''
                QPushButton{
                    border-radius:5px;
                    color:red;
                    font-size:16px;
                    height:40px;
                    text-align:center;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                    }
            ''')
        else:
            QMessageBox.information(self, '提示信息', '请输入漫画的名称')
    
    def comicSearchUI(self):
        num = len(self.spider.comicList)
        if self.comicSearch2Num==0:
            self.resultNumLabel = QLabel("")
            self.resultNumLabel.setText("共"+str(num)+"条搜索结果,优先显示前10条")
            self.cartoonSearch_layout.addWidget(self.resultNumLabel,0,0,1,4)
            self.comicSearch2Num += 1
        else:
            self.resultNumLabel.setText("共"+str(num)+"条搜索结果,优先显示前10条")
        empty_widget = QWidget()
        empty_layout = QGridLayout()
        empty_widget.setLayout(empty_layout)
        self.cartoonSearch_layout.addWidget(empty_widget,3,0,8,1)
        self.comicSearchUIpageChange(1)

    
    def comicSearchUIpageChange(self,pageNum):
        searchPage = pageNum
        searchImg = (searchPage-1)*10
        num = len(self.spider.comicList)-(searchPage-1)*10
        self.searchTitle1 =""
        self.searchTitle2 =""
        self.searchTitle3 =""
        self.searchTitle4 =""
        self.searchTitle5 =""
        self.searchTitle6 =""
        self.searchTitle7 =""
        self.searchTitle8 =""
        self.searchTitle9 =""
        self.searchTitle10 =""
        if self.comicSearchNum == 0:
            self.search_button_1 = QToolButton()
            self.search_button_1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
            self.cartoonSearch_layout.addWidget(self.search_button_1,4,1,1,1)
            self.search_button_2 = QToolButton()
            self.search_button_2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
            self.cartoonSearch_layout.addWidget(self.search_button_2,4,2,1,1)
            self.search_button_3 = QToolButton()
            self.search_button_3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
            self.cartoonSearch_layout.addWidget(self.search_button_3,4,3,1,1)
            self.search_button_4 = QToolButton()
            self.search_button_4.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
            self.cartoonSearch_layout.addWidget(self.search_button_4,4,4,1,1)
            self.search_button_5 = QToolButton()
            self.search_button_5.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
            self.cartoonSearch_layout.addWidget(self.search_button_5,4,5,1,1)
            self.search_button_6 = QToolButton()
            self.search_button_6.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
            self.cartoonSearch_layout.addWidget(self.search_button_6,6,1,1,1)
            self.search_button_7 = QToolButton()
            self.search_button_7.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
            self.cartoonSearch_layout.addWidget(self.search_button_7,6,2,1,1)
            self.search_button_8 = QToolButton()
            self.search_button_8.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
            self.cartoonSearch_layout.addWidget(self.search_button_8,6,3,1,1)
            self.search_button_9 = QToolButton()
            self.search_button_9.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
            self.cartoonSearch_layout.addWidget(self.search_button_9,6,4,1,1)
            self.search_button_10 = QToolButton()
            self.search_button_10.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
            self.cartoonSearch_layout.addWidget(self.search_button_10,6,5,1,1)
            self.cartoonSearch_layout.addWidget(self.home_empty_widget,4,6,1,2)
            self.cartoonSearch_layout.addWidget(self.home_empty_widget,6,6,1,2)
            self.search_button_1.setIconSize(QSize(self.imgwidth,self.imgheight)) # 设置图标大小
            self.search_button_2.setIconSize(QSize(self.imgwidth,self.imgheight)) # 设置图标大小 
            self.search_button_3.setIconSize(QSize(self.imgwidth,self.imgheight)) # 设置图标大小
            self.search_button_4.setIconSize(QSize(self.imgwidth,self.imgheight)) # 设置图标大小            
            self.search_button_5.setIconSize(QSize(self.imgwidth,self.imgheight)) # 设置图标大小
            self.search_button_6.setIconSize(QSize(self.imgwidth,self.imgheight)) # 设置图标大小          
            self.search_button_7.setIconSize(QSize(self.imgwidth,self.imgheight)) # 设置图标大小    
            self.search_button_8.setIconSize(QSize(self.imgwidth,self.imgheight)) # 设置图标大小       
            self.search_button_9.setIconSize(QSize(self.imgwidth,self.imgheight)) # 设置图标大小 
            self.search_button_10.setIconSize(QSize(self.imgwidth,self.imgheight)) # 设置图标大小
            self.search_button_1.clicked.connect(lambda:self.cartoonDetail(self.searchTitle1,choice=3))
            self.search_button_2.clicked.connect(lambda:self.cartoonDetail(self.searchTitle2,choice=3))
            self.search_button_3.clicked.connect(lambda:self.cartoonDetail(self.searchTitle3,choice=3))
            self.search_button_4.clicked.connect(lambda:self.cartoonDetail(self.searchTitle4,choice=3))
            self.search_button_5.clicked.connect(lambda:self.cartoonDetail(self.searchTitle5,choice=3))
            self.search_button_6.clicked.connect(lambda:self.cartoonDetail(self.searchTitle6,choice=3))
            self.search_button_7.clicked.connect(lambda:self.cartoonDetail(self.searchTitle7,choice=3))
            self.search_button_8.clicked.connect(lambda:self.cartoonDetail(self.searchTitle8,choice=3))
            self.search_button_9.clicked.connect(lambda:self.cartoonDetail(self.searchTitle9,choice=3))
            self.search_button_10.clicked.connect(lambda:self.cartoonDetail(self.searchTitle10,choice=3))
            self.comicSearchNum += 1
    
        if num==0:
            pass
        if num>=1:
            self.search_button_1.show()
            self.searchImg1 = '.\\home\\search\\'+str(searchImg+0)+'.jpg'
            self.searchTitle1 = self.spider.comicList[(searchPage-1)*10][0]
            self.search_button_1.setText(self.searchTitle1) # 设置按钮文本
            self.search_button_1.setIcon(QIcon(self.searchImg1)) # 设置按钮图标
        else:
            self.search_button_1.hide()

        if num>=2:
            self.search_button_2.show()
            self.searchImg2 = '.\\home\\search\\'+str(searchImg+1)+'.jpg'
            self.searchTitle2 = self.spider.comicList[(searchPage-1)*10+1][0]         
            self.search_button_2.setText(self.searchTitle2) # 设置按钮文本
            self.search_button_2.setIcon(QIcon(self.searchImg2)) # 设置按钮图标
        else:
            self.search_button_2.hide()
      
        if num>=3:
            self.search_button_3.show()
            self.searchImg3 = '.\\home\\search\\'+str(searchImg+2)+'.jpg'
            self.searchTitle3 = self.spider.comicList[(searchPage-1)*10+2][0]
            self.search_button_3.setText(self.searchTitle3) # 设置按钮文本
            self.search_button_3.setIcon(QIcon(self.searchImg3)) # 设置按钮图标
        else:
            self.search_button_3.hide()
      
        if num>=4:
            self.search_button_4.show()
            self.searchImg4 = '.\\home\\search\\'+str(searchImg+3)+'.jpg'
            self.searchTitle4 = self.spider.comicList[(searchPage-1)*10+3][0]            
            self.search_button_4.setText(self.searchTitle4) # 设置按钮文本
            self.search_button_4.setIcon(QIcon(self.searchImg4)) # 设置按钮图标
        else:
            self.search_button_4.hide()
            
        if num>=5:
            self.search_button_5.show()
            self.searchImg5 = '.\\home\\search\\'+str(searchImg+4)+'.jpg'
            self.searchTitle5 = self.spider.comicList[(searchPage-1)*10+4][0] 
            self.search_button_5.setText(self.searchTitle5) # 设置按钮文本
            self.search_button_5.setIcon(QIcon(self.searchImg5)) # 设置按钮图标
        else:
            self.search_button_5.hide()
            
        if num>=6:
            self.search_button_6.show()
            self.searchImg6 = '.\\home\\search\\'+str(searchImg+5)+'.jpg'
            self.searchTitle6 = self.spider.comicList[(searchPage-1)*10+5][0]           
            self.search_button_6.setText(self.searchTitle6) # 设置按钮文本
            self.search_button_6.setIcon(QIcon(self.searchImg6)) # 设置按钮图标
        else:
            self.search_button_6.hide()
            
        if num>=7:
            self.search_button_7.show()
            self.searchImg7 = '.\\home\\search\\'+str(searchImg+6)+'.jpg'
            self.searchTitle7 = self.spider.comicList[(searchPage-1)*10+6][0]      
            self.search_button_7.setText(self.searchTitle7) # 设置按钮文本
            self.search_button_7.setIcon(QIcon(self.searchImg7)) # 设置按钮图标
        else:
            self.search_button_7.hide()
            
        if num>=8:
            self.search_button_8.show()
            self.searchImg8 = '.\\home\\search\\'+str(searchImg+7)+'.jpg'
            self.searchTitle8 = self.spider.comicList[(searchPage-1)*10+7][0]        
            self.search_button_8.setText(self.searchTitle8) # 设置按钮文本
            self.search_button_8.setIcon(QIcon(self.searchImg7)) # 设置按钮图标
        else:
            self.search_button_8.hide()
            
        if num>=9:
            self.search_button_9.show()
            self.searchImg9 = '.\\home\\search\\'+str(searchImg+8)+'.jpg'
            self.searchTitle9 = self.spider.comicList[(searchPage-1)*10+8][0]     
            self.search_button_9.setText(self.searchTitle9) # 设置按钮文本
            self.search_button_9.setIcon(QIcon(self.searchImg9)) # 设置按钮图标
        else:
            self.search_button_9.hide()
            
        if num>=10:
            self.search_button_10.show()
            self.searchImg10 = '.\\home\\search\\'+str(searchImg+9)+'.jpg'
            self.searchTitle10 = self.spider.comicList[(searchPage-1)*10+9][0]
            self.search_button_10.setText(self.searchTitle10) # 设置按钮文本
            self.search_button_10.setIcon(QIcon(self.searchImg10)) # 设置按钮图标
        else:
            self.search_button_10.hide()
    

    def cartoonDetailUI(self,img,comicName):
        self.detailpage = 0
        chapterNum = len(self.urlList)
        self.chapterNum = len(self.urlList)
        self.comicName = comicName
        if int(chapterNum/6)*6 == chapterNum:
            self.pagemax = int(chapterNum/6) - 1
        else:
            self.pagemax = int(chapterNum/6)
        if self.detailNum == 0: 
            self.detailImg = QToolButton()
            self.detailImg.setText(comicName) # 设置按钮文本
            
            empty = QLabel("  ")
            self.cartoonDetail_layout.addWidget(empty,0,0,1,7)

            self.detailImg.setIcon(QIcon(img)) # 设置按钮图标
            self.detailImg.setIconSize(QSize(self.imgwidth+50,self.imgheight+100)) # 设置图标大小
            self.detailImg.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
            self.cartoonDetail_layout.addWidget(self.detailImg,2,2,1,1)

            self.chapterNumLabel = QLabel("")
            self.chapterNumLabel.setText("【注】该漫画当前共"+str(chapterNum)+'章')
            self.cartoonDetail_layout.addWidget(self.chapterNumLabel,8,1,1,2)

            self.detailInfo1 = QLabel("")
            self.detailInfo1.setText("更新至："+self.info[0])
            self.cartoonDetail_layout.addWidget(self.detailInfo1,3,1,1,2)
            self.detailInfo2 = QLabel("")
            self.detailInfo2.setText("更新于："+self.info[1])
            self.cartoonDetail_layout.addWidget(self.detailInfo2,4,1,1,1)
            self.detailInfo3 = QLabel("")
            self.detailInfo3.setText("作者："+self.info[2])
            self.cartoonDetail_layout.addWidget(self.detailInfo3,5,1,1,1)
            self.detailInfo4 = QLabel("")
            self.detailInfo4.setText("类别："+self.info[3])
            self.cartoonDetail_layout.addWidget(self.detailInfo4,6,1,1,2)
            self.detailInfo5 = QLabel("")
            self.detailInfo5.setText("标签："+self.info[4])
            self.cartoonDetail_layout.addWidget(self.detailInfo5,7,1,1,2)
            self.cartoonDetail_layout.addWidget(self.home_empty_widget,11,0,2,1)
            
            self.nextpageButton = QPushButton(qtawesome.icon('fa.forward', color='#141414'), "")
            self.nextpageButton.setStyleSheet("border:none")
            self.prepageButton = QPushButton(qtawesome.icon('fa.backward', color='#141414'), "")
            self.prepageButton.setStyleSheet("border:none")
            self.cartoonDetail_layout.addWidget(self.nextpageButton,9,5,1,1)
            self.cartoonDetail_layout.addWidget(self.prepageButton,9,3,1,1)
            self.prepageButton.setStyleSheet('''QPushButton{width:10px}''')
            self.nextpageButton.clicked.connect(lambda:self.detailpagechange(1,self.pagemax))
            self.prepageButton.clicked.connect(lambda:self.detailpagechange(-1,self.pagemax))

            self.pageLabel = QLabel("1")
            self.cartoonDetail_layout.addWidget(self.pageLabel,9,4,1,1)

            self.chapterTitle1 = QPushButton("")
            self.chapterTitle1.setEnabled(False)
            self.cartoonDetail_layout.addWidget(self.chapterTitle1,3,3,1,3)
            self.chapterTitle2 = QPushButton("")
            self.chapterTitle2.setEnabled(False)
            self.cartoonDetail_layout.addWidget(self.chapterTitle2,4,3,1,3)
            self.chapterTitle3 = QPushButton("")
            self.chapterTitle3.setEnabled(False)
            self.cartoonDetail_layout.addWidget(self.chapterTitle3,5,3,1,3)
            self.chapterTitle4 = QPushButton("")
            self.chapterTitle4.setEnabled(False)
            self.cartoonDetail_layout.addWidget(self.chapterTitle4,6,3,1,3)
            self.chapterTitle5 = QPushButton("")
            self.chapterTitle5.setEnabled(False)
            self.cartoonDetail_layout.addWidget(self.chapterTitle5,7,3,1,3)
            self.chapterTitle6 = QPushButton("")
            self.chapterTitle6.setEnabled(False)
            self.cartoonDetail_layout.addWidget(self.chapterTitle6,8,3,1,3)

            self.cartoonDownloadButton1 = QPushButton("完本下载")
            self.cartoonDownloadButton1.clicked.connect(lambda:self.imgDownload(0,self.chapterNum,self.urlList,self.comicName))
            self.cartoonDetail_layout.addWidget(self.cartoonDownloadButton1,10,1,1,1)
            self.cartoonDownloadButton1.setStyleSheet('''
                QPushButton{
                    border : 1px solid #6699cc;
                    background-color:black;
                    color:white;
                    font-size:22px;
                    padding-left:10px;
                    text-align:center;
            }        
            ''')

            self.cartoonDownloadButton2 = QPushButton("指定章节下载（推荐）")
            self.cartoonDetail_layout.addWidget(self.cartoonDownloadButton2,11,1,1,1)
            self.cartoonDownloadButton2.setStyleSheet('''
                QPushButton{
                    border : 1px solid #6699cc;
                    background-color:black;
                    color:white;
                    font-size:22px;
                    padding-left:10px;
                    text-align:center;
            }        
            ''')
            self.cartoonDownloadButton2.clicked.connect(self.selectChapter)
            tipsButton = QPushButton("漫画内容来源于互联网抓取\nEasyDown-感谢您的使用")
            tipsButton.setStyleSheet('''
            QPushButton{
                    border : 1px solid #6699cc;
                    color:black;
                    font-size:17px;
                    font-weight:500;
                    padding-top:10px;
                    padding-bottom:10px;
                    text-align:center;
                    }
            ''')
            tipsButton.setEnabled(False)
            self.cartoonDetail_layout.addWidget(tipsButton,10,3,2,3)
            self.detailNum += 1
        else:
            if self.detailpage==0:
                self.chapterNumLabel.setText("该漫画当前共"+str(chapterNum)+'章')
                self.detailImg.setIcon(QIcon(img))
                self.detailImg.setText(comicName)
                self.detailInfo1.setText("更新至："+self.info[0])
                self.detailInfo2.setText("更新于："+self.info[1])
                self.detailInfo3.setText("作者："+self.info[2])
                self.detailInfo4.setText("类别："+self.info[3])
                self.detailInfo5.setText("标签："+self.info[4])
        self.pageLabel.setText(str(self.detailpage+1))
        currentNum = chapterNum - 6*self.detailpage
        if currentNum>0:
            self.chapterTitle1.setText(str(currentNum)+" --- "+self.titleList[currentNum-1])
        else:
            self.chapterTitle1.setText("")
        if currentNum>1:
            self.chapterTitle2.setText(str(currentNum-1)+" --- "+self.titleList[currentNum-2])
        else:
            self.chapterTitle2.setText("")
        if currentNum>2:
            self.chapterTitle3.setText(str(currentNum-2)+" --- "+self.titleList[currentNum-3])
        else:
            self.chapterTitle3.setText("")
        if currentNum>3:
            self.chapterTitle4.setText(str(currentNum-3)+" --- "+self.titleList[currentNum-4])
        else:
            self.chapterTitle4.setText("")
        if currentNum>4:
            self.chapterTitle5.setText(str(currentNum-4)+" --- "+self.titleList[currentNum-5])
        else:
            self.chapterTitle5.setText("")
        if currentNum>5:
            self.chapterTitle6.setText(str(currentNum-5)+" --- "+self.titleList[currentNum-6])
        else:
            self.chapterTitle6.setText("")

    def selectChapter(self):
        dialog = Dialog(self.chapterNum,parent=self)
        if dialog.exec_():
            info = dialog.getChapter()
            if len(info)!=0:
                start_chapter = info[0]
                end_chapter = info[1]
                if end_chapter==0:
                    QMessageBox.information(self, '提示信息', '请正确输入章节信息')
                else:
                    self.imgDownload(start_chapter-1,end_chapter,self.urlList,self.comicName)

                

    def imgDownload(self,start_chapter,end_chapter,urlList,comicName):
        urlList = urlList[start_chapter:end_chapter]
        find = 0
        for i in range(5):
            if self.checkRecommend == 0:
                QMessageBox.information(self, '提示信息', 'EasyDown正在更新信息~\n请稍等1~2分钟喔,请不要退出')
                break
            if self.imgThread_busy[i]==0:
                if i == 0:
                    self.manageButton1.show()
                    self.pbar1.show()
                    self.manageButton1.setText(comicName)
                    self.pbar1.setValue(0)
                    self.getimgListThread0 = EasyDownThread.comicImgList(urlList,i,comicName)
                    self.getimgListThread0.progress_signal.connect(self.imgProgressCallBack)
                    self.getimgListThread0.finish_signal.connect(self.comicgetImgListCallBack)
                    self.getimgListThread0.start()
                    self.imgThread_busy[i] = 1
                    find =1
                    break
                elif i == 1:
                    self.manageButton2.show()
                    self.pbar2.show()
                    self.manageButton2.setText(comicName)
                    self.pbar2.setValue(0)
                    self.getimgListThread1 = EasyDownThread.comicImgList(urlList,i,comicName)
                    self.getimgListThread1.finish_signal.connect(self.comicgetImgListCallBack)
                    self.getimgListThread1.start()
                    self.imgThread_busy[i] = 1
                    find = 1
                    break
                elif i ==2:
                    self.manageButton3.show()
                    self.pbar3.show()
                    self.manageButton3.setText(comicName)
                    self.pbar3.setValue(0)
                    self.getimgListThread2 = EasyDownThread.comicImgList(urlList,i,comicName)
                    self.getimgListThread2.finish_signal.connect(self.comicgetImgListCallBack)
                    self.getimgListThread2.start()
                    self.imgThread_busy[i] = 1
                    find = 1
                    break 
                elif i==3:
                    self.manageButton4.show()
                    self.pbar4.show()
                    self.manageButton4.setText(comicName)
                    self.pbar4.setValue(0)
                    self.getimgListThread3 = EasyDownThread.comicImgList(urlList,i,comicName)
                    self.getimgListThread3.finish_signal.connect(self.comicgetImgListCallBack)
                    self.getimgListThread3.start()
                    self.imgThread_busy[i] = 1
                    find =1
                    break
                else:
                    self.manageButton5.show()
                    self.pbar5.show()
                    self.manageButton5.setText(comicName)
                    self.pbar5.setValue(0)
                    self.getimgListThread4 = EasyDownThread.comicImgList(urlList,i,comicName)
                    self.getimgListThread4.finish_signal.connect(self.comicgetImgListCallBack)
                    self.getimgListThread4.start()
                    self.imgThread_busy[i] = 1
                    find =1
                    break
        if find == 0:
            QMessageBox.information(self, '提示信息', 'EasyDown同时只能进行5个下载任务哦')
        self.manageDownloadShow()
        
    def detailpagechange(self,num,pagemax):
        chapterNum = len(self.urlList)
        if num<0 and self.detailpage==0:
            pass    
        elif num>0 and self.detailpage==pagemax:
            pass
        else:
            self.detailpage += num
            self.pageLabel.setText(str(self.detailpage+1))
            currentNum = chapterNum - 6*self.detailpage
            if currentNum>0:
                self.chapterTitle1.setText(str(currentNum)+" --- "+self.titleList[currentNum-1])
            else:
                self.chapterTitle1.setText("")
            if currentNum>1:
                self.chapterTitle2.setText(str(currentNum-1)+" --- "+self.titleList[currentNum-2])
            else:
                self.chapterTitle2.setText("")
            if currentNum>2:
                self.chapterTitle3.setText(str(currentNum-2)+" --- "+self.titleList[currentNum-3])
            else:
                self.chapterTitle3.setText("")
            if currentNum>3:
                self.chapterTitle4.setText(str(currentNum-3)+" --- "+self.titleList[currentNum-4])
            else:
                self.chapterTitle4.setText("")
            if currentNum>4:
                self.chapterTitle5.setText(str(currentNum-4)+" --- "+self.titleList[currentNum-5])
            else:
                self.chapterTitle5.setText("")
            if currentNum>5:
                self.chapterTitle6.setText(str(currentNum-5)+" --- "+self.titleList[currentNum-6])
            else:
                self.chapterTitle6.setText("")


    def manageDownloadUI(self):
        label = QToolButton(self.downloadManageWidget)
        label.setIcon(QIcon('./home/UI/manage.jpg'))
        label.setIconSize(QSize(400,900))
        label.resize(400,900)
        label.move(250,50)
        label.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        label.setStyleSheet('''
                QToolButton{border:none;margin-left:50px}
             ''')
        self.manageButton1 = QPushButton("1",self.downloadManageWidget)
        self.pbar1 = QProgressBar(self.downloadManageWidget)  
        self.manageButton1.resize(300,50)
        self.pbar1.resize(500,20)
        self.manageButton2 = QPushButton("2",self.downloadManageWidget)
        self.pbar2 = QProgressBar(self.downloadManageWidget)  
        self.manageButton2.resize(300,50)
        self.pbar2.resize(500,20)
        self.manageButton3 = QPushButton("3",self.downloadManageWidget)
        self.pbar3 = QProgressBar(self.downloadManageWidget)  
        self.manageButton3.resize(300,50)
        self.pbar3.resize(500,20)
        self.manageButton4 = QPushButton("4",self.downloadManageWidget)
        self.pbar4 = QProgressBar(self.downloadManageWidget)  
        self.manageButton4.resize(300,50)
        self.pbar4.resize(500,20)
        self.manageButton5 = QPushButton("5",self.downloadManageWidget)
        self.pbar5 = QProgressBar(self.downloadManageWidget)  
        self.manageButton5.resize(300,50)
        self.pbar5.resize(500,20)
        self.pbar1.setValue(20)
        self.manageButton1.move(50,250)
        self.pbar1.move(400,260)
        self.manageButton2.move(50,350)
        self.pbar2.move(400,360)
        self.manageButton3.move(50,450)
        self.pbar3.move(400,460)
        self.manageButton4.move(50,550)
        self.pbar4.move(400,560)
        self.manageButton5.move(50,650)
        self.pbar5.move(400,660)
        self.manageButton1.hide()
        self.pbar1.hide()
        self.manageButton2.hide()
        self.pbar2.hide()
        self.manageButton3.hide()
        self.pbar3.hide()
        self.manageButton4.hide()
        self.pbar4.hide()
        self.manageButton5.hide()
        self.pbar5.hide()


    def home_recommend_img_Change(self):
        self.recommendImg = (self.recommendPage-1)*5
        self.recommendImg1 = '.\\home\\recommend\\r'+str(self.recommendImg+0)+'.jpg'
        self.recommendImg2 = '.\\home\\recommend\\r'+str(self.recommendImg+1)+'.jpg'
        self.recommendImg3 = '.\\home\\recommend\\r'+str(self.recommendImg+2)+'.jpg'
        self.recommendImg4 = '.\\home\\recommend\\r'+str(self.recommendImg+3)+'.jpg'
        self.recommendImg5 = '.\\home\\recommend\\r'+str(self.recommendImg+4)+'.jpg'
        self.recommendTitle1 = self.spider.recommendcomic_title[(self.recommendPage-1)*5]
        self.recommendTitle2 = self.spider.recommendcomic_title[(self.recommendPage-1)*5+1]
        self.recommendTitle3 = self.spider.recommendcomic_title[(self.recommendPage-1)*5+2]
        self.recommendTitle4 = self.spider.recommendcomic_title[(self.recommendPage-1)*5+3]
        self.recommendTitle5 = self.spider.recommendcomic_title[(self.recommendPage-1)*5+4]

        self.home_recommend_button_1.setText(self.recommendTitle1) # 设置按钮文本
        self.home_recommend_button_1.setIcon(QIcon(self.recommendImg1)) # 设置按钮图标
      
       
        self.home_recommend_button_2.setText(self.recommendTitle2) # 设置按钮文本
        self.home_recommend_button_2.setIcon(QIcon(self.recommendImg2)) # 设置按钮图标

        self.home_recommend_button_3.setText(self.recommendTitle3) # 设置按钮文本
        self.home_recommend_button_3.setIcon(QIcon(self.recommendImg3)) # 设置按钮图标


        self.home_recommend_button_4.setText(self.recommendTitle4) # 设置按钮文本
        self.home_recommend_button_4.setIcon(QIcon(self.recommendImg4)) # 设置按钮图标

        self.home_recommend_button_5.setText(self.recommendTitle5) # 设置按钮文本
        self.home_recommend_button_5.setIcon(QIcon(self.recommendImg5)) # 设置按钮图标

    def cartoonDetail(self,name,choice):
        if choice == 1:
            for i in range(25):
                if name == self.spider.recommendcomic_title[i]:
                    url = self.spider.recommendcomic_url[i]
                    if "97manhua"in url:
                        url = url.replace("www",'m')
                    self.detailImglocate = '.\\home\\recommend\\r'+str(i)+'.jpg'
                    self.comicgetDetailthread = EasyDownThread.comicDetail(name,url,0,"")
                    self.comicgetDetailthread.signal.connect(self.comicgetDetailCallBack)
                    self.comicgetDetailthread.start()
                    break
                elif i == 24:
                    QMessageBox.information(self, '提示信息', '很抱歉，未查找到该漫画的详细信息\n提示：切换一下页面可能会恢复正常喔')
        if choice == 3:
            for i in range(len(self.spider.comicList)):
                if name == self.spider.comicList[i][0]:
                    url = self.spider.comicList[i][1]
                    if "97manhua"in url:
                        url = url.replace("www",'m')
                        self.detailImglocate = '.\\home\\search\\'+str(i)+'.jpg'
                        self.comicgetDetailthread = EasyDownThread.comicDetail(name,url,0,"")
                        self.comicgetDetailthread.signal.connect(self.comicgetDetailCallBack)
                        self.comicgetDetailthread.start()
                        break
                    else:
                        QMessageBox.information(self, '提示信息', '拼命加载中....请勿切换页面~')
                        self.detailImglocate = '.\\home\\search\\'+str(i)+'.jpg'
                        self.comicgetDetailthread = EasyDownThread.comicDetail(name,url,0,"")
                        self.comicgetDetailthread.signal.connect(self.comicgetDetailCallBack)
                        self.comicgetDetailthread.start()
                        break
        if choice ==4 and self.hotclick==0:
            self.hotclick=1
            for i in range(100):
                if name == self.topcomicList[0][i]:
                    url = self.topcomicList[1][i]
                    img = self.topcomicList[2][i]
                    url = "http://comic.kukudm.com"+url
                    QMessageBox.information(self, '提示信息', '拼命加载中....请勿切换页面~')
                    self.detailImglocate = '.\\home\\top\\0.jpg'
                    self.comicgetDetailthread = EasyDownThread.comicDetail(name,url,1,img)
                    self.comicgetDetailthread.signal.connect(self.comicgetDetailCallBack)
                    self.comicgetDetailthread.start()
                    break



    def recommendPageChange(self,num):
        if self.recommendPage < 5 and num == 1:
            self.recommendPage += num
            self.home_recommend_img_Change()
        if self.recommendPage > 1 and num == -1:
            self.recommendPage += num
            self.home_recommend_img_Change()

    def hotCartoonUI(self,page):
        self.hotCartoonPage = page
        num = self.hotCartoonPage*20
        if self.hotCartoonInit == 0:
            self.hotclick = 0
            self.topcomicList = self.spider.top100()
            label = QToolButton(self.cartoon_widget)
            label.setIcon(QIcon('./home/UI/1.jpg'))
            label.setIconSize(QSize(480,170))
            label.resize(480,170)
            label.move(250,50)
            label.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            label.setStyleSheet('''
                QToolButton{border:none;margin-left:50px}
                QToolButton:hover{border-bottom:2px solid #F76677;}
             ''')
            self.pagelabel = QLabel("1",self.cartoon_widget)
            self.pagelabel.move(520,800)
            nextpageButton = QPushButton(qtawesome.icon('fa.forward', color='#141414'), "",self.cartoon_widget)
            nextpageButton.setStyleSheet("border:none")
            nextpageButton.move(580,800)
            prepageButton = QPushButton(qtawesome.icon('fa.backward', color='#141414'), "",self.cartoon_widget)
            prepageButton.setStyleSheet("border:none")
            prepageButton.move(380,800)
            nextpageButton.clicked.connect(lambda:self.hotCartoonPageChange(1))
            prepageButton.clicked.connect(lambda:self.hotCartoonPageChange(-1))
            self.hotcomicButoon1 = QPushButton(self.topcomicList[0][0],self.cartoon_widget)
            self.hotcomicButoon1.resize(400,50)
            self.hotcomicButoon1.move(50,280)
            self.hotcomicButoon2 = QPushButton(self.topcomicList[0][1],self.cartoon_widget)
            self.hotcomicButoon2.resize(400,50)
            self.hotcomicButoon2.move(50,330)
            self.hotcomicButoon3 = QPushButton(self.topcomicList[0][2],self.cartoon_widget)
            self.hotcomicButoon3.resize(400,50)
            self.hotcomicButoon3.move(50,380)
            self.hotcomicButoon4 = QPushButton(self.topcomicList[0][3],self.cartoon_widget)
            self.hotcomicButoon4.resize(400,50)
            self.hotcomicButoon4.move(50,430)
            self.hotcomicButoon5 = QPushButton(self.topcomicList[0][4],self.cartoon_widget)
            self.hotcomicButoon5.resize(400,50)
            self.hotcomicButoon5.move(50,480)
            self.hotcomicButoon6 = QPushButton(self.topcomicList[0][5],self.cartoon_widget)
            self.hotcomicButoon6.resize(400,50)
            self.hotcomicButoon6.move(50,530)
            self.hotcomicButoon7 = QPushButton(self.topcomicList[0][6],self.cartoon_widget)
            self.hotcomicButoon7.resize(400,50)
            self.hotcomicButoon7.move(50,580)
            self.hotcomicButoon8 = QPushButton(self.topcomicList[0][7],self.cartoon_widget)
            self.hotcomicButoon8.resize(400,50)
            self.hotcomicButoon8.move(50,630)
            self.hotcomicButoon9 = QPushButton(self.topcomicList[0][8],self.cartoon_widget)
            self.hotcomicButoon9.resize(400,50)
            self.hotcomicButoon9.move(50,680)
            self.hotcomicButoon10 = QPushButton(self.topcomicList[0][9],self.cartoon_widget)
            self.hotcomicButoon10.resize(400,50)
            self.hotcomicButoon10.move(50,730)
            self.hotcomicButoon11 = QPushButton(self.topcomicList[0][10],self.cartoon_widget)
            self.hotcomicButoon11.resize(400,50)
            self.hotcomicButoon11.move(580,280)
            self.hotcomicButoon12 = QPushButton(self.topcomicList[0][11],self.cartoon_widget)
            self.hotcomicButoon12.resize(400,50)
            self.hotcomicButoon12.move(580,330)
            self.hotcomicButoon13 = QPushButton(self.topcomicList[0][12],self.cartoon_widget)
            self.hotcomicButoon13.resize(400,50)
            self.hotcomicButoon13.move(580,380)
            self.hotcomicButoon14 = QPushButton(self.topcomicList[0][13],self.cartoon_widget)
            self.hotcomicButoon14.resize(400,50)
            self.hotcomicButoon14.move(580,430)
            self.hotcomicButoon15 = QPushButton(self.topcomicList[0][14],self.cartoon_widget)
            self.hotcomicButoon15.resize(400,50)
            self.hotcomicButoon15.move(580,480)
            self.hotcomicButoon16 = QPushButton(self.topcomicList[0][15],self.cartoon_widget)
            self.hotcomicButoon16.resize(400,50)
            self.hotcomicButoon16.move(580,530)
            self.hotcomicButoon17 = QPushButton(self.topcomicList[0][16],self.cartoon_widget)
            self.hotcomicButoon17.resize(400,50)
            self.hotcomicButoon17.move(580,580)
            self.hotcomicButoon18 = QPushButton(self.topcomicList[0][17],self.cartoon_widget)
            self.hotcomicButoon18.resize(400,50)
            self.hotcomicButoon18.move(580,630)
            self.hotcomicButoon19 = QPushButton(self.topcomicList[0][18],self.cartoon_widget)
            self.hotcomicButoon19.resize(400,50)
            self.hotcomicButoon19.move(580,680)
            self.hotcomicButoon20 = QPushButton(self.topcomicList[0][19],self.cartoon_widget)
            self.hotcomicButoon20.resize(400,50)
            self.hotcomicButoon20.move(580,730)

            self.hotcomicButoon1.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20],4))
            self.hotcomicButoon2.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+1],4))
            self.hotcomicButoon3.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+2],4))
            self.hotcomicButoon4.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+3],4))
            self.hotcomicButoon5.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+4],4))
            self.hotcomicButoon6.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+5],4))
            self.hotcomicButoon7.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+6],4))
            self.hotcomicButoon8.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+7],4))
            self.hotcomicButoon9.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+8],4))
            self.hotcomicButoon10.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+9],4))
            self.hotcomicButoon11.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+10],4))
            self.hotcomicButoon12.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+11],4))
            self.hotcomicButoon13.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+12],4))
            self.hotcomicButoon14.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+13],4))
            self.hotcomicButoon15.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+14],4))
            self.hotcomicButoon16.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+15],4))
            self.hotcomicButoon17.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+16],4))
            self.hotcomicButoon18.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+17],4))
            self.hotcomicButoon19.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+18],4))
            self.hotcomicButoon20.clicked.connect(lambda:self.cartoonDetail(self.topcomicList[0][self.hotCartoonPage*20+19],4))
            self.hotCartoonInit = 1
        else:
            self.pagelabel.setText(str(page+1))
            self.hotcomicButoon1.setText(self.topcomicList[0][num])
            self.hotcomicButoon2.setText(self.topcomicList[0][num+1])
            self.hotcomicButoon3.setText(self.topcomicList[0][num+2])
            self.hotcomicButoon4.setText(self.topcomicList[0][num+3])
            self.hotcomicButoon5.setText(self.topcomicList[0][num+4])
            self.hotcomicButoon6.setText(self.topcomicList[0][num+5])
            self.hotcomicButoon7.setText(self.topcomicList[0][num+6])
            self.hotcomicButoon8.setText(self.topcomicList[0][num+7])
            self.hotcomicButoon9.setText(self.topcomicList[0][num+8])
            self.hotcomicButoon10.setText(self.topcomicList[0][num+9])
            self.hotcomicButoon11.setText(self.topcomicList[0][num+10])
            self.hotcomicButoon12.setText(self.topcomicList[0][num+11])
            self.hotcomicButoon13.setText(self.topcomicList[0][num+12])
            self.hotcomicButoon14.setText(self.topcomicList[0][num+13])
            self.hotcomicButoon15.setText(self.topcomicList[0][num+14])
            self.hotcomicButoon16.setText(self.topcomicList[0][num+15])
            self.hotcomicButoon17.setText(self.topcomicList[0][num+16])
            self.hotcomicButoon18.setText(self.topcomicList[0][num+17])
            self.hotcomicButoon19.setText(self.topcomicList[0][num+18])
            self.hotcomicButoon20.setText(self.topcomicList[0][num+19])

    def movieDownloadUI(self):
        label = QToolButton(self.movieDownloadwidget)
        label.setIcon(QIcon('./home/UI/2.jpg'))
        label.setIconSize(QSize(640,220))
        label.resize(640,200)
        label.move(120,50)
        label.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        label.setStyleSheet('''
                QToolButton{border:none;margin-left:50px}
             ''')
        self.movie_search_input = QLineEdit(self.movieDownloadwidget)
        self.movie_search_input.setPlaceholderText("输入电影的名称进行搜索")
        self.movie_search_input.resize(800,40)
        self.movie_search_input.move(50,300)
        self.moviesearchButton = QPushButton("搜索",self.movieDownloadwidget)
        self.moviesearchButton.setStyleSheet('''
                QPushButton{
                    border : 1px solid #6699cc;
                    background-color:black;
                    color:white;
                    font-size:22px;
                    padding-left:10px;
                    text-align:center;
            }        
            QPushButton:hover{
                color:white;
                border:1px solid #F3F3F5;
                border-radius:10px;
            }
            ''')
        #self.moviesearchButton.clicked.connect(self.movieSearch)
        self.moviesearchButton.resize(100,40)
        self.moviesearchButton.move(860,300)
        self.movie_result = QLineEdit("功能有待开发",self.movieDownloadwidget)
        self.movie_result.resize(900,40)
        self.movie_result.move(50,400)

    def movieSearch(self):
        text = self.movie_search_input.text()
        self.moviesearchButton.setEnabled(False)
        self.moviethread = EasyDownThread.movie(text)
        self.moviethread.signal.connect(self.movieCallBack)
        self.moviethread.start()

    def hotCartoonPageChange(self,num):
        if num==1 and self.hotCartoonPage ==4:
            pass
        elif num==-1 and self.hotCartoonPage==0:
            pass
        else:
            self.hotCartoonPage+=num
            self.hotCartoonUI(self.hotCartoonPage)

    def beautyUI(self):
        self.left_close.setFixedSize(15,15) # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15) # 设置最小化按钮大小
        self.left_close.setStyleSheet('''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet('''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.left_widget.setStyleSheet('''
                QPushButton{border:none;color:white;}
                QPushButton#left_label{
                    border:none;
                    border-bottom:1px solid white;
                    font-size:22px;
                    font-weight:900;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QPushButton#left_button{font-size:18px}
                QPushButton#left_button:hover{border-left:4px solid red;font-weight:900;}
                QWidget#left_widget{
                    background:#0F0F0F;
                    border-top:1px solid white;
                    border-bottom:1px solid white;
                    border-left:1px solid white;
                    border-top-left-radius:10px;
                    border-bottom-left-radius:10px;
                }
            ''')
        self.home_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:22px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')
        self.cartoon_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton{
                border:none;
                color:gray;
                font-size:18px;
                font-weight:500;
                height:40px;
                text-align:center;
            }
            QPushButton:hover{
                color:black;
                border:1px solid #F3F3F5;
                border-radius:10px;
                background:LightGray;
            }
        '''
        )

        self.cartoonDetailWidget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel{
                border:none;
                font-size:16px;
                font-weight:500;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QToolButton{border:none;}
            QToolButton:hover{border-bottom:2px solid #F76677;}
            QPushButton{
                border:none;
                color:gray;
                font-size:16px;
                height:40px;
                text-align:left;
            }
            QPushButton:hover{
                color:black;
                border:1px solid #F3F3F5;
                border-radius:10px;
                background:LightGray;
            }
        '''
        )

        self.downloadManageWidget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton{
                border:none;
                color:black;
                font-size:22px;
                height:40px;
                text-align:center;
            }

        ''')

        self.cartoonDownloadWidget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')

        self.cartoonSearch_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QToolButton{border:none;}
            QToolButton:hover{border-bottom:2px solid #F76677;}
        ''')

        self.movieDownloadwidget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QLineEdit{
                    border:1px solid gray;
                    width:200px;
                    border-radius:10px;
                    padding:2px 4px;
                    font-size:20px;
                    height:30px;
                    }
        ''')


        self.cartoon_search_input.setStyleSheet(
            '''QLineEdit{
                    border:1px solid gray;
                    width:200px;
                    border-radius:10px;
                    padding:2px 4px;
                    font-size:20px;
                    height:30px;
            }''')
        self.describtionWidget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QToolButton{border:none;}
            QToolButton:hover{border-bottom:2px solid #F76677;}
        ''')
        self.home_recommend_widget.setStyleSheet(
            '''
                QToolButton{border:none;}
                QToolButton:hover{border-bottom:2px solid #F76677;}

            ''')
        self.home_movie_widget.setStyleSheet(
            '''
                QToolButton{border:none;padding-top:20px}
                QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')
 
        self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.main_layout.setSpacing(0)#去除缝隙 因为两个窗口中间有距离
    
    def buttonConnected(self):
        self.hot_cartoon.clicked.connect(self.hotCartoonShow)
        self.home.clicked.connect(self.homeShow)
        self.left_visit.clicked.connect(self.fullscreen)
        self.cartoon_download.clicked.connect(self.cartoonDownloadShow)
        self.movie_download.clicked.connect(self.movieDownloadShow)
        self.manage_download.clicked.connect(self.manageDownloadShow)
        self.left_mini.clicked.connect(self.mini)
        self.left_close.clicked.connect(QCoreApplication.instance().quit)
        self.contact.clicked.connect(self.describtionShow)

    def mini(self):
        self.setWindowState(Qt.WindowMinimized)

    def fullscreen(self):
        if self.isfullscreen == False:
            width = QDesktopWidget().availableGeometry().width()
            height = QDesktopWidget().availableGeometry().height()
            self.setFixedSize(width,height)
            self.isfullscreen = True
            self.center()
            self.imgwidth = 250
            self.imgheight = 250
            self.home_recommend_button_1.setIconSize(QSize(self.imgwidth,self.imgheight))
            self.home_recommend_button_2.setIconSize(QSize(self.imgwidth,self.imgheight))
            self.home_recommend_button_3.setIconSize(QSize(self.imgwidth,self.imgheight))
            self.home_recommend_button_4.setIconSize(QSize(self.imgwidth,self.imgheight))
            self.home_recommend_button_5.setIconSize(QSize(self.imgwidth,self.imgheight))


            self.beautyUI()
        else:
            self.setFixedSize(1200,960)
            self.isfullscreen = False
            self.center()
            self.imgwidth = 150
            self.imgheight = 150
            self.home_recommend_button_1.setIconSize(QSize(self.imgwidth,self.imgheight))
            self.home_recommend_button_2.setIconSize(QSize(self.imgwidth,self.imgheight))
            self.home_recommend_button_3.setIconSize(QSize(self.imgwidth,self.imgheight))
            self.home_recommend_button_4.setIconSize(QSize(self.imgwidth,self.imgheight))
            self.home_recommend_button_5.setIconSize(QSize(self.imgwidth,self.imgheight))

            self.beautyUI()

    def center(self):
        qr = self.frameGeometry() #主窗口的大小
        cp = QDesktopWidget().availableGeometry().center() #机器分辨率 得到中间点的位置
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def mousePressEvent(self, event):
        if event.button()== Qt.LeftButton:
            self.m_drag=True
            self.m_DragPosition=event.globalPos()-self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if QMouseEvent.buttons() and Qt.LeftButton:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag=False     

    def homeRecommendCallBack(self):
        self.spider.readhomeRecommend()
        self.checkRecommend = 1
        self.homeRecommendthread.quit()
    
    def comicSearchCallBack(self,List):
        self.spider.comicList =list(List)
        if len(self.spider.comicList)!=0:
            self.comicSearchUI()
            self.cartoonSearchShow()
        else:
            QMessageBox.information(self, '提示信息', '很抱歉，未查找到该漫画的信息')    
        self.comicSearchthread.quit()
        self.cartoon_search_button.setText("搜索一下")
        self.cartoon_search_button.setStyleSheet('''
                QPushButton{
                    background-color: #FFF5EE;
                    color:black;
                    font-size:16px;
                    height:40px;
                    text-align:center;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                    }
            ''')
        self.cartoon_search_button.setEnabled(True)

    def comicgetDetailCallBack(self,info,urlList,titleList,comicName):
        self.info = list(info)
        self.urlList = list(urlList)
        self.titleList = list(titleList)
        name = comicName
        self.hotclick=0
        self.comicgetDetailthread.quit()
        self.cartoonDetailUI(self.detailImglocate,name)
        self.cartoonDetailShow()
    
    def comicgetImgListCallBack(self,name,index,num):
        comicName = name
        chapterNum = num
        self.imgThread_busy[index] = 0
        if index ==0:
            self.getimgListThread0.quit()
            self.pbar1.hide()
            self.manageButton1.hide()
        elif index ==1:
            self.getimgListThread1.quit()
            self.pbar2.hide()
            self.manageButton2.hide()
        elif index ==2:
            self.getimgListThread2.quit()
            self.pbar3.hide()
            self.manageButton3.hide()
        elif index ==3:
            self.getimgListThread3.quit()
            self.pbar4.hide()
            self.manageButton4.hide()
        elif index==4:
            self.getimgListThread4.quit()
            self.pbar5.hide()
            self.manageButton5.hide()
        path ="./Download/"+comicName
        self.spider.imgChange(path,chapterNum)

    
    def imgProgressCallBack(self,progress,index):
        if index==0:
            self.pbar1.setValue(progress)

    def movieCallBack(self,movie):
        print("ok")
        self.movie_result.setText(movie)
        self.moviesearchButton.setEnabled(True)
        self.moviethread.quit()


class Dialog(QDialog):
    def __init__(self,maxNum,parent=None):
        QDialog.__init__(self,parent)
        self.resize(400, 300)
        self.maxNum =maxNum
        self.setWindowTitle("EasyDown-章节选择")
        self.label = QLabel("请输入您想下载的章节",parent=self)
        self.label.setStyleSheet('''
            QLabel{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')
        self.label.move(120,40)
        self.chapter1 = QLineEdit(parent=self)
        self.chapter1.setStyleSheet('''
             QLineEdit{
                    border:1px solid gray;
                    width:150px;
                    border-radius:10px;
                    padding:2px 4px;
                    font-size:20px;
                    height:30px;
                    }
        ''')
        self.chapter1.move(20,100)
        self.chapter2 = QLineEdit(parent=self)
        self.chapter2.setStyleSheet('''
             QLineEdit{
                    border:1px solid gray;
                    width:150px;
                    border-radius:10px;
                    padding:2px 4px;
                    font-size:20px;
                    height:30px;
                    }
        ''')
        self.chapter2.move(220,100)
        self.chapter1.setValidator(QIntValidator())
        self.chapter2.setValidator(QIntValidator())
        symbol = QLabel("___",parent=self)
        symbol.move(190,100)
        self.setWindowIcon(QIcon('./home/UI/logo.png'))  
        buttonBox = QDialogButtonBox(parent=self)
        buttonBox.setOrientation(Qt.Horizontal) # 设置为水平方向
        buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok) # 确定和取消两个按钮
        # 连接信号和槽
        buttonBox.accepted.connect(self.accept) # 确定
        buttonBox.rejected.connect(self.reject) # 取消
        buttonBox.move(110,200)
        tip = QLabel("",parent=self)
        tip.setStyleSheet('''
            QLabel{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')
        tip.setText("(提示：该漫画最大下载章节: "+str(self.maxNum)+"  )")
        tip.move(70,150)
        self.show()

    def getChapter(self):
        chapter1 = int(self.chapter1.text())
        chapter2 = int(self.chapter2.text())
        if chapter1<0 or chapter2>self.maxNum or chapter1>chapter2:
            return 0,0
        else:
            return chapter1,chapter2

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = EasyDown()
    sys.exit(app.exec_())

