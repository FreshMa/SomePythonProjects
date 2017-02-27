import requests
import re
from bs4 import BeautifulSoup
from urllib import quote

class ByrSearch():

    '''
    @param header and session : used to maintain login state
    @param name_list: store all board names,including those under secondary board content
    @func get_login_session(): use requests to login, return the session
    @func get_board_name(): traverse the leftside menu on the website to get all board names,and store them into name_list
    @func search(): use built-in searching of the website to search
    '''
    def __init__(self):    
        self.header = {'x-requested-with':'XMLHttpRequest'}
        self.session = self.get_login_session(self.header)
        self.name_list = self.get_board_name()
        
    def get_login_session(self,header):
        
        url = 'https://bbs.byr.cn/user/ajax_login.json'
        s = requests.Session()
        
        #bbs id and passwd
        byr_data = {'id':'','passwd':''}

        s.post(url,data = byr_data,headers = header)
        
        return s

    def get_board_name(self):
        sec_board_list = ['Association','School','Advertise','BYRBT']
        
        #complete the url1 with your bbs id
        url1 = 'https://bbs.byr.cn/section/ajax_list.json?uid=YOUR_ID&root=sec-'
        url_list = []
        name_list = []
        session = self.session
        header = self.header

        for i in range(1,10):
            temp_url = url1 + str(i)
            url_list.append(temp_url)
        for i in sec_board_list:
            temp_url = url1+i
            url_list.append(temp_url)

        for i in url_list:
            res = session.get(i,headers = header)
            json_res = res.json()
            for j in json_res:
                ahref = j['t']
                if 'section' not in ahref:
                    pattern = '.*board\/(.+?)\".*'
                    result = re.match(pattern,ahref)
                    name_list.append(result.group(1))
        return name_list
    
    def search(self,au,tl):
        '''
        @param au: author of the post
        @param tl: title keyword of the post
        complete s_url with your bbs id
        '''
        p_url = 'https://bbs.byr.cn/s/article?t1='+tl+'&au='+au+'&b='
        s_url = '&_uid=YOUR_ID'
        t_url = 'https://bbs.byr.cn'
        
        for i in self.name_list:
            url = p_url+str(i)+s_url
            
            r = self.session.get(url,headers = self.header)
            html = r.text
            soup = BeautifulSoup(html,'lxml')
           
            tr_list = soup.find_all('tr')
            for tr in tr_list:
                length = len(tr)
                t1 = tr('td',class_='title_9')
                t2 = tr('td',class_='title_10')
                if length==7 and t1:
                    href = t_url+t1[0]('a')[0]['href']
                    string = t1[0]('a')[0].string
                    time = t2[0].string

                    print time+' '*4+href+'\n'+' '*14+string+'\n'
                    

                
if __name__ == '__main__':
    obj = ByrSearch()
    au = ''
    tl = 'test'
    tl = quote(tl)
    obj.search(au,tl)
