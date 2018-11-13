# -*- coding: utf-8 -*-
"""
Created on Mon May 15 13:10:15 2017
@author: Celfras--Levi
"""
from PyQt5.QtWidgets import QWidget,QApplication,QVBoxLayout,QMainWindow,QGridLayout,QGroupBox,QPushButton,QCheckBox,QLabel,QAction,QFileDialog,QLineEdit,QTextEdit,QDialog,QGraphicsView,QGraphicsScene,QHBoxLayout
from PyQt5.QtGui import QIcon,QPalette,QFont,QTextCursor,QImage,QPixmap
from PyQt5.QtCore import Qt,QObject,pyqtSignal,QRect
import codecs,sys,os
import linecache2 as linecache

from sys import path
path.append(".")
from makespeccode import Maketestdataspec

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

class EmittingStream(QObject):
    textWritten = pyqtSignal(str)
    def flush(self):
        pass
    def write(self,text):
        try:                                                  
            self.textWritten.emit(str(text))
        except:
            pass

class Figure_Canvs(FigureCanvas):
    def __init__(self,parent=None):
        fig=Figure(figsize=(15, 15), dpi=90)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(111)

    def Figure_data(self,sampleplotdata):
        if len(sampleplotdata)!=0:
            long=len(sampleplotdata[0])
            makelocator=int((sampleplotdata[0][int(long/2)]+200)/50)
            for i in sampleplotdata:
                plotdata=[int(j) for j in i]
                self.axes.plot(range(long), plotdata, 'b-')

        else:
            makelocator=1         
        xmajorLocator = MultipleLocator(makelocator+4)
        xmajorFormatter = FormatStrFormatter('%1d')
        xminorLocator = MultipleLocator(makelocator)

        ymajorLocator = MultipleLocator(makelocator+4)
        ymajorFormatter = FormatStrFormatter('%1d')
        yminorLocator = MultipleLocator(makelocator)

        self.axes.xaxis.set_major_locator(xmajorLocator)
        self.axes.xaxis.set_major_formatter(xmajorFormatter)
        self.axes.xaxis.set_minor_locator(xminorLocator)

        self.axes.yaxis.set_major_locator(ymajorLocator)
        self.axes.yaxis.set_major_formatter(ymajorFormatter)
        self.axes.yaxis.set_minor_locator(yminorLocator)

        self.axes.xaxis.grid(True, which='major')
        self.axes.yaxis.grid(True, which='minor')


class Example(QMainWindow,QAction,QFileDialog,QObject):

    def __init__(self):
        super(Example,self).__init__()
        self.initUI()

    def __del__(self):
        sys.__stdout__  = sys.stdout      # 初始化标准输出
        sys.__stderr__  = sys.stderr      # 初始化标准输出
        
    def initUI(self):
        self.savedStdout = sys.stdout
        self.savedStderr = sys.stderr
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)  # 重新定义系统标准输出
        sys.stderr = EmittingStream(textWritten=self.normalOutputWritten)  # 重新定义系统标准错误
      
        self.haveinformation=0                                             # 判断有没有TOOL文件导入的值， 初始化为0
        self.getspec=0                                                     # 判断有没有spec值生成， 初始化为0
        self.getdatapicture=0                                              # 判断有没有数据分布图生成， 初始化为0
        self.setWindowTitle("MfsFactory Tool Ini Maker")
        self.setWindowIcon(QIcon("C:/Users/Celfras--Levi/Desktop/celfras.ico")) 
        self.addMenu01 = self.menuBar().addMenu("&Log")
        self.addMenu02 = self.menuBar().addMenu("&Tool")
        self.logaction = QAction(QIcon("C:/Users/Administrator/Desktop/ico1-1.ico"),"&导入Log文件夹",self)
        self.logaction.setStatusTip("导入测试后log文件夹目录")
        self.toolaction = QAction(QIcon("C:/Users/Administrator/Desktop/ico2-1.ico"),"&导入Tool.ini文件",self)
        self.toolaction.setStatusTip("可不导入")
        self.logaction.triggered.connect(self.Dialog)
        self.toolaction.triggered.connect(self.Information)
        self.addMenu01.addAction(self.logaction)
        self.addMenu02.addAction(self.toolaction)

        mainLayout = QVBoxLayout()
        vboxLayout = QVBoxLayout()    
        Layout = QGridLayout()   
        
        pe=QPalette()
        pe.setColor(QPalette.WindowText,Qt.red)
        
        ModelNameLabel = QLabel("MODEL NAME")
        ModelNameLabel.setAlignment(Qt.AlignCenter)
        self.ModelNameLineEdit = QLineEdit()
     
        ICNameLabel = QLabel("CHIP_ID")
        ICNameLabel.setAlignment(Qt.AlignCenter)
        self.ICNameLineEdit = QLineEdit()
 
        FactoryLabel = QLabel("FACTORY NAME ")
        FactoryLabel.setAlignment(Qt.AlignCenter)
        self.FactoryLineEdit = QLineEdit()    
       
        RowNumberLabel = QLabel("SCREEN_ROWCHNUM")
        RowNumberLabel.setAlignment(Qt.AlignCenter)
        self.RowumberLineEdit = QLineEdit()
        
        ColNumberLabel = QLabel("SCREEN_COLCHNUM")
        ColNumberLabel.setAlignment(Qt.AlignCenter)
        self.ColNumberLineEdit = QLineEdit()
        
        KeyRowNumberLabel = QLabel("KEY_RX")
        KeyRowNumberLabel.setAlignment(Qt.AlignCenter)
        self.KeyRowNumberLineEdit = QLineEdit()

        KeyColNumberLabel = QLabel("KEY_TX")
        KeyColNumberLabel.setAlignment(Qt.AlignCenter)
        self.KeyColNumberLineEdit = QLineEdit()

        KeyNumNumberLabel = QLabel("KEY_NUM")
        KeyNumNumberLabel.setAlignment(Qt.AlignCenter)
        self.KeyNumNumberLineEdit = QLineEdit()        
                
        FW_BootLineLabel = QLabel("BOOT_VERISON")
        FW_BootLineLabel.setAlignment(Qt.AlignCenter)
        self.FW_BootLineEdit = QLineEdit()
           
        FW_CoreLineLabel = QLabel("CORE_VERISON")
        FW_CoreLineLabel.setAlignment(Qt.AlignCenter)
        self.FW_CoreLineEdit = QLineEdit()
          
        FW_CustomLineLabel = QLabel("CUSTOM_VERISON")
        FW_CustomLineLabel.setAlignment(Qt.AlignCenter)
        self.FW_CustomLineEdit = QLineEdit()  
        
        FW_ParamLineLabel = QLabel("PARAMETER_VERISON")
        FW_ParamLineLabel.setAlignment(Qt.AlignCenter)
        self.FW_ParamLineEdit = QLineEdit()
               
        Layout.addWidget(ModelNameLabel,2,0)
        Layout.addWidget(self.ModelNameLineEdit,2,1,1,2)
         
        Layout.addWidget(ICNameLabel,3,0)
        Layout.addWidget(self.ICNameLineEdit,3,1,1,2)
        
        Layout.addWidget(FactoryLabel,4,0)
        Layout.addWidget(self.FactoryLineEdit,4,1,1,2)
        
        Layout.addWidget(RowNumberLabel,5,0)
        Layout.addWidget(self.RowumberLineEdit,5,1,1,2)
        
        Layout.addWidget(ColNumberLabel,6,0)
        Layout.addWidget(self.ColNumberLineEdit,6,1,1,2)
        
        Layout.addWidget(KeyRowNumberLabel,7,0)
        Layout.addWidget(self.KeyRowNumberLineEdit,7,1,1,2)            

        Layout.addWidget(KeyColNumberLabel,2,6)
        Layout.addWidget(self.KeyColNumberLineEdit,2,7,1,2)
        
        Layout.addWidget(KeyNumNumberLabel,3,6)
        Layout.addWidget(self.KeyNumNumberLineEdit,3,7,1,2)
        
        Layout.addWidget(FW_BootLineLabel,4,6)
        Layout.addWidget(self.FW_BootLineEdit,4,7,1,2)
        
        Layout.addWidget(FW_CoreLineLabel,5,6)
        Layout.addWidget(self.FW_CoreLineEdit,5,7,1,2)
        
        Layout.addWidget(FW_CustomLineLabel,6,6)
        Layout.addWidget(self.FW_CustomLineEdit,6,7,1,2)
        
        Layout.addWidget(FW_ParamLineLabel,7,6)
        Layout.addWidget(self.FW_ParamLineEdit,7,7,1,2)
        
        pe=QPalette()
        pe.setColor(QPalette.Text,Qt.red)

        Layout2 = QGridLayout()
        self.AutoDownloadcheck = QCheckBox("Auto Download FW    ")
        self.AutoDownloadcheck.setFont(QFont("Roman times",8,QFont.Bold)) 
        self.AutoDownloadcheck.setChecked(True)

        self.Cmdeltatestcheck = QCheckBox("Cm Delta Test")
        self.Cmdeltatestcheck.setFont(QFont("Roman times",8,QFont.Bold)) 
        self.Cmdeltatestcheck.setChecked(True)       
        
        self.Selfcptestcheck = QCheckBox("Self CP Test")
        self.Selfcptestcheck.setFont(QFont("Roman times",8,QFont.Bold)) 
        self.Selfcptestcheck.setChecked(True)
        
        self.Selfshortcheck = QCheckBox("Self Short Test")
        self.Selfshortcheck.setFont(QFont("Roman times",8,QFont.Bold)) 
        self.Selfshortcheck.setChecked(True)
        
        self.Selfjittercheck = QCheckBox("Self Jitter Test")
        self.Selfjittercheck.setFont(QFont("Roman times",8,QFont.Bold)) 
        self.Selfjittercheck.setChecked(False)
        
        self.Vdifftestcheck=QCheckBox("V Diff Test")
        self.Vdifftestcheck.setFont(QFont("Roman times",8,QFont.Bold)) 
        self.Vdifftestcheck.setChecked(False)
        
        self.Hdifftestcheck=QCheckBox("H Diff Test")
        self.Hdifftestcheck.setFont(QFont("Roman times",8,QFont.Bold)) 
        self.Hdifftestcheck.setChecked(False)

        self.Jittertestcheck=QCheckBox("Jitter Test")
        self.Jittertestcheck.setFont(QFont("Roman times",8,QFont.Bold))
        self.Jittertestcheck.setChecked(False)
       
        button = QPushButton('Make')
        button.clicked.connect(self.writename)
        button.resize(button.sizeHint())
            
        Layout2.addWidget(self.AutoDownloadcheck,1,0,1,1)               
        Layout2.addWidget(self.Cmdeltatestcheck,1,3,1,1)
        Layout2.addWidget(self.Selfcptestcheck,1,4,1,1,)
        Layout2.addWidget(self.Selfshortcheck,1,5,1,1)
        Layout2.addWidget(self.Selfjittercheck,3,0,1,1)               
        Layout2.addWidget(self.Vdifftestcheck,3,3,1,1)
        Layout2.addWidget(self.Hdifftestcheck,3,4,1,1,)
        Layout2.addWidget(self.Jittertestcheck,3,5,1,1)        
              
        Layout3 = QGridLayout()
        AveragespecLine = QLabel("VA均值采集spec:")
        AveragespecLine.setFont(QFont("Roman times",8,QFont.Bold)) 
        AveragespecLine.setAlignment(Qt.AlignCenter)
        self.AveragespecLineEdit = QLineEdit('0.25')
        self.AveragespecLineEdit .setFont(QFont("Roman times",8,QFont.Bold)) 
        self.AveragespecLineEdit.setPalette(pe)
        KeyaveragespecLine = QLabel("KEY均值采集spec:")
        KeyaveragespecLine.setFont(QFont("Roman times",8,QFont.Bold)) 
        KeyaveragespecLine.setAlignment(Qt.AlignCenter)
        self.KeyaveragespecLineEdit=QLineEdit('0.25')
        self.KeyaveragespecLineEdit.setFont(QFont("Roman times",8,QFont.Bold)) 
        self.KeyaveragespecLineEdit.setPalette(pe)
        OutputmaxspecLine = QLabel("输出MAX值spec:")
        OutputmaxspecLine.setFont(QFont("Roman times",8,QFont.Bold)) 
        OutputmaxspecLine.setAlignment(Qt.AlignCenter)
        self.OutputmaxspecLineEdit=QLineEdit('0.25')
        self.OutputmaxspecLineEdit.setFont(QFont("Roman times",8,QFont.Bold)) 
        self.OutputmaxspecLineEdit.setPalette(pe)
        OutputminspecLine = QLabel("输出MIN值spec:")
        OutputminspecLine.setFont(QFont("Roman times",8,QFont.Bold)) 
        OutputminspecLine.setAlignment(Qt.AlignCenter)
        self.OutputminspecLineEdit=QLineEdit('0.25')
        self.OutputminspecLineEdit.setFont(QFont("Roman times",8,QFont.Bold)) 
        self.OutputminspecLineEdit.setPalette(pe)
        
        Layout3.addWidget(AveragespecLine,1,0)
        Layout3.addWidget(self.AveragespecLineEdit,1,1,1,2)
        Layout3.addWidget(KeyaveragespecLine,1,6)
        Layout3.addWidget(self.KeyaveragespecLineEdit,1,7,1,2)
        Layout3.addWidget(OutputmaxspecLine,2,0)
        Layout3.addWidget(self.OutputmaxspecLineEdit,2,1,1,2)
        Layout3.addWidget(OutputminspecLine,2,6)
        Layout3.addWidget(self.OutputminspecLineEdit,2,7,1,2)
        
        self.TxtWidget=QTextEdit()
        
        Layout4 = QHBoxLayout()
        Layout4.addWidget(QLabel(''),8)
        Layout4.addWidget(QLabel(''),8)
        Layout4.addWidget(QLabel(''),8)
        Layout4.addWidget(QLabel(''),8)
        Layout4.addWidget(button,8)

        Layout5 = QGridLayout()
        Layout5.setContentsMargins(0,0,0,0)
        self.graph_widget=QWidget()
        self.Datagrid_Widget=QGraphicsView(self.graph_widget)
        Layout5.addWidget(self.Datagrid_Widget,0,0)
        self.graph_widget.setLayout(Layout5)

        self.graph_1=Figure_Canvs()
        self.graph_1.Figure_data([])
        self.graphicsscene=QGraphicsScene()
        self.graphicsscene.addWidget(self.graph_1)
        self.Datagrid_Widget.setScene(self.graphicsscene)
        self.Datagrid_Widget.show()
               
        Layout6=QHBoxLayout()
        Layout6.addWidget(self.TxtWidget,8)
        Layout6.addWidget(self.graph_widget,8)
        
        TestitemWidget = QGroupBox('Test Item')
        TestitemWidget.setLayout(Layout2)
        
        SpecWidget = QGroupBox('Spec Item')
        SpecWidget.setLayout(Layout3)

        LayoutWidget = QGroupBox('Sample Information')
        LayoutWidget.setLayout(Layout)

        TxtandgraphWidget=QGroupBox('')
        TxtandgraphWidget.setLayout(Layout6)
        
        ButtonWidget=QGroupBox('')
        ButtonWidget.setLayout(Layout4)
              
        mainLayout.addLayout(vboxLayout)

        mainLayout.addWidget(SpecWidget)
        mainLayout.addWidget(TestitemWidget)
        mainLayout.addWidget(LayoutWidget)
        
        mainLayout.addWidget(TxtandgraphWidget)
        mainLayout.addWidget(ButtonWidget)
  
        MainLayoutWidget = QWidget()
        MainLayoutWidget.setBackgroundRole(QPalette.Light)

        MainLayoutWidget.setLayout(mainLayout)    
        self.setCentralWidget(MainLayoutWidget)

        self.filedir=os.path.split(os.path.abspath(sys.argv[0]))[0]
        if os.path.isdir(self.filedir+'\\Templet\\')==False:
            os.makedirs(self.filedir+'\\Templet\\')
        if os.path.isdir(self.filedir+'\\Transitdata\\')==False:
            os.makedirs(self.filedir+'\\Transitdata\\')
        if os.path.isdir(self.filedir+'\\Makefile\\')==False:
            os.makedirs(self.filedir+'\\Makefile\\')
        
    def Dialog(self):         # 处理log文件夹 
        
        directory = QFileDialog.getExistingDirectory(self,"打开log文件夹","C:\\")
        averagefile=(self.filedir+'\\Transitdata\\maxandmindata.txt')
        alldataoutputfile=(self.filedir+'\\Transitdata\\')
        
        if os.path.isdir(directory):
            self.getspec=1
            logdirectory = directory
            '''print(logdirectory)'''  
            vatargetpercent=float(self.AveragespecLineEdit.text())
            keytargetpercent=float(self.KeyaveragespecLineEdit.text())
            outputmaxsetspec=float(self.OutputmaxspecLineEdit.text())
            outputminsetspec=float(self.OutputminspecLineEdit.text())
            sampleplotdata=Maketestdataspec(logdirectory+'/',vatargetpercent,keytargetpercent,averagefile,alldataoutputfile,outputmaxsetspec,outputminsetspec)        #Maketestdataspec(inputfiledirectory,vatargetpercent,keytargetpercent,outputaveragefile,outputmaxsetspec,outputminsetspec)
            self.getdatapicture=1
            self.graph_1=Figure_Canvs()
            self.graph_1.Figure_data(sampleplotdata)
            self.graphicsscene=QGraphicsScene()
            self.graphicsscene.addWidget(self.graph_1)
            self.Datagrid_Widget.setScene(self.graphicsscene)
            self.Datagrid_Widget.show()
           
        else:
            print('-'*21+'请输入文件夹路径'+'-'*21)
 
    
    def Information(self):     # 导入TOOL.ini文件得到项目信息
        tooldirectory = QFileDialog.getOpenFileName(self,"打开TOOL.ini","C:\\",'TOOL.ini')
        if os.path.isfile(tooldirectory[0]):
            self.tooldirectory=tooldirectory
            self.haveinformation=1
            print(self.tooldirectory)
            output= codecs.open(self.tooldirectory[0],'r')
            linecache.updatecache(self.tooldirectory[0])
            linefile = linecache.getlines(self.tooldirectory[0])
            catchname=['MODELNAME','CHIP_ID','FACTORYNAME','SCREEN_ROWCHNUM','SCREEN_COLCHNUM','KEY_RX','KEY_TX','KEY_NUM','BOOT_VERISON','CORE_VERISON','CUSTOM_VERISON','PARAMETER_VERISON']
            checkfile =['AUTO_DOWNLOAD','CM_DELTA_ENABLE','SELF_CP_ENABLE','CP_SHORT_ENABLE','SELF_JITTER_ENALBE','CM_V_DIFF_ENABLE','CM_H_DIFF_ENABLE','CM_JITTER_ENABLE']     
            informationdir = dict()

            for l in linefile:
                for i in catchname:    
                    if l.find(i) != -1:
                        '''print( i,'=',l[26:])'''
                        '''informationdir[i]=l[26:-1]'''
                        informationdir[i]=((l[(l.find('='))+1:-1]).replace(' ','')).replace(',','')
            
                for j in checkfile:
                    if l.find(j) != -1:
                        '''print( j,'=',l[-2:])'''
                        informationdir[j]=(((l[(l.find('='))+1:(l.find('='))+5]).replace(' ','')).replace(',','')).replace('\n','')

            print(informationdir)
            linecache.clearcache()    
            output.close()        
            self.ModelNameLineEdit.setText(str(informationdir.get('MODELNAME','No find')))
            self.ICNameLineEdit.setText(informationdir.get('CHIP_ID','No find'))
            self.FactoryLineEdit.setText(informationdir.get('FACTORYNAME','No find'))
            self.RowumberLineEdit.setText(informationdir.get('SCREEN_ROWCHNUM','No find'))
            self.ColNumberLineEdit.setText(informationdir.get('SCREEN_COLCHNUM','Nofind'))
            self.KeyRowNumberLineEdit.setText(informationdir.get('KEY_RX','No find'))
            self.KeyColNumberLineEdit.setText(informationdir.get('KEY_TX','No find'))
            self.KeyNumNumberLineEdit.setText(informationdir.get('KEY_NUM','No find'))
            self.FW_BootLineEdit.setText(informationdir.get('BOOT_VERISON','No find'))
            self.FW_CoreLineEdit.setText(informationdir.get('CORE_VERISON','No find'))
            self.FW_CustomLineEdit.setText(informationdir.get('CUSTOM_VERISON','No find'))
            self.FW_ParamLineEdit.setText(informationdir.get('PARAMETER_VERISON','No find'))

        
    def writename(self):     # 写入更改后项目信息到模板TOOL.ini中
        autodownload=0
        cmdeltatest=0
        selfcptest=0
        selfshorttest=0
        selfjittertest=0
        vdifftest=0
        hdifftest=0
        jittertest=0
        if self.haveinformation == 0: #判断有没导入tool文件如果没有则导入tool模板
            self.tooldirectory=((self.filedir+'\\Templet\\TOOLtemplet.ini'),'TOOL.ini')    #('C:/Users/Administrator/Desktop/PyQttest/config/TOOL模板.ini','TOOL.ini')
        if self.AutoDownloadcheck.isChecked():
            autodownload=1
        if self.Cmdeltatestcheck.isChecked():
            cmdeltatest=1
        if self.Selfcptestcheck.isChecked():
            selfcptest=1
        if self.Selfshortcheck.isChecked(): 
            selfshorttest=1
        if self.Selfjittercheck.isChecked():
            selfjittertest=1
        if self.Vdifftestcheck.isChecked():
            vdifftest=1
        if self.Hdifftestcheck.isChecked():
            hdifftest=1
        if self.Jittertestcheck.isChecked(): 
            jittertest=1
        newcatchname=['MODELNAME','CHIP_ID','FACTORYNAME','SCREEN_ROWCHNUM','SCREEN_COLCHNUM','KEY_RX','KEY_TX','KEY_NUM','BOOT_VERISON','CORE_VERISON','CUSTOM_VERISON','PARAMETER_VERISON','AUTO_DOWNLOAD','CM_DELTA_ENABLE','SELF_CP_ENABLE','CP_SHORT_ENABLE','SELF_JITTER_ENALBE','CM_V_DIFF_ENABLE','CM_H_DIFF_ENABLE','CM_JITTER_ENABLE']
        newtext =[self.ModelNameLineEdit.text(),self.ICNameLineEdit.text(),self.FactoryLineEdit.text(),self.RowumberLineEdit.text(),self.ColNumberLineEdit.text(),str(self.KeyRowNumberLineEdit.text()),str(self.KeyColNumberLineEdit.text()),str(self.KeyNumNumberLineEdit.text()),str(self.FW_BootLineEdit.text()),str(self.FW_CoreLineEdit.text()),str(self.FW_CustomLineEdit.text()),str(self.FW_ParamLineEdit.text()),autodownload,cmdeltatest,selfcptest,selfshorttest,selfjittertest,vdifftest,hdifftest,jittertest]
        newinformation=dir()
        newinformation=dict(map(lambda x,y:[x,y],newcatchname,newtext)) 
        print (newinformation)
        newtool=(self.filedir+'\\Transitdata\\norealtool.ini')
        newoutput = codecs.open(newtool,'w','gbk','ignore')
        linecache.updatecache(self.tooldirectory[0])
        linefile = linecache.getlines(self.tooldirectory[0])
        for h in linefile:
            for key in newinformation:
                if h.find(key)!= -1:
                    w=list(h)
                    '''w =''.join(w[:26])'''
                    w =''.join(w[:(h.find('='))])
                    w = w+str(newinformation[key])+'\n'
                else:
                    w=h                    
            newoutput.write(w)  
        linecache.clearcache()
        newoutput.close()
        
        if self.getspec == 1:
            specfile = (self.filedir+'\\Transitdata\\maxandmindata.txt')
            toolfile = (self.filedir+'\\Transitdata\\norealtool.ini')
            newoutfile = (self.filedir+'\\Makefile\\NEWTOOL.ini')
            linecache.updatecache(specfile)
            linecache.updatecache(toolfile)
            speclines = linecache.getlines(specfile)
            toolfilelines= linecache.getlines(toolfile)
            linenumber = 0
            for line in toolfilelines:
                if line.find(';CM_DELTA_MAX')!=-1:
                    starlinenumber = linenumber
                if line.find(';FPCB_MAX')!=-1:
                    endlinenumber = linenumber
                linenumber+=1
            if starlinenumber != 0 and endlinenumber != 0:
                newoutputline=toolfilelines[:starlinenumber+1]+speclines+toolfilelines[endlinenumber-2:]
            linecache.clearcache()
            newout=codecs.open(newoutfile,'w')
            for newline in newoutputline:
                newout.write(newline)
            newout.close()

    def normalOutputWritten(self,text):
        """Append text to the QTextEdit."""
        cursor = self.TxtWidget.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.TxtWidget.setTextCursor(cursor)
        self.TxtWidget.ensureCursorVisible()
        

'''
class Testdatadiagram(QDialog):
    def __init__(self):
        super().__init__()
        self.Testdatadiagram()
        
    def Testdatadiagram(self):
        self.setWindowTitle('测试数据CM-Delta分布图')
        self.imageview=QLabel("测试数据分布图")
        self.vlayout=QVBoxLayout()
        self.vlayout.addWidget(self.imageview)
        self.setLayout(self.vlayout)
        self.file=os.path.split(os.path.abspath(sys.argv[0]))[0]
        self.imagefile=self.file+'\\Transitdata\\test.jpg'
        self.image=QImage(self.imagefile)
        self.imageview.setPixmap(QPixmap.fromImage(self.image))
        self.resize(self.image.width(),self.image.height())
    
    def showimage(self):
        if not self.isVisible():
            self.show()
'''

if __name__ == '__main__':
    try:
        app = 0
        app = QApplication(sys.argv)
        app.setStyleSheet('''
        QPushButton{
        background-color: rgb(51,153,255) ;
        height:18px;
        border-style: inset;
        border-width: 2px;
        border-radius: 9px;
        border-color: beige;
        font: bold 10px;
        min-width: 10em;
        padding: 6px;
        }
        
        QPushButton:hover {
        background-color: rgb(255,255,102);
        border-style: inset;
        }
        
        QPushButton:pressed {
        background-color: rgb(220, 0, 0);
        border-style: inset;
        }
        
        QPushButton:enabled:pressed{
        background: rgb(0, 78, 161);
        }
        
        QPushButton:!enabled {
        background: rgb(180, 180, 180);
        color: white;
        }
        
        QMenuBar {
        background: rgb(232,232,232);
        border-left: none;
        border-right: none;
        }
        
        QMenuBar::item {
        border: 1px solid transparent;
        padding: 5px 10px 5px 10px;
        background: transparent;
        }
        
        StyledWidget {
        background: rgb(232,232,232);
        qproperty-normalColor: rgb(232,232,232);
        qproperty-disableColor: rgb(232,232,232);
        qproperty-highlightColor: rgb(232,232,232);
        qproperty-errorColor: red;
        }
        
        QToolTip{
        border: 1px solid rgb(111, 156, 207);
        background: rgb(232,232,232);
        color: rgb(51, 51, 51);
        }
        
        QCheckBox::indicator {
        width: 13px;
        height: 13px;
        }
        
        QTextEdit {
        border: 1px solid rgb(105,105,105);
        border-radius: 3px;
        }
        
        QGroupBox {
        background: rgb(232,232,232);
        font-size: 14px;
        border: 1px solid rgb(105,105,105);
        border-radius: 3px;
        margin-top: 3px;
        }

        QGroupBox::title {
        color: rgb(105,105,105);
        subcontrol-origin: margin;
        left: 5px;
        margin-top: -7px;
        padding: 0 1px;
        }''')
        ex = Example()
        ex.show()            

    except:
        print ("Unexpected error:", sys.exc_info())#sys.exc_info()返回出错信息
        input('press enter key to exit') #放一个等待输入是为了不让程序退出
    sys.exit(app.exec_())    
