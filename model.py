import re
import json
import os

#记录各个位置
class Position:
    def __init__(self) -> None:
        pass
#模板文件的存储
class TemplateModel:
    __path:str
    __positions:list

    def __init__(self,path) -> None:
        self.__path=path
        self.__positions=self.scan(None)

    def get_path(self)-> str:
        return self.__path
    
    def get_positions(self)-> str:
        return self.__positions

    #扫描模板 确定模板中需要的所有值
    def scan(self,lines):
        if(lines==None):
            infile=open(self.__path,mode="r",encoding="utf-8")
            lines=infile.readlines()
            infile.close()
        finalline=""
        for line in lines:
            line=str(line)
            if(len(line)>0):
                finalline=finalline+line
        positions=group_by(finalline)
        return positions
class ModelSet:
    __modelset:dict
    def __init__(self) -> None:
        self.__modelset={}
    
    def add(self,model):
        errors=[]
        if(isinstance(model,TemplateModel)):
        #if(type()isinstance is not TemplateModel):
            for position in model.get_positions():
                #print("position:"+str(position))
                print("__modelset:"+str(self.__modelset))
                temp=self.__modelset.get(position["name"])
                if(temp is None):
                    self.__modelset.update({position["name"]:position})
                elif(position["type"]==temp["type"]):
                    pass
                else:
                    errors.append(position)
            if(len(errors)>0):
                errorsMsg=""
                errorsMsg=errorsMsg+" path:"+model.get_path()+"\n"
                for item in errors:
                    errorsMsg=errorsMsg+"=>"+str(item)+"\n"
                raise Exception("find errors : "+str(errorsMsg))
        else:
            raise Exception("not type:TemplateModel")
    def get_model_set(self):
        return self.__modelset

# 遍历文件夹及其子文件夹中的文件，并存储在一个列表中
# 输入文件夹路径、空文件列表[]
# 返回 文件列表Filelist,包含文件名（完整路径）
def get_filelist(dir, Filelist):
    newDir = dir
    if os.path.isfile(dir) and str(dir).endswith(".model"):
        Filelist.append(dir)
        # # 若只是要返回文件文，使用这个
        # Filelist.append(os.path.basename(dir))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            #if s == "xxx":
                #continue
            newDir=os.path.join(dir,s)
            get_filelist(newDir, Filelist)
    return Filelist

#从文件夹及子文件夹加载 model，后缀为 model
def load_models_from_path(dir)-> ModelSet:
    modelset=ModelSet()
    model_dir_list=get_filelist(dir,[])
    for model_dir in model_dir_list:
        model=TemplateModel(model_dir)
        if(len(model.get_positions())>0):
            modelset.add(model)
            print("load model from path:"+str(model_dir))
        else:
            print("unable to load model from path:"+str(model_dir))
    return modelset
def format_kv(text):
    text=str(text)
    text=text.replace("'","").replace(" ","").replace("{","").replace("}","")
    return text

def group_by(input):
    input=str(input).strip().replace("\n","").replace(" ","")
    # print("input:"+str(input).strip())
    positions=[]
    pattern = re.compile(r"@\{.*?\}@")
    result=pattern.findall(str(input))
    if(result is not None):
        for gr in result:
            if(gr is not None):
                gr=gr[1:-1]
                try:
                    gr=format_kv(gr)
                    attrs=str(gr).split(",")
                    temp=""
                    for attr in attrs:
                        if(len(attr)>0):
                            pair=attr.split(":")
                            if(len(pair)==2):
                                temp=temp+f""""{pair[0]}":"{pair[1]}","""
                            else:
                                raise Exception("不能解析"+attr)
                    if(str(temp).endswith(",")):
                        temp=temp[0:-1]
                    gr=json.loads("{"+temp+"}")
                    print("final gr"+str(gr))
                    positions.append(gr)
                except:
                    raise Exception("scan error")
    return positions
        
if __name__ == '__main__':
    folder=os.path.dirname(__file__)
    filepath=folder+"/models/a.model"
    model=TemplateModel(filepath)
    m = re.search('(?<=abc)def', 'abcdef')
    print(m.group(0))
    dic={}
    dic.update(eval("""{'name': 'ABC', 'type': 'Model'}""".replace("'",'"')))
    

    print(model.scan(None))

    model_set=load_models_from_path(folder)
    for key in (model_set.get_model_set()):
        print(str(key))
        print(model_set.get_model_set().get(key))