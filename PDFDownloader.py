import os,time,requests,sys
from urllib.parse import urljoin
from colorama import init,Fore
from bs4 import BeautifulSoup



def alreadyDownloaded(fileList,resourceName):



    '''DEBUG Print
    print(fileList)
    '''


    if(resourceName in fileList):
        return True
    else:
        return False


def okBlackList(blackList,resourceName):
    result=True;
    for word in blackList:
        if(word in resourceName):
            result=False
    return result;
'''
Main Program
'''
#FOR COLOR FILTERS
init()

if(len(sys.argv)<2):
    print('USAGE: python3 PDFDownloader.py baseUrl [blacklist words]')
    exit(-1)
programName= '[PDFDownloader]'
baseUrl=sys.argv[1]
blackList=sys.argv[2:]
#print(blackList)
fileList= os.listdir('.')
downloadList=os.listdir('./Downloads')
print(Fore.GREEN+programName+"My Url: "+baseUrl+'\n'+programName+'--STARTING ROUTINE--')
htmlFile = requests.get(baseUrl)
print(programName+'--SENT REQUEST--'+Fore.RESET)

if('Downloads' not in fileList):
    os.mkdir('Downloads')

"""
Per Debug decommentare questo paragrafo:

print(htmlFile.text)
"""

soupParser= BeautifulSoup(htmlFile.text,'html.parser')

for link in soupParser.find_all('a'):
    resourceName=link.get('href')
    #print(resourceName)
    if(('PDF' in resourceName or 'pdf' in resourceName) and okBlackList(blackList,resourceName)):

        print(Fore.LIGHTCYAN_EX+ programName + Fore.RESET+ 'FOUND: ' + resourceName)
        newURL=urljoin(baseUrl,resourceName)
        #print(newURL)
        tokens=(resourceName.split('/'))
        fileName=tokens[len(tokens)-1]

        if(not alreadyDownloaded(downloadList,fileName)):



            file= requests.get(newURL)
            if(file.status_code==200):
                #Salvo il file in locale
                localeFile= open('Downloads/'+fileName,'wb+')
                localeFile.write(file.content);
                localeFile.close();
                print(Fore.LIGHTGREEN_EX+programName+'SAVED: '+fileName+Fore.RESET)
        else:
            fileStat = os.stat('Downloads/'+fileName)
            print(Fore.YELLOW+programName+'ALREADY DOWNLOADED, LAST MODIFIED: '+time.asctime(time.localtime(fileStat.st_mtime))+Fore.RESET)


