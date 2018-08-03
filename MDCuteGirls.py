#! /usr/bin/env Python3
# MDCuteGirls.py - Download packs of sexy girls from the website http://mmjpg.com. Using threading.
# Just for test and learning.

import os, requests, bs4, threading

def getSoup(url):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
               'referer':'http://www.mmjpg.com/mm/1420/75'
    }
    res = requests.get(url, headers = headers)
    try:
        res.raise_for_status()
    except:
        print ('The page %s is missing...' % (url))
    res.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    return soup

def downloadMM(startNum, endNum):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
               'referer':'http://www.mmjpg.com/mm/1420/75'
    }
    for i in range (startNum, endNum+1):
        url = 'http://www.mmjpg.com/mm/' + str(i)
        print ('Opening %s' % (url))
        soup = getSoup(url)
        title = soup.select('div.main div.article h2')[0].getText()
        print ('Downloading %s to the folder %s' % (title, title))
        existGirl = []
        for folderName, subFolders, fileNames in os.walk('.'):
            for subfolder in subFolders:
                existGirl.append(subfolder)
        if title not in existGirl:
            os.makedirs('./%s' % (title), exist_ok= True)
            totlePage = int(soup.select('div.page a')[-2].getText())
            for j in range (1, totlePage+1):
                if j == 1:
                    url2 = 'http://www.mmjpg.com/mm/' + str(i)
                else:
                    url2 = 'http://www.mmjpg.com/mm/' + str(i) + '/' + str(j)
                soup2 = getSoup(url2)
                imgLink = soup2.select('div.content img')[0].get('src')
                imgRes = requests.get(imgLink, headers = headers)
                try:
                    imgRes.raise_for_status()
                except:
                    print ('The img %s is missing...' % (imgLink))
                imgRes.encoding = 'utf-8'
                imgFile = open(os.path.join('./%s' % (title), os.path.basename(imgLink)), 'wb')
                print ('Downloading the img %s' % os.path.basename(imgLink))
                for chunk in imgRes.iter_content(100000):
                    imgFile.write(chunk)
                imgFile.close()
        else:
            print ('The girl already exists...')
        print ('')

os.makedirs('/Users/meizihan/Documents/VScode/Python/sexyGirls', exist_ok=True)
os.chdir('/Users/meizihan/Documents/VScode/Python/sexyGirls')
downloadThreadList = []
for i in range(1, 1500, 100):
    downloadThread = threading.Thread(target=downloadMM, args=(i, i+99))
    downloadThreadList.append(downloadThread)
    downloadThread.start()
for downloadThread in downloadThreadList:
    downloadThread.join()
print ('Done.')
