# -*-coding:utf8-*-
import os
import shutil
from PIL import Image
import hashlib
import platform
import sys

def file_list(path):
    path = path+'/temp'
    li = os.listdir(path)
    li2 = []
    #要删除的文件名列表
    del_list = []
    #文件的md5值列表
    md5_list = []
    '''
    遍历文件夹下的文件，如果发现以'jpg'结尾的文件且该文件没有重复过，
    就将它加到要返回的文件列表li2中；如果发现重复文件，就将它加到删除列表del_list中，
    在遍历完成之后将del_list中的文件删除
    去重是通过判断文件的md5值是否重复出现来完成的
    '''
    for i in li:
        if i[-3:]=='jpg':
            full_name = path+'/'+i
            
            with open(full_name,'rb') as f:
                m = hashlib.md5()
                m.update(f.read())
                dig = m.hexdigest()
                #将重复文件的文件名加到del_list中
                if dig in md5_list:
                    del_list.append(full_name)
                #如果没重复就加到li2中
                else:
                    md5_list.append(dig)
                    li2.append(i)
    #删除重复的文件
    for i in del_list:
        os.remove(i)
    return li2

def file_filter(path,list1):
    '''
    PIL的Image.open方法没有对应的close方法，也就是说如果直接将文件路径传递给该函数，
    无法主动关闭文件，这对接下来的删除操作造成了麻烦；
    所以我们采用python自带的Open()函数打开图像文件，将文件指针传递给Image.open()方法，
    这样就可以调用文件指针的关闭方法来主动关闭文件，进而删除该文件
    '''
    list_1920 = []
    list_1080 = []
    #i是文件名
    pre_path = path + '/temp/'
    for i in list1:     
        ab_path = pre_path + i
        try:
            fp = open(ab_path,'rb')
            im = Image.open(fp)
            if im.size[0] == 1920:
                list_1920.append(i)
                fp.close()
            elif im.size[0] == 1080:
                list_1080.append(i)
                fp.close()
            else:
                fp.close()
                os.remove(ab_path)       
        except IOError:
            fp.close()
            os.remove(ab_path)
            continue

    dir_1080 = path + u'/1080p竖屏'
    dir_1920 = path + u'/1080p横屏'
    try:
        os.mkdir(dir_1080)
        os.mkdir(dir_1920)
    except OSError as err:
        if err.args[0] == 183:
            print 'WARN:'+u'1080p横竖屏文件夹已存在'
    for f in list_1080:
        src_name = pre_path + f
        dst_name = dir_1080 + '/' + f
        shutil.copy2(src_name,dst_name)

    for f in list_1920:
        src_name = pre_path + f
        dst_name = dir_1920 + '/' + f
        shutil.copy2(src_name,dst_name)
    

def copy_file(path):
    #pfl用来存储已读取的过的文件名
    pflist = []
    #获取环境变量USERPROFILE
    up = os.environ['USERPROFILE']
    ori_wp_dir = up+'\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets'
    dir_list1 = os.listdir(ori_wp_dir)
    #目标目录是D盘的wpdir文件夹，建立临时文件夹，存放所有文件
    dst_dir1 = path
    dst_dir = path+'/temp'

    istxt = 1
    try:
        os.mkdir(dst_dir1)
    except OSError as err:
        if err.args[0] == 183:
            print 'WARN:'+dst_dir1+u'已存在'
    
    try:
        os.mkdir(dst_dir)
    except OSError as err:
        if err.args[0] == 183:
            print 'WARN:'+dst_dir+u'已存在'
            
    #从文件中读取已处理过的文件，并保存到pflist列表中
    protxt = dst_dir+'/processed.txt'    
    try:
        with open(protxt,'r') as fp1:
            while 1:
                #readline之后要用strip去掉文件后面的换行符，很重要
                line = fp1.readline().strip()
                if line == '' or line == '\n':
                    break
                else:
                    pflist.append(line)
    #如果无法读取说明是文件不存在，也就是第一次运行本程序。
    except IOError:
        istxt = 0
        print '没有找到processed.txt，即将创建...'
        
    '''
    dir_list1是源文件夹下的所有文件名组成的列表
    如果dir_list1中的元素已经在pflist中出现过，那就跳过，不进行处理；
    如果没有出现过，说明是微软下载的新图片，将它加入pflist中；
    随后写到文件protxt中。
    
    复制操作需要绝对路径，使用os.path.join来拼接路径
    '''
    isnew = 0
    for name in dir_list1:
        if name in pflist:
            #print u'已存在'
            continue
        else:
            isnew = 1
            pflist.append(name)
            src_name = os.path.join(ori_wp_dir,name)
            dst_name = os.path.join(dst_dir,name)
            shutil.copy2(src_name,dst_name)
    if isnew == 1:
        print u'成功复制到temp文件夹中'  
    
    #第一次运行时负责创建该文件
    with open(protxt,'w') as fp2:
        if istxt == 0:
            print u'processed.txt已创建'
        for name in pflist:
            fp2.write(name)
            fp2.write('\n')
    return isnew

def ren(path):
    path = path+'/temp'
    fl = os.listdir(path)
    '''
    对文件夹中没有进行过重命名的文件进行重命名，判断依据是是否以.jpg结尾
    '''
    isren = 0
    try:
        for name in fl:     
            if (name[-3:]!='txt' and name[-3:]!='jpg'):
                #rename函数需要绝对路径，当然也可以事先切换工作目录，然后用相对路径
                src_name = os.path.join(path,name)
                dst_name = os.path.join(path,name+'.jpg')
                os.rename(src_name,dst_name)
                isren = 1
            else:
                continue
        if isren == 1:
            print u'重命名成功'
    except WindowsError as err:
        if err.args[0] == 183:
            print 'WARN:'+u'目的文件夹有重名文件，无法完成重命名'
        elif err.args[0] == 2:
            print 'WARN:'+u'请使用绝对路径'
        

if __name__ == '__main__':
    pf = platform.platform()
    try:
        assert pf[:10]=='Windows-10'
    except AssertionError:
        print 'win10 only'
        sys.exit()
    path = 'D:/win10wp'
    t = copy_file(path)
    if t==1:
        ren(path)
        list1 = file_list(path)
        file_filter(path,list1)
        print u'成功'
    else:
        print u'没有新文件'
    
