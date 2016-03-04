import os,time,requests,sys
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

if(len(sys.argv)<2):
    print('USAGE: python3 PDFDownloader.py baseUrl [blacklist words]')
    exit(-1)
programName= '[PDFDownloader]'
baseUrl=sys.argv[1]
blackList=sys.argv[2:]
print(blackList)
fileList= os.listdir('.')
print(programName+"My Url: "+baseUrl+'\n'+programName+'--STARTING ROUTINE--')
htmlFile = requests.get(baseUrl)
print(programName+'--SENT REQUEST--')

"""
Per Debug decommentare questo paragrafo:

"""
print(htmlFile.text)

soupParser= BeautifulSoup(htmlFile.text,'html.parser')

for link in soupParser.find_all('a'):
    resourceName=link.get('href')
    print(resourceName)
    if(('PDF' in resourceName or 'pdf' in resourceName) and okBlackList(blackList,resourceName)):

        print(programName + 'FOUND: ' + resourceName)
        fileName=resourceName

        if(not alreadyDownloaded(fileList,fileName)):
            '''newURL=baseUrl+'/'+resourceName
            print(newURL)
            '''
            file= requests.get('http://'+resourceName)
            if(file.status_code==200):
                #Salvo il file in locale
                localeFile= open(fileName,'wb+')
                localeFile.write(file.content);
                localeFile.close();
                print(programName+'SAVED: '+fileName)
        else:
            fileStat = os.stat(fileName)
            print(programName+'ALREADY DOWNLOADED, LAST MODIFIED: '+time.asctime(time.localtime(fileStat.st_mtime)))


