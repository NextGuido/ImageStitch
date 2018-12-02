import os
import sys
import hashlib
import globalvar as gl

class myconfig():
    # default = {'imgresize':'False','imgresize_x':'1.00','imgresize_y':'1.00',
    #     'featureMethod':'sift', 'searchRatio':'0.75', 'offsetCaculate':'众数',
    #     'offsetEvaluate':'2.5', 'direction':'行拼接', 'method':'0','fusion':'无融合'}
    default={'imgresize':'False','imgresize_x':'1.000', 'imgresize_y':'1.000',
             'featureMethod':'surf', 'searchRatio':'0.750','offsetCaculate':'众数',
             'offsetEvaluate':'3','direction':'左向拼接','method':'全局','fusion':'无融合'}
    def __init__(self):
        self.configpath=gl.get_value('programData')+'/imageStitchConfig/'
        if not os.path.exists(self.configpath):
            os.makedirs(self.configpath)
    def setDefault(self):
        #设置默认参数
        return self.default
    def getList(self):
        items=[]
        for fn in os.listdir(self.configpath):
            items.append(fn)
        return items
    def read(self, fileName):
        #读取配置信息
        f = open(self.configpath+ fileName, 'r')
        mode={}
        for line in f.readlines():

            if not line:
                continue
            line = line.strip()
            mode[line.split(":")[0]] = line.split(":")[-1]

        f.close()
        for key in self.default:
            if not key in mode:
                mode[key]=self.default[key]
        return mode

    def create(self, fileName, mode):
        #新建配置文件
        s=[]
        f = open(self.configpath + fileName, 'w')
        for key in mode:
            s.append(key+":"+mode[key]+"\n")
        f.writelines(s)
        f.close()

    def reset(self, fileName, mode):
        #更新配置文件
        s = []
        f = open(self.configpath + fileName, 'w')
        for key in mode:
            s.append(key + ":" + mode[key] + "\n")
        f.writelines(s)
        f.close()
    def delFile(self,fileName):
        # 删除配置文件
        f=self.configpath+fileName
        os.remove(f)
    # def setPassword(self,password):
    #     #设置密码并加密
    #     f=open("./user.ini",'w')
    #     h=hashlib.md5()
    #     h.update(password.encode(encoding='utf-8'))
    #     f.write(h.hexdigest())
    # def matchPassword(self,password):
    #     #密码验证
    #     f = open("./user.ini", 'r')
    #     h = hashlib.md5()
    #     h.update(password.encode(encoding='utf-8'))
    #     if h.hexdigest()==f.read():
    #         return True
    #     else:
    #         return False
    # def delPassword(self):
    #     f=open("./user.ini",'w')
    #     f.write("")