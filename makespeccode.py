# -*- coding: utf-8 -*-

"""
Created on Sat Jun 24 09:24:05 2017
@author: Celfras--Levi
"""

import os
import codecs
import linecache2 as linecache
import numpy as np

def Maketestdataspec(inputfiledirectory,vatargetpercent,keytargetpercent,outputaveragefile,alldataoutputfile,outputmaxsetspec,outputminsetspec):
    
    def filedirectorycatchdata(filedirectory):                   #获取log csv文件数据 输出格式为[[all屏体数据][all按键数据]]数组
        global L,usefuldatafile
        listfile = os.listdir(filedirectory)
        L=[filename for filename in listfile if filename[-4:]=='.csv'and not filename.find('summary')!= -1]
        print('   '+'-'*19+'导入文件'+'-'*20)
        
        alldata=[]
        allsampledata=[]
        allsamplekeydata=[]
        allsamplecptestdata=[]
        allsamplecpshortdata=[]
        nodatafile=[]
        usefuldatafile=[]

        for fileadr in L:
            try:                                                    #解决文件存在非法编码导致无法linecache问题
                linecache.updatecache(filedirectory+fileadr)
                linefile = linecache.getlines(filedirectory+fileadr)
            except Exception:
                print(str(fileadr)+'该文件数据存在非法字符')
                newfile=codecs.open(filedirectory+fileadr,'r','gbk','ignore')
                text=newfile.read()
                newfile.close()
                with codecs.open(filedirectory+fileadr,'w') as newfile2:
                    newfile2.write(text)
                linecache.updatecache(filedirectory+fileadr)
                linefile = linecache.getlines(filedirectory+fileadr)
            '''print(filedirectory+fileadr)'''
            linenumber= 0
            starline = 0
            endline = 0
            sampledata=[]
            keyarray=[]
            
            cpteststartline=0
            cptestendline=0
            cpshortstartline=0
            cpshortendline=0
            sampledata=[]
            keyarray=[]
            samplecpselfdata=[]
            samplecpshortdata=[]
            
            for line in linefile:
                linenumber+=1    
                if line.find('CMDelta Test Start') != -1:
                    starline = linenumber

                if line.find('CMDelta Test End') != -1:
                    endline = linenumber   
                    
                if line.find('Self Cp Test Start')!= -1:#加入Self CP test 
                    cpteststartline=linenumber 
            
                if line.find('Self Cp Test End')!= -1:
                    cptestendline=linenumber
            
                if line.find('CP_SHORT Test Start')!= -1:#加入CP Short test 
                    cpshortstartline=linenumber
                    #print(cpshortstartline)

                if line.find('CP_SHORT Test End')!= -1:
                    cpshortendline=linenumber
            datanumber = 0
       
            if starline !=0 and endline !=0:
                dataline = linefile[starline:endline]    

                for data in dataline:
                    if data.find('[Row00]') != -1:
                        datastar = datanumber
                    if data.find('CM Delta Key') != -1:
                        dataend = datanumber   
                    datanumber+=1
                keydata=dataline[dataend:endline]
                del keydata[0]
                del keydata[-1]
                keyarray=[]
            
                for k in keydata:
                    if k == '\n':
                        pass
                    else:
                        keyread=k.split(',')
                        keyrealdata=keyread[:-1]
                        for i in keyrealdata:
                            if i ==''or i=='\n':
                                pass
                            else:
                                newkey=(((((i.replace('[','')).replace(']','')).replace('{','')).replace('}','')).replace('\n','')).replace('\t','')
                                keyarray.append(int(newkey))

                data = dataline[datastar:dataend-1]
                for datare in data:
                    if datare =='\n':
                        pass
                    else:
                        dataread=datare.split(',')
                        d=dataread[1:]
                        slist=[]
                        for s in d:
                            if s==''or s=='\n':
                                pass
                            else:
                                news=(((((s.replace('[','')).replace(']','')).replace('{','')).replace('}','')).replace('\n','')).replace('\t','')
                                slist.append(int(news))
                        if len(slist)!=0:
                            sampledata.append(slist)
                usefuldatafile.append(str(fileadr))
            else:
                nodatafile.append(str(fileadr))
            
            if(len(sampledata)!=0):
                allsampledata.append(sampledata)
            if(len(keyarray)!=0):
                allsamplekeydata.append(keyarray)
            
            if cpteststartline !=0 and cptestendline !=0:#提取 Self CP 测试数据
                #print('try to catch self cp data')
                selfcpdatanumber=0
                selfcpdataline=linefile[cpteststartline:cptestendline]

                for selfcpdata in selfcpdataline:
                    if selfcpdata.find('Row00')!=-1:
                        selfdatastart=selfcpdatanumber
                    if selfcpdata.find(' Self Cp Test End')!=-1:
                        selfdataend=selfcpdatanumber
                    selfcpdatanumber+=1
                    
                selfcpdatafile=selfcpdataline[selfdatastart:selfdataend]

                for datare in selfcpdatafile:
                    if datare =='\n':
                        pass
                    else:
                        dataread=datare.split(',')
                        d=dataread[1:]
                        slist2=[]                
                        for s in d:
                            if s==''or s=='\n':
                                pass
                            else:
                                news=(((((s.replace('[','')).replace(']','')).replace('{','')).replace('}','')).replace('\n','')).replace('\t','')
                                slist2.append(int(news))
                        if len(slist2)!=0:
                            samplecpselfdata.append(slist2)
            if(len(samplecpselfdata)!=0):
                #print(samplecpselfdata)
                allsamplecptestdata.append(samplecpselfdata)

            if cpshortstartline !=0 and cpshortendline !=0:#提取 CP SHORT 测试数据
                #print('try to catch SHORT data')
                selfshortnumber=0
                cpshortline=linefile[cpshortstartline:cpshortendline]
                #print(cpshortline)
                
                for cpshortdata in cpshortline:
                    if cpshortdata.find('Row00') !=-1:
                        cpshortstart=selfshortnumber
                    if cpshortdata.find(' CP_SHORT Test End') !=-1:
                        cpshortend=selfshortnumber
                    selfshortnumber+=1
        
                cpshortfile=cpshortline[cpshortstart:cpshortend]
                
                #print(cpshortfile)
                for datare in cpshortfile:
                    if datare =='\n':
                        pass
                    else:
                        dataread=datare.split(',')
                        d=dataread[1:]
                        slist3=[]                
                        for s in d:
                            if s==''or s=='\n':
                                pass
                            else:
                                news=(((((s.replace('[','')).replace(']','')).replace('{','')).replace('}','')).replace('\n','')).replace('\t','')
                                slist3.append(int(news))
                        if len(slist3)!=0:
                            samplecpshortdata.append(slist3)
            if(len(samplecpshortdata)!=0):
                #print(samplecpshortdata)
                allsamplecpshortdata.append(samplecpshortdata) 

        print('*'*19+'数据不存在样品'+'*'*19)
        print(nodatafile)
        print('\n')
        '''print('-'*19+'有效文件'+'-'*19)
        print(usefuldatafile)'''
        alldata.append(allsampledata)
        if (len(allsamplekeydata)!=0):
            alldata.append(allsamplekeydata)
        return alldata


    def makespec(testsampledata,targetpercent):
        def makeaverage(sampledata2):
            b=(np.array(sampledata2[0]))*0
            for i in sampledata2:
                j = np.array(i)
                b = b+j
            average = b//(len(sampledata2))
            return average
    
        havengsample = 1 
        ngfileadr=[]
      
        while havengsample == 1:
            print('-'*19+'判断良品中'+'-'*19)
            print('数目：',len(testsampledata))
            print('\n')
            sampleaverage=makeaverage(testsampledata)
            percentarray=[]
            diffvaluearray=[]
                                        
            for data in testsampledata:
                specvalue=abs(((np.array(data))/sampleaverage)-1)
                percentarray.append(specvalue)
        
                diffvalue=abs((np.array(data)-sampleaverage))
                diffvaluearray.append(diffvalue)
            
            testsamplenumber=0
            samplenumber = 0
            ngsamplenumber=[]
            havengsample = 0
            percentarray=np.nan_to_num(percentarray)
            diffvaluearray=np.nan_to_num(diffvaluearray)
                
            for samplepercent in percentarray:
                maxpercent = np.max(samplepercent)
                if maxpercent >= targetpercent:
                
                    singellinepercent = samplepercent.flatten() #样品数据从二维变为一维方便比较
                    singellinediff = (diffvaluearray[testsamplenumber]).flatten()   #样品测试数值与average值的差值从二维变为一维方便比较     
                    b= np.arange(len(singellinepercent))
                    c= b[singellinepercent>=targetpercent] # c array 存放的是单个样品中大于targetpercent位置的索引 

                    for i in range(len(c)):
                        if singellinediff[c[i]]>5:
                            havengsample=1
                            ngsamplenumber.append(testsamplenumber)
                            del testsampledata[samplenumber]
                            samplenumber-=1
                            break

                testsamplenumber+=1
                samplenumber+=1 
             
            if havengsample ==1:
                for ng in ngsamplenumber:
                    ngfileadr.append(L[ng])
        print('*'*19+'VA区不良样品'+'*'*19)
        print(ngfileadr)
        print('VA区不良样品总数：',len(ngfileadr))
        print('\n')
        '''print(sampleaverage)'''
        return sampleaverage
  
    def makekeyspec(samplekeydata,targetpercent):
        def makekeyaverage(data):
            b=np.array(data[0])*0
            for i in data:
                j = np.array(i)
                b=b+j
            average=b//len(data)
            return average
        
        havengsample =1
        ngfileadr=[]
     
        while havengsample ==1:
            print('-'*19+'判断按键良品中'+'-'*19)
            print('数目：',len(samplekeydata))
            samplekeyaverage=makekeyaverage(samplekeydata)
            percentarray=[]
            diffvaluearray=[]
         
            for data in samplekeydata:
                specvalue=abs((((np.array(data))/samplekeyaverage)-1))
                percentarray.append(specvalue)
             
                diffvalue=abs((np.array(data))-samplekeyaverage)
                diffvaluearray.append(diffvalue)
             
            testsamplenumber=0
            samplenumber = 0
            ngsamplenumber=[]
            havengsample = 0    
        
            percentarray=np.nan_to_num(percentarray)
            diffvaluearray=np.nan_to_num(diffvaluearray)
         
            for samplepercent in percentarray:
                maxpercent = np.max(samplepercent)

                if maxpercent >= targetpercent:
                    maxlocation=np.where(samplepercent==np.max(samplepercent))

                    maxdatanumbers=len(maxlocation)
                    diffarray=[]
                 
                    while (maxdatanumbers >= 1):
                        x=0
                        row=maxlocation[x]
                        diff=diffvaluearray[testsamplenumber][row]
                        diffarray.append(diff)
                        maxdatanumbers-=1
                        x+=1
                     
                    maxdiff=np.max(diffarray)
                    if (maxdiff <=5):
                        samplenumber+=1
                        break
                    else:
                        havengsample=1
                        ngsamplenumber.append(testsamplenumber)
                        del samplekeydata[samplenumber]
                     
                    testsamplenumber +=1
                
                else:
                    samplenumber +=1
                    testsamplenumber +=1
                
            if havengsample ==1:      
                for ng in ngsamplenumber:
                    ngfileadr.append(L[ng])
        print('*'*19+'按键不良样品'+'*'*19)
        print(ngfileadr)
        print('\n')        
        return samplekeyaverage            
                
    def writeaveragearray(file,average):
        output = codecs.open(file,'w')
        linenumber=0
        for line in average:
            output.write('CM_DELTA_ROW'+ str("%02d" %linenumber) +' ' +'='+'  ')
            inumber=0
            for i in line:
                if inumber == (len(line)-1):
                    output.write(str(i)+'\n')
                else:
                    output.write(str(i)+','+'   ')
                inumber+=1                  
            linenumber+=1
        output.close()

    def writeaveragemaxminarray(file,average,maxsetspec,minsetspec):
        output = codecs.open(file,'w')
        linenumber=0
        havekey=0
    
        if len(average)==1:
            averagemax = (np.array(average[0]))*(1+maxsetspec)
            averagemin = (np.array(average[0]))*(1-minsetspec)
            havekey=0
      
        elif len(average)==2:
            havekey=1
            averagemax = (np.array(average[0]))*(1+maxsetspec)
            averagemin = (np.array(average[0]))*(1-minsetspec)
            keymax=(np.array(average[1]))*(1+maxsetspec)
            keymin=(np.array(average[1]))*(1-minsetspec)
            '''print(averagemax)
            print(averagemin)
            print(keymax)
            print(keymin)'''        
        
        for line in averagemax:
            output.write('CM_DELTA_MAX_ROW'+ str("%02d" %linenumber) +' ' +'='+'  ')
            inumber=0
            for avdata in line:
                if avdata==0:
                    avdata=5
                else:
                    pass
            
                if inumber ==(len(line)-1):
                    output.write(str(int(avdata))+'\n')
                else:
                    output.write(str(int(avdata))+','+'   ')
                inumber +=1
            linenumber+=1
        
        if havekey==1:
            output.write('CM_DELTA_MAX_KEY'+'   '+'='+'  ')
            inumber=0
            for i in keymax:
                if i==0:
                    i=5
                else:
                    pass
                if inumber ==(len(keymax)-1):
                    output.write(str(int(i))+'\n')
                else:
                    output.write(str(int(i))+','+'   ')
                inumber+=1
    
        output.write('\n'+'\n'+'; cm delta min'+'\n')
        linenumber=0
    
        for line in averagemin:
            output.write('CM_DELTA_MIN_ROW'+ str("%02d" %linenumber) +' ' +'='+'  ')
            inumber=0
            for i in line:
                if inumber ==(len(line)-1):
                    output.write(str(int(i))+'\n')
                else:
                    output.write(str(int(i))+','+'   ')
                inumber +=1
            linenumber+=1        
        
        if havekey==1:
            inumber=0
            output.write('CM_DELTA_MIN_KEY'+'   '+'='+'  ')
            for i in keymin:
                if i==0:
                    i=5
                else:
                    pass
                if inumber ==(len(keymin)-1):
                    output.write(str(int(i))+'\n')
                else:
                    output.write(str(int(i))+','+'   ')
                inumber+=1            
        output.close()
    averagedata=[]  
    sampleplotdata=[]
    
    #def makecpselfspec(samplecpdata,maxspec,minspec):
        
    
    if len(filedirectorycatchdata(inputfiledirectory))==1 and len(usefuldatafile)!=0:
        dataoutput=codecs.open(alldataoutputfile+'alldata.csv','w+')
        d=filedirectorycatchdata(inputfiledirectory)    
        for i in range(len(d[0])):
            dataoutput.write(str(usefuldatafile[i])+',')
            dataoutput.write(((str((np.array(d[0][i]).flatten()).tolist())).replace('[','')).replace(']',''))
            dataoutput.write('\n')
            sampleplotdata.append((np.array(d[0][i]).flatten()).tolist())
        dataoutput.close()
        averagedata.append(makespec(d[0],vatargetpercent))
        
    elif len(filedirectorycatchdata(inputfiledirectory))==2 and len(usefuldatafile)!=0:
        dataoutput=codecs.open(alldataoutputfile+'alldata.csv','w+')
        d=filedirectorycatchdata(inputfiledirectory)
        for i in range(len(d[0])):
            dataoutput.write(str(usefuldatafile[i])+',')
            dataoutput.write(((str(((np.array(d[0][i]).flatten()).tolist())+((np.array(d[1][i]).flatten()).tolist()))).replace('[','')).replace(']',''))
            dataoutput.write('\n')
            sampleplotdata.append(((np.array(d[0][i]).flatten()).tolist())+((np.array(d[1][i]).flatten()).tolist()))
        dataoutput.close()
        averagedata.append(makespec(d[0],vatargetpercent))
        averagedata.append(makekeyspec(d[1],keytargetpercent))

    writeaveragemaxminarray(outputaveragefile,averagedata,outputmaxsetspec,outputminsetspec)
    print('<<<<<<<<<样品数据已保存在Tarnsitdata文件夹>>>>>>>>>')
    return sampleplotdata

 

'''Maketestdataspec("C:/Users/Administrator/Desktop/PyQttest/Pixdata/",0.3,0.3,"C:/Users/Administrator/Desktop/PyQttest/averagefile/average.txt",'C:/Users/Administrator/Desktop/UItesttool/allsampledata/',0.3,0.3)'''

'''if len(usefuldatafile)!=0:
        long=len(sampleplotdata[0])
        makelocator=int((sampleplotdata[0][int(long/2)]+200)/50) #自定义计算网格刻度的单位值，方便不同样品值不一样时刻度太小，设定的值为第一个样品中间值除以50后加4
    
        xmajorlocator=MultipleLocator(makelocator)
        xmajorformatter=FormatStrFormatter('%d')
        xminorforlocator=MultipleLocator(makelocator)
    
        ymajorlocator=MultipleLocator(makelocator)
        ymajorformatter=FormatStrFormatter('%d')
        yminorforlocator=MultipleLocator(makelocator)
    
        plt.figure(figsize=(20,10))
        ax=plt.gca()
        
        for i in sampleplotdata:
            plotdata=[int(j) for j in i]
            plt.plot(range(long),plotdata,'g-')
        ax.xaxis.set_major_locator(xmajorlocator)
        ax.xaxis.set_major_formatter(xmajorformatter)
    
        ax.yaxis.set_major_locator(ymajorlocator)
        ax.yaxis.set_major_formatter(ymajorformatter)
    
        ax.xaxis.set_minor_locator(xminorforlocator)  
        ax.yaxis.set_minor_locator(yminorforlocator)
    
        ax.xaxis.grid(True, which='major') 
        ax.yaxis.grid(True, which='minor')
        plt.savefig(alldataoutputfile+'test.jpg')
        print('<<<<<<<<<样品数据和数据分布图已保存在Tarnsitdata文件夹>>>>>>>>>')'''
