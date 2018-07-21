import os
import sys
import hashlib


class myconfig():
    defult = {'imgresize':'False','imgresize_x':'1.00','imgresize_y':'1.00',
        'featureMethod':'sift', 'searchRatio':'0.75', 'offsetCaculate':'众数',
        'offsetEvaluate':'2.5', 'direction':'行拼接', 'method':'0','fusion':'无融合'}
    def setDefault(self):
        #设置默认参数

        return self.defult

    def read(self, fileName):
        #读取配置信息
        f = open("./config/" + fileName, 'r')
        mode={}
        for line in f.readlines():

            if not line:
                continue
            line = line.strip()
            mode[line.split(":")[0]] = line.split(":")[-1]

        f.close()
        for key in self.defult:
            if not key in mode:
                mode[key]=self.defult[key]
        return mode

    def create(self, fileName, mode):
        #新建配置文件
        s=[]
        f = open("./config/" + fileName, 'w')
        for key in mode:
            s.append(key+":"+mode[key]+"\n")
        f.writelines(s)
        f.close()

    def reset(self, fileName, mode):
        #更新配置文件
        s = []
        f = open("./config/" + fileName, 'w')
        for key in mode:
            s.append(key + ":" + mode[key] + "\n")
        f.writelines(s)
        f.close()
    def delFile(self,fileName):
        # 删除配置文件
        f="./config/"+fileName
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