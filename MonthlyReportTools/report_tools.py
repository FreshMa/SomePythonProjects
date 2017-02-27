# -*- coding: utf-8 -*-
import requests
import json
import time
import csv
from operator import itemgetter

class ipCount():
    src_ip_list = []
    dest_ip_list = []
    src_ip_dic = {}
    dest_ip_dic = {}
    uni_src_ip_list = []
    
    def __init__(self,filename):  
        self.filename = filename
        self.lines = self.__get_lines(self.filename)
        self.__set_src_ip()
        self.__set_dest_ip()
        self.uni_src_ip_list = self.__get_uni_ip_list()
        
    def __get_lines(self,filename):
        '''
        将csv文件中的内容读到lines变量中，此后就不对文件进行操作了
        '''
        lines = []
        with open (filename,'rb') as f:
            result = csv.reader(f,dialect = 'excel')
            for line in result:
                if line[0].isdigit():
                    lines.append(line)
        return lines
    
    def __set_src_ip(self):
        for line in self.lines:
            if(line[8][0].isdigit() and not self.__is_inner_ip(line[8])):
                self.src_ip_list.append(line[8])
                self.src_ip_dic.setdefault(line[8],0)
                self.src_ip_dic[line[8]] += 1
            
    def __set_dest_ip(self):
        for line in self.lines:
            #存在 已合并 这种数据，需要isdigit来判断
            if(line[9][0].isdigit()):
                self.dest_ip_list.append(line[9])
                self.dest_ip_dic.setdefault(line[9],0)
                self.dest_ip_dic[line[9]] += 1
            
    def __get_uni_ip_list(self):
        for k,v in self.src_ip_dic.items():
            self.uni_src_ip_list.append(k)
        return self.uni_src_ip_list
    
    def print_top_ip(self):
        '''
        该函数统计攻击次数最多和被攻击次数最多的IP
        并对攻击源IP TOP列表中的IP的攻击类型进行统计，输出到屏幕上
        '''
        l1 = sorted(self.src_ip_dic.items(),key = itemgetter(1),reverse = True)
        print u'攻击源IP TOP5：'
        for i in range(5):
            print '\ntop %2d:\t%-18s 次数：%-7d'%(i+1,l1[i][0],l1[i][1])
            #对TOP IP列表中的每一个IP，统计它的具体攻击类型
            temp_dic = {}
            temp_li = []

            #先筛选出源IP 与TOP IP相同的行，保存到temp_li列表中
            for line in self.lines:
                if line[8] == l1[i][0]:
                    temp_li.append(line)
            #利用字典进行统计
            for j in temp_li:
                temp_dic.setdefault(j[2],0)
                temp_dic[j[2]] += 1

            #对该字典进行排序，得到temp_li2这一有序列表
            temp_li2 = sorted(temp_dic.items(),key = itemgetter(1),reverse = True)

            #按序逐个输出攻击类型的统计结果
            i = 0
            for k,v in temp_li2:
                i+=1
                print '\t%2d. %-60s%6d'%(i,k,v)

        #统计被攻击的TOP IP 
        l2 = sorted(self.dest_ip_dic.items(),key = itemgetter(1),reverse = True)
        print '-------------------------------'
        print u'被攻击IP TOP5：'
        for i in range(5):
            print 'top %2d:\t%-18s 次数：%-7d'%(i+1,l2[i][0],l2[i][1])
            
    def __is_inner_ip(self,s):
        a_s = '10.0.0.0'
        a_e = '10.255.255.255'
        b_s = '172.16.0.0'
        b_e = '172.31.255.255'
        c_s = '192.168.0.0'
        c_e = '192.168.255.255'
    
        return a_s<s<a_e or b_s<s<b_e or c_s<s<c_e

    def __get_ip_loc(self,addrs):
        url1 = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip='
        cn_dic = {}
        cn_list = []
        for ip in addrs:
            url = url1+ip
            r = requests.get(url)
            t_dic = r.json()
            cn = t_dic['country'].encode('gbk')
            #print cn

            cn_dic.setdefault(cn,0)
            cn_dic[cn] += 1

        cn_list = sorted(cn_dic.items(),key = itemgetter(1),reverse = True)
        return cn_list

    def print_ip_loc(self):
        #print len(self.uni_src_ip_list)
        ip_loc = self.__get_ip_loc(self.uni_src_ip_list)
        print '****************************************'
        print 'IP统计'
        print '%-10s%-4s'%('国家','次数')
        print '-------------------------------'
        for k,v in ip_loc:
            print '%-10s%d'%(k,v)
        print '****************************************'

class typeCount():
    def __init__(self,filename):

        self.filename = filename
        self.sec_type = self.__get_sec_type(filename)
        self.type_dic = self.__get_type_dic(self.sec_type)
        self.sum = reduce(lambda x,y:x+y,self.type_dic.values())

        
    def __get_sec_type(self,s):
        sec_type = []
        with open(s,'rb') as f:
            result = csv.reader(f,dialect = 'excel')
            for i in result:
                if i[3]!='\xb0\xb2\xc8\xab\xc0\xe0\xd0\xcd':
                    sec_type.append(i[3])
                else:
                    continue
        return sec_type
    
    def __get_type_dic(self,sec_t):
        type_d = {}
        for i in sec_t:
            type_d.setdefault(i,0)
            type_d[i] += 1
        return type_d
    
    #calc可以用属性吗,答案是可以
    def calc(self,a):
        return float(a)*100/float(self.sum)
        
    def output(self):
        sorted_list = sorted(self.type_dic.items(),key = itemgetter(1),reverse = True)
        s = reduce(lambda x,y:x+y,self.type_dic.values())
        
        #强行使用map，首先需要将value从list中提取出来
        value_list = []
        for k,v in sorted_list:
            value_list.append(v)

        #per_list里存放着sorted_list中每个value对应的百分比
        per_list = map(self.calc,value_list)
        
        #输出到文件和屏幕
        #self.__write2file(sorted_list,per_list)
        self.__print_out(sorted_list,per_list)
        
    def __write2file(self,sl,pl):
        zl = zip(sl,pl)

        with open('type_count_test.txt','w') as f:
            f.write(''.join(['%8s%10d%10.2f%% \n'%(i[0][0],i[0][1],i[1]) for i in zl])) 
            print 'write to file  \'type_count_test.txt\'  done'

    def __print_out(self,sl,pl):
        zl = zip(sl,pl)
        print '****************************************'
        print '攻击类型统计'
        print '%s%8s%7s'%(u'安全类型',u'出现次数',u'百分比')
        print '-------------------------------'
        
        print ''.join(['%8s%10d%10.2f%% \n'%(i[0][0],i[0][1],i[1]) for i in zl])
        print '****************************************'
        '''
        for i in zl:
            print '%8s%10d%10.2f%%'%(i[0][0],i[0][1],i[1])
        '''
if __name__ == '__main__':
    '''
    ipCount对象对外拥有print_ip_loc和print_top_ip两个方法，
    print_ip_loc方法输出对源IP地址的地理位置（国家）统计结果，
    print_top_ip方法输出攻击次数最多的ip及其具体攻击名称，和被攻击次数最多的ip
    
    typeCount对象拥有output一个方法，输出安全类型统计结果
    '''
    filename = raw_input("输入文件名:")
    ip_obj = ipCount(filename)
    type_obj = typeCount(filename)

    ip_obj.print_ip_loc()
    ip_obj.print_top_ip()
    type_obj.output()
    
