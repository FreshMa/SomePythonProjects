import requests
from bs4 import BeautifulSoup
import os

def _write2file(year):
    url = 'https://www.threatminer.org/getReport.php?e=report_list_container&t=0&q='+str(year)
    filename = str(year)+'.dat'
    res = requests.get(url)
    res.encoding = 'utf-8'
    con = res.content

    with open(filename,'wb')as f:
        f.write(con)

def getname(td):
    return td.a.string

def getds(td):
    altlist = td.find_all('a')
    retlist = []
    for alt in altlist:
        retlist.append(alt.string)
    return retlist

def write_item_to_file(name,spec,conlist):
    filename = name+spec+'.txt'
    with open(filename,'wb') as f:
        for i in conlist:
            if(i):
                f.write(i+'\n')

#save the html pages to file
def download():
    for i in xrange(2008,2018):
        _write2file(i)


def getInfo(year):
    filename = str(year)+'.dat'
    con = ''
    with open(filename,'r') as f:
        con = f.read()

    #DO NOT USE LXML!!
    soup = BeautifulSoup(con,'html.parser')

    #find divs that contain apt report information, save it to rawlist
    rawlist = soup.find_all(attrs={'class':'table table-bordered table-hover table-striped'})
    year = str(year)

    #make dirs for the reports,save them by their year
    if not os.path.exists(year):
        os.mkdir(year)

    #change working dirs
    os.chdir(year)

    for item in rawlist:
        tdlist = item.find_all('td')
        pdfname = ''
        domainlist = []
        hostlist = []
        samplelist = []

        #length of each item in tdlist is 4, [name,domains,hosts,samples]
        for i in xrange(4):
            if i==0:
                pdfname = getname(tdlist[i])
            elif i==1:
                domainlist = getds(tdlist[i])
            elif i==2:
                hostlist = getds(tdlist[i])
            elif i==3:
                samplelist = getds(tdlist[i])

        #save them in respective file
        write_item_to_file(pdfname[:-4], '_domain',domainlist)
        write_item_to_file(pdfname[:-4], '_host', hostlist)
        write_item_to_file(pdfname[:-4], '_sample', samplelist)

    #back to upper dir,ready for next iteration
    os.chdir('..')

def run():
    for i in xrange(2008,2018):
        getInfo(i)


#if __name__=='__main__':
#    run()
