import os
import uuid
import re
import shutil
class Info:
    oldword=""
    newword=""
    count=0

    def __init__(self,oldword,newword):
        self.oldword=oldword
        self.newword=newword


def copy_to(infilepos,outfilepos):
    infile=open(infilepos,mode="r",encoding="utf-8")
    outfile=open(outfilepos,mode="w",encoding="utf-8")
    outfile.writelines(infile)
    infile.close()
    outfile.close()

def delete_symbol(infilepos: str, symbol="#main"):
    '''
    删除 一对#main之间的代码段
    #main
    .......................
    #main
    '''
    infile=open(infilepos,mode="r",encoding="utf-8")
    lines=list(infile)
    infile.close()
    start=-1
    end=-1
    num=int((str(lines).count(symbol)+1)/2)
    for i in range(num):
        start=-1
        end=-1
        for i in range(len(lines)):
            line=lines[i]
            ind=re.match(symbol,line)
            if(ind!=None and start!=-1):
                end=i
                print("start:",start)
                print("end:",end)
                break
            if(ind!=None and start==-1):
                start=i
            
            if(i==len(lines)-1 and ind!=None and start!=-1 and end==-1):
                end=len(lines)-1
        if(start!=-1 and end!=-1):
            del lines[start:end+1]
    
    writeto=open(infilepos,mode="w",encoding="utf-8")
    for line in lines:
        writeto.write(line)
    writeto.close()

def delete_symbol_start_to_end(infilepos:str,startsymbol="#main",endsymbol="#main"):
    '''
    删除 startsymbol和endsymbol之间的代码段 要求有序
    startsymbol
    .......................
    endsymbol
    '''
    infile=open(infilepos,mode="r",encoding="utf-8")
    lines=list(infile)
    infile.close()
    start=-1
    end=-1
    num=int((str(lines).count(startsymbol)+1))
    for i in range(num):
        start=-1
        end=-1
        for i in range(len(lines)):
            line=lines[i]
            
            ind=line.strip().count(endsymbol)>0
            if(start==-1):
                ind=line.strip().count(startsymbol)>0
                
            if(ind!=False and start!=-1):
                end=i
                print("start:",start)
                print("end:",end)
                break
            if(ind!=False and start==-1):
                start=i
            
            if(i==len(lines)-1 and ind!=False and start!=-1 and end==-1):
                end=len(lines)-1
        if(start!=-1 and end!=-1):
            print("删除")
            del lines[start:end+1]
    
    writeto=open(infilepos,mode="w",encoding="utf-8")
    for line in lines:
        writeto.write(line)
    writeto.close()

def printReplaceResult(InfoList):
    for entity in InfoList:
        print("oldword: ",entity.oldword," 替换次数是",entity.count)

#单行替换
def doReplaceSetElement(line:str,entity:Info):
    templine=""
    entity.count=entity.count+line.count(entity.oldword)
    templine=line.replace(entity.oldword,entity.newword)
    return templine

#循环文件内替换
def doReplaceSet(infilepos:str,outfilepos:str,entitylist):
    flag=False#不使用同一个文件进行操作
    if(os.path.abspath(infilepos)==os.path.abspath(outfilepos)):
        flag=True
    if(flag==True):
        outfilepos=str(uuid.uuid1())+".txt"
    infile=open(infilepos,mode="r",encoding="utf-8")
    outfile=open(outfilepos,mode="w",encoding="utf-8")
    
    tmp=""
    for line in infile:
        tmp=line
        for entity in entitylist:
            tmp=doReplaceSetElement(tmp,entity)
        outfile.write(tmp)
    infile.close()
    outfile.close()
    if(flag==True):
        readfrom=open(outfilepos,mode="r",encoding="utf-8")
        writeto=open(infilepos,mode="w",encoding="utf-8")
        for line in readfrom:
            writeto.write(line)
        readfrom.close()
        writeto.close()
        os.remove(outfilepos)

#单行附加 direction=True放在前面
def doAppendSetElement(line:str,entity:Info,direction=True,end=False):
    templine=line
    oldcount=line.count(entity.oldword)
    if(oldcount==0):
        return line
    currentpos=0
    while(oldcount>0):
        currentpos=templine.find(entity.oldword,currentpos,len(templine))
        
        if(currentpos<0):
            currentpos=0
        linelist=list(templine)
        if(direction==True):
            linelist.insert(currentpos,entity.newword)#-
        else:
            linelist.insert(currentpos-len(entity.oldword),entity.newword)#+
        templine=''.join(linelist)
        
        if(direction==True):
            currentpos=currentpos+len(entity.oldword)-1
        else:
            currentpos=currentpos-len(entity.oldword)-1
        oldcount=oldcount-1
        templine.replace(entity.oldword,"",1)
        if(end==True):
            templine=templine
            templine.replace(entity.oldword,"")
        else:
            print("末尾添加:",str(templine))
            templine.replace(entity.oldword,"")
    return str(templine)

#循环文件内替换
def doAppendSet(infilepos:str,outfilepos:str,entitylist):
    flag=False#不使用同一个文件进行操作
    if(os.path.abspath(infilepos)==os.path.abspath(outfilepos)):
        flag=True
    if(flag==True):
        outfilepos=str(uuid.uuid1())+".txt"
    infile=open(infilepos,mode="r",encoding="utf-8")
    outfile=open(outfilepos,mode="w",encoding="utf-8")
    result=""
    tmp=""
    for line in infile:
        tmp=line
        i=0
        for entity in entitylist:
            if(tmp.count(entity.oldword)==0):
                continue
            if(i==len(entitylist)-1):
                tmp=doAppendSetElement(tmp,entity,end=False)
                #print("tmp 1")
            else:
                tmp=doAppendSetElement(tmp,entity,end=True)
                #print("tmp 2")
            i=i+1
        outfile.write(tmp)
    infile.close()
    outfile.close()
    if(flag==True):
        readfrom=open(outfilepos,mode="r",encoding="utf-8")
        writeto=open(infilepos,mode="w",encoding="utf-8")
        for line in readfrom:
            writeto.write(line)
        readfrom.close()
        writeto.close()
        os.remove(outfilepos)

#读取文件内的替换model
def readModel(infilepos,skipsymbol='##'):
    infile=open(infilepos,mode="r",encoding="utf-8")
    templine=""
    for line in infile:
        if(skipsymbol!=None and line.startswith(skipsymbol)):
            continue
        templine=templine+line
    infile.close()
    return templine

def readModelList(infilepos,skipsymbol='##'):
    infile=open(infilepos,mode="r",encoding="utf-8")
    templine=[]
    for line in infile:
        if(skipsymbol!=None and line.startswith(skipsymbol)):
            continue
        templine.append(line)
    infile.close()
    return templine

#在appendpos添加由modelname指定的model,replacelist指定model内容的替换
def createModelAndReplace(infilepos:str,outfilepos:str,modelname,appendpos,replacelist):
    tmpfile = str(uuid.uuid1())
    shutil.copyfile(modelname, tmpfile)
    doReplaceSet(tmpfile, tmpfile, replacelist)
    
    appendlist=[]
    div=readModel(tmpfile)
    appendlist.append(Info(appendpos,div))
    doAppendSet(infilepos, outfilepos, appendlist)
    
    printReplaceResult(replacelist)
    print("添加指定model:", modelname, "")
    
    os.remove(tmpfile)


def createModelAndReplaceAndDelete(infilepos:str,outfilepos:str,modelname,appendpos,replacelist,deletelist=None):
    '''
    deletelist: [{'start':"",'end':""}]
    '''

    tempfile=str(uuid.uuid1())+".txt"
    #复制模板至新文件
    copy_to(modelname,tempfile)
    #新文件内执行替换操作
    doReplaceSet(tempfile,tempfile,replacelist)
    if(deletelist!=None and isinstance(deletelist,list)):
        for deletepair in deletelist:
            delete_symbol_start_to_end(tempfile,deletepair['start'],deletepair['end'])
    #添加
    appendlist=[]
    div=readModel(tempfile)
    appendlist.append(Info(appendpos,div))
    doAppendSet(infilepos,outfilepos,appendlist)
    printReplaceResult(replacelist)
    os.remove(tempfile)

if __name__ == "__main__":
    infilepos="in.txt"
    outfilepos="out.txt"
    
    chg="CHG_1222113"
    replacelist=[]
    
    replacelist.append(Info("DataCLASS","xxxx"))
    replacelist.append(Info("OperationCLASS","xxxxxx"))
    
    doReplaceSet(infilepos,outfilepos,replacelist)

    model="abc.txt"
    replacelist=[]
    replacelist.append(Info("DATA","zzzzzz"))
    createModelAndReplace(outfilepos,outfilepos,model,"CODESHERE",replacelist)

    
    #消除标记
    replacelist=[]
    replacelist.append(Info("CODESHERE",""))
    replacelist.append(Info("MESSAGEPOS",""))
    doReplaceSet(outfilepos,"c.txt",replacelist)



